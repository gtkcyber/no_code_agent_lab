"""GTK Cyber — phishing triage tool server (MCP).

Exposes three mock security-investigation tools over the Model Context Protocol so a
ChatGPT or Claude agent can call them from the GUI. All lookups hit the local
data/threat_intel_db.json fixture, so no API keys and no network egress are required.

Run:  python server.py
"""

import json
from pathlib import Path
from urllib.parse import urlparse

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("gtk-phishing-tools")

_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "threat_intel_db.json"
_THREAT_DB = json.loads(_DB_PATH.read_text())


@mcp.tool()
def check_url_reputation(url: str) -> str:
    """Check a URL against the threat intelligence database.

    Use this whenever an email contains a link. Returns a verdict of MALICIOUS, CLEAN,
    or UNKNOWN along with a threat type and confidence score.

    Args:
        url: The full URL to check, including scheme.
    """
    for entry in _THREAT_DB["url_reputation"]:
        if url.startswith(entry["url"]) or entry["url"].startswith(url.split("?")[0]):
            threat = entry.get("threat_type") or "none"
            return (
                f"URL: {url}\n"
                f"Verdict: {entry['verdict'].upper()}\n"
                f"Threat Type: {threat}\n"
                f"Confidence: {entry['confidence']:.0%}"
            )

    try:
        domain = urlparse(url).netloc
    except Exception:
        domain = url

    for entry in _THREAT_DB["malicious_domains"]:
        if entry["domain"] in domain:
            return (
                f"URL: {url}\n"
                f"Verdict: MALICIOUS\n"
                f"Threat Type: {entry['category']}\n"
                f"Confidence: {entry['confidence']:.0%}\n"
                f"Note: Domain {entry['domain']} flagged since {entry['first_seen']}"
            )

    for entry in _THREAT_DB["safe_domains"]:
        if entry["domain"] in domain:
            return (
                f"URL: {url}\n"
                f"Verdict: CLEAN\n"
                f"Threat Type: none\n"
                f"Confidence: 95%\n"
                f"Note: Domain {entry['domain']} is a verified {entry['category']} domain"
            )

    return (
        f"URL: {url}\n"
        f"Verdict: UNKNOWN\n"
        f"Threat Type: unknown\n"
        f"Confidence: N/A\n"
        f"Note: URL not found in threat intelligence database"
    )


@mcp.tool()
def check_sender_reputation(email_address: str) -> str:
    """Check a sender's address and domain against phishing and reputation databases.

    Use this on the from_address of any email under investigation. Returns whether the
    sender is a known phishing source, a suspicious domain, or a trusted sender.

    Args:
        email_address: The sender's full email address.
    """
    for entry in _THREAT_DB["known_phishing_senders"]:
        if entry["email"] == email_address:
            return (
                f"Sender: {email_address}\n"
                f"Verdict: KNOWN PHISHING SENDER\n"
                f"Reports: {entry['reported_count']} reports since {entry['first_reported']}\n"
                f"Recommendation: BLOCK"
            )

    domain = email_address.split("@")[-1] if "@" in email_address else email_address

    for entry in _THREAT_DB["malicious_domains"]:
        if entry["domain"] == domain:
            return (
                f"Sender: {email_address}\n"
                f"Verdict: SUSPICIOUS DOMAIN\n"
                f"Domain Category: {entry['category']}\n"
                f"Domain First Seen: {entry['first_seen']}\n"
                f"Confidence: {entry['confidence']:.0%}\n"
                f"Recommendation: INVESTIGATE"
            )

    for entry in _THREAT_DB["safe_domains"]:
        if entry["domain"] == domain:
            return (
                f"Sender: {email_address}\n"
                f"Verdict: TRUSTED SENDER\n"
                f"Domain Category: {entry['category']}\n"
                f"Domain Verified: {entry['verified']}\n"
                f"Recommendation: ALLOW"
            )

    return (
        f"Sender: {email_address}\n"
        f"Verdict: UNKNOWN\n"
        f"Note: Sender not found in reputation databases\n"
        f"Recommendation: PROCEED WITH CAUTION"
    )


@mcp.tool()
def check_email_authentication(from_address: str, spf: str, dkim: str, dmarc: str) -> str:
    """Evaluate SPF, DKIM, and DMARC results to assess whether an email was spoofed.

    Use this whenever the email's headers include authentication results. Returns a
    per-mechanism breakdown and an overall risk rating.

    Args:
        from_address: The sender's email address.
        spf: SPF result (pass, fail, softfail, neutral, none).
        dkim: DKIM result (pass, fail, none).
        dmarc: DMARC result (pass, fail, none).
    """
    results = []
    score = 0.0

    spf_lower = spf.lower()
    if spf_lower == "pass":
        results.append("SPF: PASS - Sender IP is authorized to send for this domain")
        score += 1
    elif spf_lower == "softfail":
        results.append(
            "SPF: SOFTFAIL - Sender IP is NOT explicitly authorized "
            "(possible misconfiguration or spoofing)"
        )
        score += 0.5
    elif spf_lower == "neutral":
        results.append("SPF: NEUTRAL - Domain makes no assertion about this sender")
        score += 0.25
    else:
        results.append(
            "SPF: FAIL - Sender IP is NOT authorized to send for this domain (likely spoofed)"
        )

    if dkim.lower() == "pass":
        results.append("DKIM: PASS - Email signature is valid and verified")
        score += 1
    else:
        results.append(
            "DKIM: FAIL - Email signature is invalid or missing (message may be tampered)"
        )

    if dmarc.lower() == "pass":
        results.append("DMARC: PASS - Email passes domain alignment checks")
        score += 1
    else:
        results.append("DMARC: FAIL - Email fails domain alignment (high risk of spoofing)")

    if score >= 2.5:
        overall, risk = "LEGITIMATE - Authentication checks pass", "LOW"
    elif score >= 1.5:
        overall, risk = "INCONCLUSIVE - Some authentication checks fail", "MEDIUM"
    else:
        overall, risk = "SUSPICIOUS - Most authentication checks fail", "HIGH"

    body = "\n".join(results)
    return (
        f"Email Authentication Analysis for {from_address}\n"
        f"{'=' * 50}\n"
        f"{body}\n"
        f"{'=' * 50}\n"
        f"Overall: {overall}\n"
        f"Spoofing Risk: {risk}"
    )


if __name__ == "__main__":
    mcp.run()
