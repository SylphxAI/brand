# Name test kit — `Sylphx` umbrella + AI family (draft)

**Status:** DRAFT proposal. Not adopted naming law and not legal advice. This
kit measures human responses; it does not clear a trademark.

**Companion:** [`name-clearance-desk-research.md`](./name-clearance-desk-research.md)
defines why these tests exist and which results would change the naming
decision. Run this kit before or while the
[attorney brief](./trademark-clearance-brief-template.md) is being answered.

## What this measures

1. Can a stranger **spell** `Sylphx` after hearing it once?
2. Can a stranger, given a 10-second glance, **place** `Models` vs `Agents` vs
   `Cloud` vs `Data`?
3. Do `SylphAI` and `Sylphix` read as **us**, or as separate companies?

## Setup (3 minutes)

- **Participants:** 5 people who have not seen the brand (note anyone who
  has). If used as a quantitative gate, use 20–30 online with the same script.
- **Materials:** the three cards in the appendix; one record sheet per
  participant; a stopwatch.
- **Rules:** no logos or colours; typed answers for spelling; do not spell the
  name for participants; read the scripts exactly; record answers verbatim.
- **Order:** Test 1 → Test 2 → Test 3, without explaining the brand in
  between.

## Test 1 — Say-and-spell (2 minutes per participant)

Read the script exactly:

> "I'm testing a company name. I'll say it once and you write it down the way
> you think it is spelled. There is no right answer. Ready? **Sylphx.**
> (pause) **Sylphx Limited.**"

Then wait. After they write, ask and log:

1. "How would you say that out loud?"
2. "If you had to find it online, what would you type?"
3. "Without knowing anything else, what do you think the company does?"

**Measure:** first-try spelling (correct/incorrect) and the exact string they
wrote; whether they hesitated or asked for a repeat; the pronunciation they
gave; the first thing they would search.

**Score:** correct = exactly `Sylphx` (case-insensitive). Log near misses
(`Sylph`, `Sylphix`, `Sylphex`, `Sylph X`, `Silfex`, other) separately.

## Test 2 — 10-second recognition (3 minutes per participant)

Hand over **Card B** (one line of names, no descriptions) and say:

> "You have 10 seconds to read this. Then I'll take it away and ask four
> questions."

After 10 seconds, remove the card and ask (in this order, without hints):

1. "Which one would you use to host or deploy an app?"
2. "Which one would you use to call a model through an API?"
3. "Which one would you use to run an agent?"
4. "Which one would you use for a database, cache, or search?"

**Score:** 1 point per correct placement (max 4). Log the wrong pairings —
the important signal is `Models` ↔ `Agents` swaps, not the total alone.

## Test 3 — Confusion probe (1.5 minutes per participant)

Show **Card C** (three names at once) for 5 seconds, then hide it. Ask:

1. "Are these the same company, different companies, or can't tell?"
2. "Which one, if any, is the AI agent company?"
3. "Would it surprise you to learn they are different companies?" (yes/no)

Log each name pairing (`Sylphx`↔`SylphAI`, `Sylphx`↔`Sylphix`) as
same / different / can't tell, plus the surprise answer.

## Record sheet (copy once per participant)

| Field | Answer |
|---|---|
| Participant ID (P1…) | |
| Seen the brand before? (Y/N) | |
| T1 spelling verbatim | |
| T1 first-try correct? (Y/N) | |
| T1 how they'd search | |
| T2 Q1–Q4 answers | |
| T2 correct count (/4) | |
| T3 Sylphx vs SylphAI (same/different/can't tell) | |
| T3 Sylphx vs Sylphix (same/different/can't tell) | |
| T3 surprise (Y/N) | |
| Notes (hesitation, questions asked) | |

## Scoring and pre-registered thresholds

Compute and report raw counts *and* percentages:

- **Spell rate** = first-try correct ÷ participants. **Revisit naming if
  below ~80%.**
- **Mapping accuracy** = correct placements ÷ (4 × participants). **Revisit
  if below ~75%.**
- **Confusion rate** = participants saying same-or-can't-tell for `SylphAI`
  or `Sylphix` ÷ participants. **Revisit if any participant in a 5-person
  round says "same company", or if more than one says "can't tell".**

For a quantitative read, use n = 20–30 and report the 95% confidence interval
(a simple Wilson interval is enough). Do not treat differences below n = 10 as
conclusive. These thresholds are deliberately conservative; they are a
research proposal, not company law.

## How to interpret the result

| Result | Likely response |
|---|---|
| All three pass | Keep the structure (option A in the desk research) and continue to professional clearance |
| Spell fails, rest pass | Keep the umbrella; consider a spelling/spoken-alias convention or pronunciation note in copy; test again after the fix |
| Mapping fails | The umbrella is fine; fix the *descriptors* (e.g. one-line copy, ordering, domains) so `Models` and `Agents` are unmistakable |
| Confusion probe fails | Escalate to counsel: decide between softening the `Sylphx AI` family label (option B) or adjusting the family name before launch (option C) |
| Two or three fail | Do not launch the family naming unchanged; revisit before public surfaces ship |

## Appendix — card texts

**Card B (recognition; keep these lines and names exactly as written)**

```
sylphx.ai
Sylphx Cloud · Sylphx Models · Sylphx Agents · Sylphx Data
```

**Card C (confusion; one word per line, order shuffled between participants)**

```
Sylphx

SylphAI

Sylphix
```

**Facilitator checklist:** consent to record answers (no audio/video needed) ·
participants have not seen the brand · cards not shown together with logos ·
T1 script read once · T2 exactly 10 seconds · T3 cards removed before
questions · answers logged verbatim · summary posted back with raw counts.
