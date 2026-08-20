<img src="../assets/img/GTK_Logo_Social_Icon.jpg" width="175" align="right" />

# Lab 3: Tools and Routing

**Estimated time: 25 minutes**
_UI steps verified: **2026-08-19**, Claude (web, Max) and ChatGPT (web, Free)._

## Learning objectives

- Understand what a "tool" is and who actually runs it
- Use code execution to get deterministic answers out of a non-deterministic system
- Express branching logic as instructions, and route work by risk
- **Measure whether your routing rules are actually obeyed**
- Understand the difference between a rule and a guarantee

## What you'll build

Lab 1's agent could only reason from the email text. Now it gathers evidence:

```
    email ──► [ agent ] ──► needs evidence? ──► [ tool ] ──┐
                  ▲                                        │
                  └────────── result ──────────────────────┘
                  │
                  └──► enough evidence ──► verdict
```

That loop (reason, act, observe, repeat) is what makes an agent an agent.

---

## Concept: the model does not run the tool

Almost everyone gets this wrong at first, so be precise about it.

When an agent "uses a tool," the language model does **not** execute anything. It emits a
structured request: *"I would like to call `check_url_reputation` with the argument
`https://micros0ft-verify.com/..`"*. Something else, the platform, actually runs it and
hands the result back as new context. The model then reads that result and decides what to
do next.

Three consequences worth holding on to:

1. **The model can ask for the wrong thing.** It chooses the tool and the arguments, and it
   can get either wrong.
2. **The tool's output becomes input.** Whatever the tool returns lands in the model's
   context and shapes everything after it. If a tool can be made to return text an attacker
   wrote, you have a problem. Lab 4 covers this.
3. **The loop can run more than once.** The model may call a tool, read the answer, and call
   another. You are not involved unless you put yourself there. Also Lab 4.

## Concept: tool descriptions are prompts

The agent decides when to call a tool by reading its **description**. That description is not
documentation for you. It is an instruction to the model. A vague description gives you an
agent that calls the tool at the wrong time, or never.

You'll see this concretely in Lab 5, where the tools you connect have descriptions like
*"Use this whenever an email contains a link."* That sentence is doing real work.

---

## Step 1: Enable the built-in tools

Both platforms ship tools you can switch on without writing or hosting anything.

Good news: on both platforms there is **nothing to switch on for code execution.** It runs
automatically when the task calls for it. Web search is a per-conversation toggle, not a
project setting, worth knowing, because it means it can be off without you noticing.

> ### 🅐 ChatGPT
>
> Click **+** in the message box. The menu lists **Web search** along with Create image,
> Maps, Deep research, and any connected apps. Selecting it applies to the current
> conversation.

> ### 🅑 Claude
>
> Click **+** in the message box. **Web search** is at the bottom of the menu with a
> checkmark when it's on (it usually is by default). The same menu holds Skills,
> Connectors, Plugins, and Research.

**Both platforms:** also upload the full `data/emails.json` (all 50 emails) to the agent's
knowledge now. Lab 1 used the 5-email file; from here on we want the whole set.

## Step 2: Watch the loop

Start a new conversation and ask something the agent cannot answer from the email text
alone:

```text
Analyze EMAIL-001. Before giving your verdict, search the web for any public
information about the sender's domain. Show me what you searched for.
```

Watch the interface, not just the answer. You should see the agent announce a search,
run it, and then continue. **That visible step is the "act" half of the loop**, in a
code-based agent this is a message in a trace that you'd have to print to see.

Note what it searched for. Was it the right query? Students frequently find the agent
searches for the *lookalike* domain and reports "no results," which is itself a finding but
not the one it was asked for.

> **Reality check.** `micros0ft-verify.com` is fictional. Web search will find nothing, and
> a well-behaved agent should say so rather than inventing a reputation report. If yours
> produces confident detail about a domain that doesn't exist, you've just watched a
> hallucination in a security workflow. Write down what it said.

## Step 3: Make it count something

Now ask a question with exactly one correct answer:

```text
Using the emails.json knowledge file, give me the exact count of emails for each
ground_truth value. Answer with just the three numbers.
```

Note the answer. Then ask for the same thing again, forcing the code path:

```text
Now answer that same question by writing and running code over the file.
Show me the code and the output.
```

