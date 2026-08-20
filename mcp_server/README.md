# Phishing Triage Tool Server (MCP)

The tool server students connect in **Lab 5**. It exposes three mock security-investigation
tools over the Model Context Protocol, backed by a local JSON fixture, no API keys, no
network calls, no data leaving the machine.

## Run

```bash
python3 -m pip install -r requirements.txt
python3 server.py
```

The server produces no output and does not exit. That's correct, it's waiting on stdio for
a client to connect. `Ctrl-C` to stop.

## Tools

| Tool | Arguments | Returns |
|---|---|---|
| `check_url_reputation` | `url` | MALICIOUS / CLEAN / UNKNOWN, threat type, confidence |
| `check_sender_reputation` | `email_address` | Known-phishing / suspicious / trusted, recommendation |
| `check_email_authentication` | `from_address`, `spf`, `dkim`, `dmarc` | Per-mechanism breakdown and spoofing risk |

All three read `../data/threat_intel_db.json`, resolved relative to `server.py`'s own
location, so the server works from any working directory, but the file must stay where it
is relative to the script.

## Note on tool descriptions

Each tool's docstring is what the model reads when deciding whether to call it. It is a
prompt, not developer documentation. If you edit the tools, keep the "Use this whenever…"
sentence, Lab 5 Step 2 teaches directly from it, and vaguer descriptions measurably reduce
how often the agent calls the tool at the right time.

## Provenance

The tool logic and the threat-intel fixture are ported from the GTK Cyber AI Cyber
Bootcamp's LangGraph labs (`utils/mock_tools.py`), so results are directly comparable
between the coded and GUI versions of the same exercise.
