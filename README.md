# ri-1285 — "Perseverance" (30-second anime sequence)

This is the production repo for a 30-second, 16:9, 24 fps anime sequence. Fang Yuan walks upstream through a reverse-flowing river, there is one flashback to a grave, and his body ignites into white light.

The canonical brief is [`brief/BRIEF.md`](brief/BRIEF.md). **When any other file in this repo contradicts the brief, the brief wins.**

The video is built across many short, independent bot sessions. Nothing carries over between sessions except this repo. Every session reads the repo, completes one task, commits the result, and stops.

## Start here (every session)

1. Read [`docs/SESSION_PROTOCOL.md`](docs/SESSION_PROTOCOL.md). It sets the rules, the budget and the commit requirement.
2. Open [`tasks/QUEUE.md`](tasks/QUEUE.md). Take the first task with status `ready` whose dependencies are all `done`.
3. Read only the inputs that task lists. Do the task. Commit the output, update the queue and add a log entry. Stop.

## Kickoff prompt for a fresh session

> Continue the ri-1285 video pipeline in https://github.com/ShehabShan/ri-1285. Follow docs/SESSION_PROTOCOL.md: take the next ready task from tasks/QUEUE.md, stay within the 50 OLU session budget, and commit your output plus a log entry before stopping.

## Layout

| Path | What it holds |
|---|---|
| `brief/BRIEF.md` | The original brief, verbatim. Never edited. |
| `bible/CHARACTER.md` | Locked character designs: present-day and younger self. |
| `bible/WORLD_AND_STYLE.md` | Locked rules for the visual style, river, light and color. |
| `docs/PIPELINE.md` | How the video is built: stages, model policy, seams, assembly, consistency pass. |
| `docs/SESSION_PROTOCOL.md` | Rules every session follows. |
| `docs/MODELS.md` | Model survey and the locked model choices. Created by task T02. |
| `keyframes/KEYFRAMES.md` | Boundary stills shared by adjacent segments. |
| `segments/COMMON.md` | Shared prompt blocks, the shared negative prompt and the shared acceptance checklist. |
| `segments/A.md` … `F.md` | One strict spec per video segment. |
| `tasks/QUEUE.md` | Task queue with dependencies and status. |
| `log/SESSIONS.md` | One entry per session. |
| `media/` | Generated assets: `refs/`, `sheets/`, `keyframes/`, `clips/`, `audio/`, `cuts/`. |

## Timeline

| Seg | Time | Part | Content |
|---|---|---|---|
| A | 0:00–0:04 | Take 1 | Extreme wide, low glide over the water toward him |
| B | 0:04–0:09 | Take 1 | Backward tracking shot, five heavy steps |
| C | 0:09–0:13 | Take 1 | Push-in to an extreme close-up of the eye; a ripple in the iris fills the frame |
| D | 0:13–0:18 | Flashback | Younger self crying at the grave, one slow arc |
| E | 0:18–0:23 | Take 2 | Leg splash close-up, tilt up to his face, ease out to a frontal three-quarter view; the chest light kindles |
| F | 0:23–0:30 | Take 2 | Light grows, rising pull-back to wide, flare, white-out |

The video has exactly two transitions: a ripple dissolve at 0:13 and a hard cut at 0:18. A→B→C and E→F are seamless joins inside unbroken takes.