**Both platforms can read your uploaded file directly from code**, no re-attaching needed.
The file appears on a virtual filesystem, at a different path on each platform:

| Platform | Path to your uploaded file |
|---|---|
| ChatGPT | `/mnt/data/emails.json` |
| Claude | `/mnt/project/emails.json` |

You don't need to memorize these, the agent works it out. But if it ever claims it can't
find the file, telling it the path is the fastest fix.

Record both:

| Method | Answer | Correct? |
|---|---|---|
| Reasoning over the file | | |
| Running code over the file | | |

**The ground truth is 25 `phishing`, 22 `legitimate`, 3 `suspicious`.**

If your agent reported two categories, it didn't miscount, it assumed a binary problem
and never checked. That's a more dangerous failure than being off by one, and reasoning
over the file will not reliably catch it. Code will.

## Step 4: The determinism lesson

If both answers were right, run Step 3's first prompt twice more before you dismiss this.
Counting 50 records by reading them is exactly the kind of task a language model does
*approximately*, and the three-way split makes it worse, the rare class is the easiest to
miss. The code path is exact, every time, and it shows its work.

This is the most portable lesson in the workshop, and it holds no matter which platform
you're on:

> **Anything with a single correct answer should be computed, not reasoned.**
> Use the model for judgment. Use code for arithmetic, counting, parsing, and lookups.

A well-built agent pushes as much work as it can into tools that cannot be wrong, and saves
the model for the parts that need judgment. "Is this email phishing?" needs a model. "How
many did we flag?" does not.

## Step 5: Require the tools

Add this to your agent's instructions, after the rules from Lab 1:

```text
Tool use requirements:
- Before assigning a verdict to any email containing URLs, you must investigate
  those URLs rather than judging them from their text alone.
- For any question involving counts, totals, percentages, or comparisons across
  multiple emails, you must write and run code. Never compute these by reasoning.
- State which tools you used in an "evidence" field added to your JSON output.
```

Re-run Step 3's first prompt. Does it use code now, without being told to?

Record the answer, because Lab 3 is entirely about that question: **when you write a rule
in the instructions, how often is it actually followed?**


> **Back to the sample data for this lab.** Lab 2 showed you how messy a real inbox is,
> which is exactly why we measure on `emails.json` instead. Ground-truth labels are the only
> reason the numbers below mean anything. Real mail for realism, sample data for measurement.

## Concept: routing is capacity management

A SOC that investigates every email to the same depth is a SOC that investigates nothing
in time. Tiering exists because analyst attention and API budget are finite.

The distribution matters as much as the accuracy. If 80% of mail routes to HIGH, your deep
pipeline is the bottleneck and you've gained nothing. If 2% does, you're missing threats.
For this dataset a healthy split is roughly 25–35% HIGH, 20–30% MEDIUM, and the rest LOW.

## Concept: a rule is not a guarantee

Here is the single most important idea in this workshop.

In a code-based agent, routing is a **graph edge**. The framework evaluates a function,
gets back the string `"deep_investigation"`, and execution goes there. It cannot go
anywhere else. The routing is a property of the program.

In a GUI agent, routing is a **sentence in the instructions**. The model reads "if risk is
high, run all three checks" and *usually* complies. Compliance is a property of the model's
behavior on that particular run, with that particular input.

| | Code agent | GUI agent |
|---|---|---|
| Routing is | a graph edge | an instruction |
| Enforced by | the framework | the model's cooperation |
| Failure mode | crash, or wrong branch, visible | silently skipped step (invisible) |
| How you verify | unit test the routing function | run it many times and count |

You cannot unit-test a sentence. You can only measure how often it holds, which is what you
are about to do.

---

## Step 6: Add routing rules

Append to your agent's instructions:

```text
Triage tiering:

First assign a risk level to every email, before any investigation:
- HIGH: authentication failures, lookalike or unknown sender domains, credential
  requests, payment or wire instructions, or urgency pressure.
- MEDIUM: some concerning signals but also legitimate indicators; unfamiliar
  sender with clean authentication.
- LOW: known-good sender, authentication passes, routine content, no links or
  only links to well-known domains.

Then investigate according to that level, and do not skip steps:
- HIGH: check the sender reputation, every URL, and the authentication headers.
- MEDIUM: check the authentication headers only.
- LOW: no investigation. Return the verdict directly.

Add these fields to your JSON output:
  "risk_level": "<high | medium | low>",
  "checks_performed": ["<name of each check you actually ran>"]
```

