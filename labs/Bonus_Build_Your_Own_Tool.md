<img src="../assets/img/GTK_Logo_Social_Icon.jpg" width="175" align="right" />

# Lab 5: Your Own Tool

**Estimated time: 30 minutes**
_UI steps verified: **2026-08-19**, Claude (web, Max) and ChatGPT (web, Free). See the
platform-support note below; this lab has a hard constraint the others don't._

## Learning objectives

- Understand what MCP is and why it exists
- Run a tool server locally and connect a GUI agent to it
- Give your agent capabilities that no built-in provides
- See a real, trustworthy record of what the agent actually called

## What you'll build

Your agent gets three security tools that you control:

```
    [ your agent in the browser ]
                │  "call check_url_reputation('https://..')"
                ▼
    [ MCP server on your laptop ]  ──►  local threat-intel database
                │  "MALICIOUS / credential_phishing / 98%"
                ▼
    [ agent continues reasoning ]
```

---

## Concept: what MCP is

In Lab 2 you used built-in tools. They're useful and generic, search the web, run some
code. What they can't do is query *your* threat intel, *your* ticketing system, *your*
asset inventory. That's most of what a real SOC agent needs.

**MCP (Model Context Protocol)** is an open standard for exposing tools to an AI
application. You run a server, the server advertises its tools, and any MCP-capable client
can call them. It's the same idea as the `@tool` decorator in a Python agent framework,
except the tools live in a separate process and any client can use them.

The important property for this workshop: **the server runs on your machine.** Your threat
intel doesn't leave your laptop. The model asks for a lookup and receives the result, it
never gets the database.

## Concept: descriptions are the interface

Look at what the server tells the model about one of its tools:

```python
@mcp.tool()
def check_url_reputation(url: str) -> str:
    """Check a URL against the threat intelligence database.

    Use this whenever an email contains a link. Returns a verdict of MALICIOUS,
    CLEAN, or UNKNOWN along with a threat type and confidence score.

    Args:
        url: The full URL to check, including scheme.
    """
```

The model never sees the implementation. It sees the name, that docstring, and the argument
types, and decides from those alone whether to call it. "Use this whenever an email
contains a link" isn't a comment for a developer; it's a prompt aimed at the model.

Badly described tools are the most common cause of an agent that has the right capability
and doesn't use it.

---

## Before you start: the one hard constraint

Labs 1–4 ran entirely in a browser. This one can't, and it's worth understanding why rather
than just working around it.

An MCP server can talk to a client two ways. **Local (stdio)** means the client launches the
server as a process on your machine and talks to it over standard input/output, private, no
network, but only possible if the client *is* on your machine. **Remote (HTTPS)** means the
client makes web requests to a URL, which works from anywhere but requires the server to be
reachable from the internet.

A web browser can't launch a process on your laptop. So:

| Client | Local stdio server | Remote HTTPS server |
|---|---|---|
| Claude desktop app | ✅ | ✅ |
| Claude in a browser | ❌ | ✅, *Add custom connector* takes an HTTPS URL |
| ChatGPT (Free) | ❌ | ❌, no custom connector on this tier |
| ChatGPT (paid tiers) | ❌ | Check your plan |

**This is why the workshop's parallel tracks stop here.** Pick the path your setup allows:

- **Path A, Claude desktop app (recommended).** Runs `server.py` locally. Nothing leaves
  your machine. Requires the desktop app installed.
- **Path B, Claude in the browser + a tunnel.** Run the server locally, expose it over
  HTTPS with a tunnel, and add that URL as a custom connector. Works without the desktop app
  but puts a public URL in front of your laptop, see the warning in Path B.
- **Path C, Watch.** If neither is available, pair with someone on Path A, or follow the
  instructor's screen. **You will still learn the lesson in Step 4**, which is the point of
  the lab.

Your instructor will tell you which path the room is taking.

## Step 1: Start the server

In a terminal:

```bash
cd mcp_server
python3 server.py
```

It will start and sit there with no output. **That's correct**, it's waiting to be spoken
to. Leave this terminal open for the rest of the lab.

The three tools it provides:

| Tool | What it does |
|---|---|
| `check_url_reputation` | Looks a URL up in the threat-intel database |
| `check_sender_reputation` | Checks a sender address and domain |
| `check_email_authentication` | Evaluates SPF/DKIM/DMARC and rates spoofing risk |

