# Session protocol

Every session follows these rules. They exist so that any fresh session can make real progress without knowing anything beyond what is in this repo.

## Hard rules

1. **Budget: 50 OLU per session, all-in.** This covers the bot's own work *and* generation charges. Higgsfield (and any other PromptQL-brokered generator) bills in OLUs from the vendor's estimate when a submit is accepted. Keep roughly 10 OLU for reading, reviewing and committing. Spend at most about 40 OLU on generation.
2. **Every session commits at least once.** If a task cannot finish, commit partial progress: a failed-attempt record, a revised prompt, or handoff notes. Then set the task to `in_progress` and write what the next session should do.
3. **One task per session**, unless the queue marks tasks as batchable and the budget allows.
4. **Never edit `brief/BRIEF.md`.** Change `bible/` only in a task that is explicitly about the bible, or when the user asks.
5. **Run sessions one at a time** by default. To run sessions in parallel, a session must first commit a claim (status `in_progress` plus its session link) before it generates anything.

## Steps

1. Read `README.md`, this file, `tasks/QUEUE.md` and the last three entries in `log/SESSIONS.md`.
2. Pick the task: the first `ready` task whose dependencies are all `done`.
3. Read the task's listed inputs, and only those. Do not re-read the whole repo.
4. Do the work. Follow the generation rules below.
5. Review every output against the relevant acceptance checklist. Record the verdict in the spec's `Attempts` table.
6. Commit in a single commit: the outputs, the updated spec(s), `tasks/QUEUE.md` (status and next steps), and a new entry at the top of `log/SESSIONS.md`.
7. Stop. Tell the user what was done, what it cost, and which task is next.

## Generation rules

- **Model choice is made at generation time, not hardcoded.** Use the best-quality model that supports the inputs the task needs. See `docs/PIPELINE.md` → Model policy, and `docs/MODELS.md` for locked choices.
- **Check the cost before you submit.** If a single submit would push the session over budget, do not submit. Record the estimate and set the task to `needs_user`.
- **Never retry a submit whose outcome is unknown**, such as a timeout or a dropped connection. It may already have created a charged job. Poll it by request ID. If no ID is available, ask the user.
- **Always poll a submitted request until it reaches a terminal status.** Refunds for `failed`, `nsfw` or `canceled` only happen when a poll observes them.
- **Download outputs immediately and commit them under `media/`.** Vendor URLs expire after about seven days. If a file is over 50 MB, attach it to a GitHub Release and commit the link instead.
- **Record every attempt**, accepted or not: model path and version, key settings, seed if available, cost, verdict and the reason.

## Reviewing a clip

- Extract and inspect at least the first frame, a frame every second, and the last frame.
- Compare the first and last frames with the start and end keyframes.
- Check every item in `segments/COMMON.md` → Acceptance checklist, plus the segment's own checklist.
- A clip is `accepted` only when every item passes. Otherwise it is `rejected`, with the failing items named.

## Commit messages

`[T07] Keyframes K1–K3: accepted K1, K2; K3 rejected (robe on shoulders)`

## Log entry format (newest on top)

```
## Session <n> — <YYYY-MM-DD> — <task id>
- Bot: <link to the PromptQL bot>
- Did: <one or two lines>
- Cost: <OLU, generation vs. own work if known>
- Result: <accepted / partial / blocked>
- Next: <task id and any handoff notes>
```