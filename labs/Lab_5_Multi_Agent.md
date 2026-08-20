<img src="../assets/img/GTK_Logo_Social_Icon.jpg" width="175" align="right" />

# Lab 5: Build a Multi-Agent Team

**Estimated time: 30 minutes**
_UI steps verified: **2026-08-19**, Claude (web, Max) and ChatGPT (web, Free)._

## Learning objectives

- Decompose one agent into specialists with separate contexts
- Act as the supervisor, and feel what supervision actually costs
- Tell real multi-agent architecture apart from a model doing impressions
- Decide when the coordination overhead is worth it

## What you'll build

```
                       ┌──────────────────┐
                  ┌───►│  Header Analyst  │───┐
                  │    └──────────────────┘   │
    email ───► YOU ───►│ Content Analyst  │───┤───► YOU ───► verdict
                  │    └──────────────────┘   │  (supervisor)
                  │    ┌──────────────────┐   │
                  └───►│   URL Analyst    │───┘
                       └──────────────────┘
```

Notice who is in the middle. That is the lab.

---

## Concept: what makes multi-agent *multi*-agent

It is more than one model playing three roles. The properties that matter are:

| Property | Why it matters |
|---|---|
| **Isolated context** | A specialist sees only its slice. It can't be biased by another's reasoning, and it can't blow its context on irrelevant detail. |
| **Its own tools** | Each agent gets only what its job needs, so a mistake reaches less. |
| **Explicit hand-offs** | Findings move as structured messages, not shared memory. |
| **Synthesis** | Someone weighs conflicting specialist opinions and decides. |

**The obvious shortcut fails this test.** Write one prompt saying "act as a header analyst,
then a content analyst, then synthesize" and you get a single model, in a single context,
playing all three parts in sequence with each part visible to the others. It matches the
diagram above and has none of the four properties.

You can prove this to yourself in one prompt, which is Step 5.

**The version that works without code** is to build separate agents and move the messages
yourself. The isolation is real because the projects are separate. The only missing piece is
automation, and noticing what is missing is the point of the lab.

## Step 1: Create three specialists

Create **three new Projects**, exactly as you did in Lab 1. Each gets its own instructions
and nothing else, no shared context, no knowledge of the others.

> **Keep moving.** These prompts are short on purpose. You have 30 minutes, and the lesson is
> not in the wording.

**Project: `Header Analyst`**

```text
You analyze ONLY email authentication and sender reputation. You never comment on
message wording, links, or attachments. Those belong to other analysts, and commenting on
them breaks the team's independence.

Given an email, examine: SPF, DKIM, DMARC results; sender domain; display-name vs.
address mismatches; lookalike or newly-seen domains.

Respond ONLY with:
{
  "specialist": "header",
  "risk": "<high | medium | low>",
  "confidence": <0.0-1.0>,
  "findings": ["<specific observable>", ".."],
  "insufficient_data": <true | false>
}
```

**Project: `Content Analyst`**

```text
You analyze ONLY the language and social engineering of an email. You never comment
on headers, domains, or link reputation. Those belong to other analysts.

Given an email, examine: urgency and pressure tactics; authority claims; requests
for credentials, payment, or secrecy; emotional manipulation; unusual phrasing for
the claimed sender.

Respond ONLY with:
{
  "specialist": "content",
  "risk": "<high | medium | low>",
  "confidence": <0.0-1.0>,
  "findings": ["<specific observable>", ".."],
  "insufficient_data": <true | false>
}
```

**Project: `URL Analyst`**

```text
You analyze ONLY links and attachments. You never comment on headers or message
wording. Those belong to other analysts.

Given an email, examine: destination domains; lookalike or homoglyph domains; URL
shorteners; mismatches between anchor text and destination; suspicious paths or
query parameters; attachment types and double extensions.

Respond ONLY with:
{
  "specialist": "url",
  "risk": "<high | medium | low>",
  "confidence": <0.0-1.0>,
  "findings": ["<specific observable>", ".."],
  "insufficient_data": <true | false>
}
```

## Step 2: Create the supervisor

**Project: `SOC Supervisor`**

