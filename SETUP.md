<img src="assets/img/GTK_Logo_Social_Icon.jpg" width="175" align="right" />

# Pre-Workshop Setup

**Do this before the session starts.** The workshop is 2.5 hours and every minute spent
creating accounts is a minute not spent building. Budget 15 minutes.

_Tiers verified 2026-08-19 against live ChatGPT and Claude._

## 1. Pick a platform and get an account

You need **one** of the following. Both tracks are fully supported; pick the one you'll
keep using after the workshop.

| | ChatGPT | Claude |
|---|---|---|
| What you'll build in | **Project** | **Project** |
| Where | chatgpt.com | claude.ai |
| Labs 1–5 | Works on a **free** account | Paid plan <!-- VERIFY: minimum tier untested --> |
| Gmail connector | Plugins → Gmail | Settings → Customize → Connectors → Gmail |

**Good news on cost:** ChatGPT **Projects** carry instructions, file uploads, and code
execution on a free account, verified, along with the Gmail connector. That covers the
entire workshop with no subscription. We deliberately use Projects rather than **Custom
GPTs**, which do require ChatGPT Plus.

### Verify your account works

Sign in and confirm you can create a project with instructions:

- **ChatGPT:** sidebar → **Projects** → **New**. Then **…** → **Project settings** and check
  you can see an **Instructions** box.
- **Claude:** sidebar → **Projects** → **New project**. On the project page, check the
  right-hand panel has an **Instructions** section and a **Context** section.

If either is missing, flag it before the session.


## 2. Create a throwaway Gmail account, **required**

From Lab 2 onward you connect a real mailbox to your AI agent, and in Lab 4 you deliberately
send that mailbox hostile content. **Do not use your personal or work email.**

1. Create a new Google account at accounts.google.com. Two minutes; no phone number needed
   in most regions.
2. Sign in to it once in a browser so the mailbox exists.
3. **Seed it with 8–10 messages** so Lab 2 has something to triage. The fastest way: sign up
   for a few newsletters, forward yourself some mail, and let some spam accumulate. A mix of
   obvious marketing, real correspondence, and junk is ideal, variety is what makes Lab 2
   interesting.
4. Know the address. You'll email it in Lab 4.

**Why not your real inbox?**

- You are granting a third-party service persistent, scoped read access.
- Every message the agent reads is sent to a model provider for processing.
- In Lab 4 you deliberately deliver crafted attack content to this mailbox.
- Corporate Google Workspace accounts commonly block third-party OAuth anyway, so a work
  account will often just fail.

If you cannot create one, tell the instructor before the session. You can complete Labs 1, 3,
and 5 without a connected mailbox, and Lab 4 has an offline fallback using
`data/emails_poisoned.json`.

## 3. Download the workshop files

Get the workshop bundle and confirm you have:

```
data/emails.json           50 labeled emails, the main dataset
data/emails_small.json      5 emails, for quick iteration in Lab 1
data/emails_poisoned.json   Lab 4 only. Contains a deliberate attack. Don't read ahead.
data/threat_intel_db.json   Mock threat intel backing the Lab 5 tools
mcp_server/                 The tool server you'll connect in Lab 5
```

You'll upload files from `data/` into your agent, so know where they landed on disk.

## 4. Optional bonus lab only: Python

The bonus lab is the one place you touch a terminal, and it's copy-paste.

**Nothing in the main 2.5-hour arc requires a terminal.** This section applies only to the
optional take-home bonus lab, where you run your own MCP tool server. Skip it unless you
plan to do that.

Check you have Python 3.10 or newer:

```bash
python3 --version
```

Then install the one dependency:

```bash
cd mcp_server
python3 -m pip install -r requirements.txt
```

Confirm the server starts (it will sit there waiting, that's correct):

```bash
python3 server.py
```

Press `Ctrl-C` to stop it. **If this works, you're done.** If it doesn't, flag it at the
start of the session rather than during Lab 5.

> **For the bonus lab only:** the **Claude desktop app** is the clean way to run a local MCP
> server, no tunnel, nothing exposed to the internet.

## 5. Network

Everything runs against cloud APIs. Conference and hotel wifi are the single most common
cause of a bad workshop. If you can tether to a phone as backup, have it ready.

## Pre-flight checklist

- [ ] Account on ChatGPT (free is fine) **or** Claude, signed in
- [ ] I can create a Project and find its **Instructions** field
- [ ] **Throwaway Gmail account created, and I know the address**
- [ ] **That inbox has 8–10 messages in it**
- [ ] Workshop files downloaded, and I know the path to `data/`
- [ ] `python3 --version` returns 3.10+
- [ ] `pip install -r mcp_server/requirements.txt` completed without errors
- [ ] `python3 mcp_server/server.py` starts without an error
- [ ] (Bonus lab only) Claude desktop app installed
- [ ] Backup network available