All three read `data/threat_intel_db.json` locally. No API keys, no network calls.

## Step 2: Connect your agent

> ### Path A, Claude desktop app
>
> Add the server to the desktop app's MCP server configuration, pointing it at the absolute
> path to `server.py`, then restart the app. The desktop app launches the process for you,
> you can stop the terminal copy from Step 1.
>
> <!-- VERIFY: config file path and exact JSON shape not yet walked. Do this on the delivery
>      machine before the session and paste the working config here. -->

> ### Path B, Claude in the browser, via a tunnel
>
> 1. With `server.py` running, expose it over HTTPS using a tunnel of your choice. Your
>    instructor will provide the exact command for the room.
> 2. In Claude, click **+** in the message box → **Connectors** → **Add connector** →
>    **Add custom connector**.
> 3. Give it a **Name** (`GTK Phishing Tools`) and paste your tunnel's HTTPS URL into
>    **Remote MCP server URL**. Leave the OAuth fields empty.
> 4. Click **Add**.
>
> ⚠️ **A tunnel makes your laptop reachable from the internet.** For this workshop the server
> only reads a fake threat-intel file, so the exposure is minimal, but treat it as a
> workshop-only technique, shut the tunnel down when you're done, and never do this with a
> tool that has real side effects. Claude's own dialog makes the general point: *"Only use
> connectors from developers you trust."*

**Confirm it worked:** ask your agent what tools it has available. All three should be
listed by name. If they aren't, stop here, nothing later in the lab will work.

## Step 3: Investigate with real tools

```text
Investigate EMAIL-001 from emails.json. Use your connected tools to check the
sender, every URL, and the authentication headers. Show me each tool call and
its result before giving your verdict.
```

You should see approval prompts and tool-result cards in the interface. Compare what comes
back to what your agent *guessed* in Lab 1:

| | Lab 1 (reasoning only) | Lab 5 (real tools) |
|---|---|---|
| Verdict | | |
| Confidence | | |
| Indicators | | |

The tools return hard facts, `142 reports since 2025-06-10`, `98% confidence`, instead of
inference from the text. This is the difference between "this domain looks like a typo of
Microsoft" and "this sender has 142 phishing reports."

## Step 4: The audit record you can trust

This is the part that matters most, and it's easy to miss.

In Lab 3 you asked the agent to report its own `checks_performed`, and I pointed out that
you were trusting the agent's self-report. Now you have something better: **the tool
approval prompts and result cards are generated by the platform, not the model.** They are
a record of what was actually called.

Re-run the Lab 3 compliance question against a handful of emails, but this time check the
agent's `checks_performed` field against the tool calls you actually saw:

| Email | `checks_performed` claims | Tool calls you observed | Match? |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

If those ever diverge, you've found something important: the agent's account of its own
behavior is not reliable, and only the execution layer's record is.

## Step 5: Break the tool loop

Combine this with Lab 4. Ask your agent to investigate `EMAIL-P03` from
`emails_poisoned.json`, the one whose payload is inside the URL query string.

Watch what argument it passes to `check_url_reputation`. The attacker-controlled string is
now flowing into a tool call.

```text
Investigate EMAIL-P03 using your tools. Show me the exact arguments you pass
to each tool.
```

In this lab the tool just does a database lookup, so nothing bad happens. Now imagine the
tool ran a shell command, queried a SIEM, or opened a ticket. **Attacker-controlled text
reaching a tool's arguments is the thing to worry about**, and it's the reason tool
approval prompts exist.

---

## Checkpoint

- [ ] The MCP server is running locally
- [ ] My agent lists all three tools (or I followed along on Path C)
- [ ] I've investigated an email with real tool calls and seen the results
- [ ] I've compared tool-derived findings against Lab 1's reasoning-only verdict
- [ ] I've checked `checks_performed` against the tool calls I actually observed
- [ ] I've seen attacker-controlled text reach a tool argument

## Think about it

1. The threat-intel database never left your laptop, but the *results* went to the model.
   What did you disclose, and is that acceptable for your organization's data?
2. Approval prompts are meaningful for 5 emails. What happens to that control at 5,000?
3. What tool would make this agent useful in your environment? What would have to be true
   before you let a model call it?

**Next:** [The wrap](../WRAP.md), the honest ledger.