```text
You are a SOC lead. You do not analyze email yourself. You receive reports from
three specialists -- header, content, and URL -- and synthesize a final verdict.

Rules:
- Weigh the specialists. A high-confidence finding from one specialist can outweigh
  two low-confidence "low risk" reports.
- If specialists disagree, say so explicitly and explain which you weighted and why.
- If any specialist reports insufficient_data, factor that uncertainty into your
  confidence rather than ignoring it.
- Never invent findings no specialist reported. You have not seen the email.

Respond with:
{
  "verdict": "<phishing | suspicious | legitimate>",
  "confidence": <0.0-1.0>,
  "reasoning": "<how you weighed the specialists>",
  "disagreement": "<describe any conflict, or 'none'>",
  "recommended_action": "<block_and_alert | quarantine | deliver_with_warning | deliver>"
}
```

## Step 3: Run an investigation

Take **EMAIL-006** from `emails.json` (a business email compromise, subtle, and the one
where specialists most often disagree). Paste the raw email into each of the three
specialists **in separate conversations**. Collect the three JSON outputs.

Then paste all three into the supervisor:

```text
Here are the specialist reports for one email. Synthesize a verdict.

[paste header analyst JSON]
[paste content analyst JSON]
[paste url analyst JSON]
```

Record what you get:

| | Risk | Confidence | Key finding |
|---|---|---|---|
| Header Analyst | | | |
| Content Analyst | | | |
| URL Analyst | | | |
| **Supervisor verdict** | | | |

Ground truth for EMAIL-006 is `phishing`, attack type `bec`.

## Step 4: Time yourself

Now the measurement that matters. Run **two more emails** through the full pipeline, pick
one you expect to be easy and one ambiguous, and time it.

| | Minutes | Copy-paste steps | Mistakes made |
|---|---|---|---|
| Email 2 | | | |
| Email 3 | | | |

Then extrapolate:

- Time per email: **______**
- Time for a 50-email queue: **______**
- Time for one shift's inbound at your org: **______**

**You are the bottleneck and the failure mode.** You lost information at every hand-off,
because you pasted the JSON and not the reasoning behind it. You may have pasted the wrong
thing once. You cannot run the three specialists at the same time, so the wait is the sum of
all three instead of the longest one. Nothing recorded any of it.

Those four jobs are what a multi-agent framework does for you: passing messages, running
agents in parallel, holding state, and keeping a record. **Automating the supervisor is the
product.** You cannot do it here, and you now know what you would be buying.

## Step 5: Prove the shortcut is a shortcut

Go back to your original single `Phishing Triage Analyst` and ask:

```text
Analyze EMAIL-006 by acting as three separate specialists in sequence -- a header
analyst, a content analyst, and a URL analyst -- then synthesize their findings
as a supervisor. Show each specialist's report.
```

You get something close to Step 3's output in about eight seconds, with no copy-pasting. So
why did we do it the slow way?

Compare the two carefully:

| | Real team (Steps 1–3) | Role-play (Step 5) |
|---|---|---|
| Did specialists see each other's findings? | No (separate projects) | Yes, one context |
| Could one specialist's framing bias another? | No | Yes, and it does |
| Was disagreement genuine? | Yes | It's one model arguing with itself |
| Could you give one specialist different tools? | Yes | No |
| Time | Minutes | Seconds |

Check whether the role-play version produced **real disagreement**. Usually it does not. The
"specialists" agree with each other because they are the same model in the same context, and
it had already decided what it thought. Your separate team disagrees more often, and that
disagreement is useful information.

**When is the shortcut fine?** When you want the model to follow a checklist and you do not
need the parts to be independent. That covers most cases. Just do not call it a multi-agent
system in an architecture review.

---

## Checkpoint

- [ ] Three specialist projects exist with non-overlapping instructions
- [ ] A supervisor project exists that never analyzes email itself
- [ ] I ran at least one email through the full pipeline
- [ ] I timed it and extrapolated to a real queue
- [ ] I ran the role-play version and compared them
- [ ] I can explain what the role-play version is missing

## Think about it

1. Your specialists were told to stay in their lane. Did they? What does that tell you about
   how firm the boundaries in your design really are?
2. If you could automate one part of what you just did by hand, which would it be? Is that
   the part with the most value, or just the most tedium?
3. A team of agents multiplies every problem from Labs 1 to 4. Answers vary more, more rules
   get skipped, there are more ways in for an injected instruction, and the record of what
   happened is spread across four agents. What would you need to see before running this
   without supervision?

**Next:** [The wrap](../WRAP.md), the honest ledger.

---

### Optional, if you have time and a terminal

[Bonus: Build your own tool](Bonus_Build_Your_Own_Tool.md), run a local MCP server and give
an agent security tools you control. Not required, and it needs the Claude desktop app or a
tunnel. Take it home.