Note that `checks_performed` asks the agent to report on its own compliance. Hold that
thought.

## Step 7: Run the batch

```text
Triage all 50 emails from emails.json. Return a JSON array with one object per email.
Use code to assemble and validate the array before returning it.
```

<!-- VERIFY: 50 emails may exceed a single response on either platform. If it truncates,
     the fallback is batches of 10, confirm which is needed and fix the prompt here. -->

## Step 8: Measure the distribution

```text
From the results, produce a table of how many emails fell into each risk_level,
and within each level, how many were phishing, suspicious, and legitimate
according to ground_truth. Compute this with code.
```

| Risk level | Count | % of total | Phishing | Suspicious | Legitimate |
|---|---|---|---|---|---|
| HIGH | | | | | |
| MEDIUM | | | | | |
| LOW | | | | | |

**The question that matters: how many `phishing` emails landed in LOW?** Those are the ones
your agent decided weren't worth looking at. In production, nobody would ever review them.
A false negative in the LOW tier is invisible in a way that a wrong verdict is not.

## Step 9: Measure compliance

Now audit the rules themselves:

```text
Using code, check every result in the array against these rules:
1. Every HIGH-risk email must have at least 3 entries in checks_performed.
2. Every MEDIUM-risk email must have exactly 1 (the authentication check).
3. Every LOW-risk email must have an empty checks_performed.
Report every row that violates its rule, with the email id and what it did instead.
```

| Rule | Violations | Rate |
|---|---|---|
| HIGH runs all three checks | | |
| MEDIUM runs auth only | | |
| LOW runs nothing | | |

Most rooms find violations somewhere between 5% and 20%. Two things to sit with:

**First, you are trusting the agent's self-report.** `checks_performed` is a field the
model wrote about its own behavior. A model that skipped a check may also report having
run it. The only trustworthy compliance record is one produced by the thing that actually
executes the tools, and in a GUI you don't own that layer. Tool-approval prompts from a connector give you a
better one, because the platform writes them rather than the model.

**Second, better prompting will not fix this.** Clearer instructions, stronger wording, and
examples all push the violation rate down. None of them reach zero, because nothing in the
system enforces the rule. If your requirement is "this check runs every time", a GUI agent
cannot meet it, and no amount of prompt work will change that.

## Step 10: Try to fix it anyway

Pick your worst-performing rule and rewrite it to be more forceful, put it first, add an
example, state a consequence. Re-run Steps 2–4.

| | Violation rate before | after |
|---|---|---|
| Worst rule | | |

Did it improve? Did it hold across the whole batch? Would you sign off on this number for
a control that a regulator asks about?

---

## Checkpoint

- [ ] Routing rules are in my instructions and produce a `risk_level`
- [ ] All 50 emails are triaged
- [ ] I have the distribution across the three tiers
- [ ] I know how many phishing emails landed in LOW
- [ ] I have measured the compliance violation rate for each rule
- [ ] I tried to improve the worst rule and recorded whether it worked


---

## Checkpoint

- [ ] I have counting results from both the reasoning path and the code path
- [ ] My instructions require tool use for anything countable
- [ ] Routing rules produce a `risk_level` on every email
- [ ] All 50 emails are triaged and I have the tier distribution
- [ ] I know how many phishing emails landed in LOW
- [ ] I have measured the compliance violation rate for each rule
- [ ] I tried to improve the worst rule and recorded whether it worked

## Think about it

1. Your LOW tier skips investigation entirely. What's the cost of one phishing email landing
   there, and who absorbs it?
2. If the violation rate is 8%, is this agent deployable? What would have to be true?
3. You measured compliance by asking the agent to audit itself. Design a way to measure it
   that doesn't rely on the agent's honesty. Can you do it inside the GUI?
4. Which parts of your triage workflow have exactly one correct answer? Are any of them
   currently left to the model?

**Next:** [Lab 4, Injection](Lab_4_Injection.md), where someone else writes a message
designed to be read by your agent.
