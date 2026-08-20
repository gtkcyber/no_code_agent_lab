<img src="assets/img/GTK_Logo_Social_Icon.jpg" width="175" align="right" />

# The Wrap: An Honest Ledger

**15 minutes.** Instructor-led discussion. Don't skip this, it's the part students take
back to work.

---

## What you built

In roughly two hours, with no code, you built an agent that:

- classifies email against a structured schema
- reads a real mailbox over a live connector
- gathers evidence with tools before deciding
- routes work to different depths based on risk
- escalates ambiguous cases to a human
- and then you split it into a four-agent team

The Python version of this same system is five worksheets and the better part of a day.
That is a real result and you should not be sheepish about it.

## What it cost

Every lab produced a number. Put them together:

| From | Measurement | Yours |
|---|---|---|
| Lab 1 | Accuracy on 5 emails | |
| Lab 1 | What changed between two identical runs | |
| Lab 2 | Failure modes on real mail that sample data never showed | |
| Lab 3 | Correct count by reasoning vs. by code | |
| Lab 3 | Phishing emails routed to LOW | |
| Lab 3 | Routing rule violation rate | |
| Lab 4 | Attacks that fooled the agent (before / after defense) | |
| Lab 4 | Attacks the agent *flagged* rather than merely survived | |
| Lab 5 | Minutes per email as the human supervisor | |

Nobody in the room gets a clean sheet. That is why you measure.

## The ledger

**Where the GUI wins**

- **Time to a working agent.** Twenty minutes against a day.
- **Who can build one.** Anyone who can write a clear procedure. This matters most. The
  bottleneck in most SOCs is not AI expertise. It is that the people with the domain
  knowledge do not write Python.
- **Keeping a human in the loop.** Built in, against checkpointers and resume logic.
- **Iteration speed.** Edit a sentence, re-run. No deploy.
- **Tool integration.** Connecting a real mailbox took four clicks and no code.

**What the GUI costs you**

- **No enforcement.** Every rule is a request. Lab 3 measured the gap.
- **No version control.** You cannot diff today's instructions against last week's, or roll
  back, or tell who changed what and why.
- **No tests.** There is no way to assert that a change didn't break something. You edit a
  prompt and hope.
- **No batch evaluation.** You measured by hand. That doesn't scale, and it doesn't run
  automatically when something changes.
- **Weak audit.** The agent's account of its own behavior isn't trustworthy (Lab 3).
- **Nothing coordinates the agents.** In Lab 5 the specialists only reached each other
  because you carried the messages by hand.
- **The same input can give you a different answer.** Lab 1 showed it moving between runs.
- **Governance.** Where does the data go, which model version answered, can you reproduce a
  decision from six months ago for an auditor? Usually: unknown, unknown, no.

## When to use which

This is the takeaway worth writing down.

**Use the GUI when:**

- you're exploring whether an agent helps at all, before committing engineering
- a human reviews every output anyway
- the cost of a wrong answer is a wasted minute, not an incident
- the people with the domain knowledge are the ones who need to build it
- you need something working this afternoon

**Move to code when:**

- a step must run every time, not usually
- you need to evaluate against a labeled set on every change
- decisions need to be reproducible or auditable
- volume makes per-item human review impossible
- it's in the path of an automated action, blocking, quarantining, ticketing
- more than one person maintains it

**The pattern that works:** prototype in the GUI, measure it, then port the parts that need
guarantees. The GUI agent you built today is a *specification*
,  you now know exactly what the system should do, which is the expensive part of building
the coded version.

## The security point

You spent Lab 4 attacking your own agent, with a real email, delivered to a real inbox,
through real infrastructure, and the defense you added helped but didn't hold.

Carry three things out of that:

1. **Prompt injection is structural.** Your instructions and the attacker's arrive in the
   same channel with no boundary between them. Mitigate, don't expect to eliminate.
2. **The attack surface is bigger than the prompt.** One attack went after your routing, not
   your verdict. Another hid in a display name. Anything the model reads is an input, and
   anything it decides is a target.
3. **Don't let the model be the only control.** Deterministic checks that run regardless of
   what the model concluded are the only part of the system an attacker can't talk out of.
   Those belong in code.

And remember how low the bar was: **anyone who knows the address can put content in front of
your agent.** You didn't need to compromise anything. You sent an email.

If you deploy an agent that reads attacker-controlled content, and email triage is exactly
that, assume it will eventually be steered, and design so that being steered isn't
catastrophic. The question is not whether it happens; it's what the agent is permitted to do
when it does.

## What Lab 5 was really about

You built a working multi-agent system. Separate contexts, independent specialists, real
hand-offs. The only missing piece was that **you** carried the messages.

That gap is the lesson. Everything a multi-agent framework sells you is the work you did by
hand: passing messages between agents, running them at the same time, holding state, and
keeping a record of what happened. You now know the shape of that product and roughly what it
is worth, which puts you ahead of most people evaluating one.

You also showed that the shortcut is not the same thing. One agent playing three parts
produces near-identical output and has none of the properties that made the real version
worth building. Carry that distinction into any vendor conversation.

Note as well that a team of agents multiplies every problem in the list above. Answers vary
more, more rules get skipped, there are more ways in for an injected instruction, and the
record of what happened is spread across four agents. Worth understanding, and worth being
slow to deploy.

## Where to go from here

- **Revoke your Gmail grant** if you're done with it. Google account → third-party access.
  Do this before you forget the burner exists.
- **Keep going in the GUI:** build an agent for a workflow you own. Measure it the
  way you measured today, accuracy, variance, and rule compliance, before you trust it.
- **Try the bonus lab:** build your own MCP tool server and give an agent capabilities you
  wrote. It's the natural next step after connecting someone else's.
- **Move to code:** GTK Cyber's **AI Cyber Bootcamp** builds this same phishing triage
  system in LangGraph, with enforced routing, real checkpointing, and multi-agent
  supervision.
- **Go on the offensive:** GTK Cyber's **Attacking AI** course takes Lab 4 considerably
  further.

## Final discussion

1. What's one workflow you own that you'd build in a GUI tomorrow?
2. What's one where you now think you shouldn't?
3. What number would you need to see before putting an agent in the path of an automated
   block?
