# Video script: RQ1 for Kundi and Sanaa

About 7 minutes. Speak slowly. **[Screen]** says what to show; the rest is what you say.
Only numbers we have already verified are used. No results yet, because we have not computed them.

---

## 1. Hello (20 seconds)

**[Screen]** `README.md` at the top.

> Hi Kundi, hi Sanaa. This is a short walkthrough of Research Question 1 for the AgentVerify paper:
> why we ask it, how we are answering it, and where we are. At the end I have two small requests.

---

## 2. The problem, with a bridge (1 minute)

**[Screen]** Nothing technical. You can show a simple drawing: two islands, one bridge.

> Imagine you hire a builder to build a bridge to Island A.
> The builder builds a beautiful, strong bridge, with no cracks, and the inspector's alarms stay silent.
> But the bridge goes to Island B.
>
> Nothing is broken. The only way to see the failure is to read the contract, which said Island A.
>
> Coding agents do the same thing. In one real run, the task said: "use the Qwen2.5 tokenizer".
> The agent used Qwen2. The code ran, no errors, a clean number came out, and it was the wrong number.
>
> Most monitors for coding agents wait for an alarm: an error, a crash, a failing test.
> If requirement failures do not set off alarms, those monitors will never see them.

---

## 3. Our question (30 seconds)

**[Screen]** `docs/plan.md`, the research question.

> So RQ1 asks: do requirement-related failures differ from other failures in three things:
> when the mistake starts, how long the agent could still fix it, and how often the failure stays silent,
> meaning no alarm ever goes off.

---

## 4. The data (45 seconds)

**[Screen]** `data/raw/faap/SOURCE.md`.

> We use the released data of "Failure as a Process", the paper Kundi recommended.
> It has 1,184 failed runs of coding agents on Terminal-Bench tasks.
> For every failed run, FaaP already marked three moments, like a flight recorder:
> the step where the mistake happens, the step after which the run can no longer be saved,
> and the first step where something visibly goes wrong, or "never", which means silent.
>
> So the measurements already exist. What we still need is the other half:
> which failures are really about the requirement.

---

## 5. Why we cannot just use FaaP's labels (1 minute)

**[Screen]** `docs/decision_log.md`, the entry about the group definition.

> FaaP labels each failure twice, and the two labels often disagree.
> 176 runs are labeled "specification neglect". But another 135 runs are labeled as a
> "specification violation" in a second field, while the first field calls them something else, like a wrong assumption.
> The Qwen2 run is one of those: FaaP files it as a "false premise", not as specification neglect.
>
> And some runs FaaP calls specification neglect are about things the specification never says.
> In one task, FaaP labels 17 runs as specification neglect, and most of them are about not writing to /app/solution.txt.
> But the task text never mentions that file. Only the hidden test expects it.
>
> It is like comparing two groups of patients when the diagnosis itself is unreliable.
> So before comparing anything, we redo the diagnosis ourselves, against the actual task text.

---

## 6. How we decide, one run at a time (1 minute 30 seconds)

**[Screen]** `docs/labeling_guide.md`, the short version. Then one example row, for instance the Qwen2.5 run.

> We take the 311 runs where FaaP's labels point at the requirement, plus 100 random other failures
> to estimate how many requirement failures FaaP's labels miss.
>
> For each run, we read the original task text and FaaP's description of what went wrong, and ask one question:
> did the agent stop doing something the task text clearly asked for?
> Yes is ANCHORED. No, it tried but failed for another reason, is NOT. Cannot tell is UNCLEAR.
>
> When it is hard to decide, we use one tie-breaker, and here the bridge helps again:
> if the builder's own plan had worked perfectly, would the bridge reach Island A?
> If the plan was to build to Island B, that is a requirement failure: ANCHORED.
> If the plan was right but the concrete was bad, that is a different failure: NOT.
>
> Only the task text counts. If the missed thing is written only in a hidden test, we label it NOT and mark it "implicit".
>
> Every ANCHORED label must quote the exact words from the task and the exact words from the evidence,
> so anyone can open the file and check it.
>
> To be transparent: Claude drafted a suggestion for every run, twice, independently.
> I go through every run and make the decision myself.

---

## 7. How we make sure it is trustworthy (1 minute)

**[Screen]** `docs/plan.md`, the section "How reliable are the labels", then "How we compare the groups".

> Kundi, this is where we need you. You label 50 random runs on your own, without seeing my labels or the drafts.
> Then we measure how often we agree. If agreement is too low, we fix the guide and relabel, before looking at any result.
>
> Then we freeze the plan in git, so we cannot change the rules after seeing the numbers.
>
> The comparison itself is simple. One table: for each group, the typical start step, the typical fix window,
> and the percentage of silent failures.
> To see if a gap is real, we redraw the set of tasks 10,000 times and check that the gap does not disappear.
> And we run four checks that answer the obvious doubts:
> is it just harder tasks, is it just one or two tasks, is it just one model, and does it depend on our labels.
> We only claim a difference if all of them agree.

---

## 8. Why it matters (30 seconds)

**[Screen]** Back to the bridge drawing.

> An early look at FaaP's own labels already hints at it: runs labeled specification neglect end silent
> in 44% of cases, versus 28% of all failures. That is why we ask the question.
> If our cleaner definition confirms it, the message is simple:
> to catch these failures, a monitor has to read the requirement, like reading the contract,
> instead of waiting for an alarm that never comes.

---

## 9. What comes next and two requests (40 seconds)

**[Screen]** `README.md`, the steps table.

> After FaaP, we repeat the same study on a second dataset, Nebius, with GitHub issues instead of terminal tasks.
> There we create our own labels, and silence is measured by a simple rule on the raw run, so anyone can recheck it.
>
> Two requests.
> Kundi: could you label the 50 runs in `kundi_blind_50.csv`, following the labeling guide? It takes about an hour.
> Kundi and Sanaa: please tell me if you disagree with the two main rules: the tie-breaker, and "only the task text counts".
>
> Thank you.
