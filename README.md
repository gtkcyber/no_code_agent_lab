<img src="assets/img/GTK_Logo_Social_Icon.jpg" width="175" align="right" />

# Building AI Agents Without Code

**A GTK Cyber workshop, 2.5 hours, hands-on, no programming required.**

You will build a working phishing-triage agent using nothing but the ChatGPT and Claude
web interfaces. By the end you will have an agent that reads an email, decides how much
scrutiny it deserves, calls real security tools to gather evidence, pauses for your
approval, and returns a structured verdict, and you will have a clear-eyed view of where
this approach stops being enough.

> **UI verified 2026-08-19** against live ChatGPT (Free) and Claude (Max) on the web, with
> screenshots captured from the live products. Open items are tracked in
> `instructor/VERIFICATION_CHECKLIST.md`.

---

## Who this is for

Security practitioners, SOC analysts, threat hunters, incident responders, security
leadership, who want to build agents but don't write Python. No prior AI, agent, or
programming experience is assumed. You need to be able to read an email header and know
what SPF means; everything else is taught here.

If you *do* write Python, this workshop is still useful as a speed-and-tradeoff study, but
you may prefer the full LangGraph treatment in GTK Cyber's AI Cyber Bootcamp.

## What you need

- A laptop with a modern browser and reliable internet. **Everything here runs in the cloud.**
- An account on **ChatGPT** *or* **Claude**. Labs 1–4 work on a **free** ChatGPT account,
  we use Projects, not Custom GPTs, partly for this reason. See `SETUP.md` and do it **before
  you arrive**, not in the room.
- **A throwaway Gmail account**, created before the session. From Lab 2 you connect real mail
  to your agent, and in Lab 4 you deliberately send it hostile content. Neither belongs near
  your personal or work inbox. `SETUP.md` walks you through it.
- Nothing else. The whole workshop runs in a browser. The optional bonus lab needs Python and
  a terminal; nothing in the main arc does.

Both platforms are covered in parallel throughout. Pick one and stay on it; a ChatGPT student
and a Claude student finish together with the same artifact.

## Agenda

| Time | Lab | What you learn |
|---|---|---|
| 0:00–0:15 | Setup and framing | What an agent is, and what it is not |
| 0:15–0:40 | **[Lab 1](labs/Lab_1_Build_Your_First_Agent.md)**, Build your first agent | Instructions, context files, structured output |
| 0:40–1:10 | **[Lab 2](labs/Lab_2_Connect_Your_Email.md)**, Connect your email | Connectors, OAuth scope, and real messy input |
| 1:10–1:35 | **[Lab 3](labs/Lab_3_Tools_and_Routing.md)**, Tools and routing | Tool use, and whether your rules are actually obeyed |
| 1:35–1:55 | **[Lab 4](labs/Lab_4_Injection.md)**, Injection | Send yourself an attack and watch it steer your agent |
| 1:55–2:25 | **[Lab 5](labs/Lab_5_Multi_Agent.md)**, Multi-agent team | Real specialist agents, with you as the supervisor |
| 2:25–2:40 | **[Wrap](WRAP.md)** | The honest ledger: GUI vs. code, and when to graduate |

Optional take-home: **[Bonus](labs/Bonus_Build_Your_Own_Tool.md)**, run a local MCP server
and give an agent security tools you built yourself.

## The running scenario

You are building a phishing triage agent, and you'll point it at two different kinds of input.

**Sample data, for measuring.** `data/emails.json` holds 50 emails, 25 phishing, 22
legitimate, and 3 ambiguous. Each has authentication headers, extracted URLs, and a
`ground_truth` label. Because the labels are there you can actually **score** your agent
instead of admiring it. `data/emails_small.json` is 5 of them for quick iteration.

**Your own inbox, for realism.** From Lab 2 onward you connect a real Gmail account and
triage live messages. This is where you find out that clean sample data was doing a lot of
work for you.

You need both. Real mail has no labels, so it can't tell you whether your agent is any good,
and "how would I know if it's any good" is the central question of this workshop, not "can I
build one." You can build one in about twenty minutes.

## What you build

By the wrap you will have:

1. A custom agent, saved in your own account, that triages phishing email.
2. A live connection to a real mailbox, and a list of everything that broke when you pointed
   the agent at it.
3. A measured accuracy number against 50 labeled emails, and a second number from re-running
   the same emails, showing how much the answer moves between runs.
4. A demonstration of your own agent being steered by an email you sent it.
5. A four-agent SOC team with you as the supervisor, and a measurement of what that costs.
6. A written view on which parts of this belong in a GUI and which belong in code.

## Repository layout

```
README.md     This file.
SETUP.md      Pre-workshop setup. Do this before you arrive.
labs/         Participant guides, one per lab. Start here.
WRAP.md       Closing discussion and the GUI-vs-code ledger.
instructor/   Facilitation notes, answer key, verification checklist. Not for participants.
data/         The email dataset and the mock threat-intel database.
mcp_server/   The tool server students connect in Lab 5.
assets/       Branding and screenshots.
```

## A note on shelf life

Both interfaces change frequently. Each lab separates **concepts** (stable) from **UI
steps** (volatile, in clearly marked boxes). If a menu name has drifted, the concept
section still tells you what you are looking for. Instructors: re-verify the UI boxes
before each delivery and update the "verified against" stamp at the top of each lab.

_Workshop content © GTK Cyber. Dataset and threat-intel fixtures adapted from the GTK
Cyber AI Cyber Bootcamp._
