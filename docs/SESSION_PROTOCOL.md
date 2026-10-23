# Session protocol

## Scope and precedence
The user's current explicit request overrides the default task selection. Read-only
reviews do not invent a production task; maintenance requests are one maintenance
task. `brief/BRIEF.md` is immutable. If the brief and any derivative disagree,
stop, report and correct the derivative; never silently reinterpret the brief.
Among implementation records: `production/timeline.json` defines frame accounting,
`production/state.json` defines task dependencies/status, `production/assets.json`
defines exact asset/lock identities; Markdown describes them, not an alternative state.
A contradiction anywhere is a stop. Do not weaken tests to make an output pass.

## Mandatory context (every production session)
1. Fetch current remote; fast-forward only on a clean tree. Record starting commit.
   Read README, this protocol, PIPELINE, QUALITY_GATE, CONTINUITY, MEDIA_CONTRACT,
   `segments/COMMON.md`, state/asset/timeline JSON, and the last three session logs.
2. Read the brief in full before the first production action in each fresh session,
   both bibles and the task's specific specs. Inspect the actual approved reference
   images and master motion samples, not just their prose descriptions. Load adjacent
   segment review/seam reports. Inputs in QUEUE are additional, never exhaustive.
3. Run `python3 tools/validate.py`. Reconcile stale outputs before spending.
4. Resume the single `in_progress` task first. An unknown charged request is recovered
   before any new submit. Otherwise select the first `ready` task with all dependencies
   done. Run `python3 tools/validate.py --task ID`; a ready label alone is insufficient.
   A task explicitly assigned by the user still cannot bypass asset/quality dependencies.

## Budget and task ownership
- **50 OLU per session all-in.** Reserve at least 10 for review, durable handoff and commit;
  use current ledger readings plus outstanding job liability, not vendor USD as OLUs.
  Record session start, baseline, last measured usage/time, estimates, actual charges.
  Keep the reported end total labelled a snapshot; later closing-message usage may accrue.
- No reliable OLU estimate/upper bound? `needs_user` BEFORE a paid submit. No price
  discovery by uncontrolled charged trials. Never infer a universal USD/OLU conversion.
- Quality has no deadline discount. If the budget cannot buy/review another strong attempt,
  preserve candidates and failures, set `in_progress` or `needs_user`, and continue in
  another session. Never accept the best of several bad attempts.
- One task per session. Candidate production and independent review are separate tasks.
  A multi-attempt task may span any number of sessions; generation alone never implies done.
- Production sessions are **serialized**. Push an `in_progress` claim with bot URL,
  starting commit and next action BEFORE any submit or lock change. A conflicting remote
  claim stops work. Do not force-push, overwrite concurrent changes, or rebase a paid job
  onto different inputs. Parallel production requires an explicit user-approved plan.

## Durable submit/recovery journal
Create `production/jobs/<unique-id>.json` BEFORE submit: task/session, input commit and
hashes, fully resolved positive/negative prompts, exact request body, model endpoint/
version availability, schema/defaults snapshot, reference roles/order, cost estimate,
reserve, UTC submit time, status `prepared`. No credentials or signed upload URLs in git.
Disable automatic prompt expansion, multi-shot, audio, random seed defaults where supported;
record unsupported controls and explicit values for ALL supported quality-affecting fields.
Seed equality does not guarantee identity or deterministic output.
Immediately record/push request ID and `submitted` state; poll to terminal, saving terminal
response, output hash, download location, actual charge/refund and review pointer.
If a response is lost, the prepared record becomes `unknown`, blocks further submits,
and is reconciled through provider history/support/user. **Never resubmit blindly.**
If a session must end while a job runs, persist request ID + polling instructions, keep
the task `in_progress`, and make the next session poll FIRST; do not launch another job.
Observe `failed`/`nsfw`/`canceled` via polling for refund processing. Unknown is not failed.

## Candidate, review and completion
- Follow QUALITY_GATE. Inspect all playback, targeted dense frame evidence, actual
  endpoints and seam loops. A contact sheet or one-frame-per-second sample is not QA.
- Use immutable attempt paths, never overwrite an accepted file. Register every input
  and output hash, model lock and dependency lineage in assets.json. Keep rejection
  evidence and reason codes. No vendor URL is a durable output.
- A generation task is done only when its complete candidate package is committed,
  validated and handed to its review task. Only a different fresh-session reviewer
  may accept; visual masters and final delivery additionally require explicit user
  approval recorded with a source link. Review sessions may not generate replacements.
- Acceptance stages are `candidate`, `accepted`, `rejected`, `stale`; a queue task `done`
  is NOT proof of asset acceptance. Unknown, missing evidence, or inconclusive = hold.
- Lock changes invalidate descendants transitively. Do not change an upstream asset to
  make one seam fit without revisiting every downstream consumer (see CONTINUITY).

## Stop and handoff
1. Update assets/reviews/jobs, state.json, regenerate QUEUE with
   `python3 tools/render_queue.py`, add a newest-first log entry.
2. Log task, bot URL, starting commit, exact inputs/outputs/reviews, cost snapshot,
   failed criteria, unresolved jobs/decisions, and ONE precise next action.
3. Run validator, tests and `git diff --check`; verify the brief hash unchanged.
4. Commit only this task. Push through the authenticated GitHub integration and verify
   remote contains the commit. Never claim "committed to repo" for local-only work.
   If push fails, export a patch plus complete handoff, report unpublished, and stop.
5. Stop. Report outcome, cost snapshot, next task/blocker. Do not take another task.

Commit example: `[T10] B candidate: motion seam review pending Q10`
Generation is not acceptance; published scaffolding is not a finished film.
