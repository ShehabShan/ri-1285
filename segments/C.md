# Segment C — Take 1 push-in to the eye (0:09–0:13)

| Field | Value |
|---|---|
| Status | blocked (needs T02, K3, K4) |
| Part | Take 1, unbroken river take |
| Timeline | 0:09.000–0:13.000 (96 frames at 24 fps) |
| Start keyframe | K3 |
| End keyframe | K4 (mandatory; declared ripple_generated or eye_for_post; post route must supply reviewed moving C composite) |
| Before | B (invisible join) |
| After | D (ripple dissolve at 0:13, done at assembly) |
| Model | follow the river lock in `docs/MODELS.md` |

## Beat (from the brief)

- **0:09–0:12:** Still without cutting, the camera keeps tracking backward while slowly pushing in: medium shot → close-up → extreme close-up of his left eye and cheekbone. He keeps walking. Water beads on his skin; a wet strand lies across his cheek. His gaze never moves.
- **0:12–0:13:** The rushing river reflects in his dark iris. A ripple crosses the reflection and spreads outward until it fills the frame. The eye itself never glows.

## Generation prompt

[STYLE] [CHARACTER] [RIVER]
One continuous shot. The camera keeps tracking backward with Fang Yuan as he walks, while slowly pushing in from a medium shot to a close-up, and then to an extreme close-up of his left eye and cheekbone. His body keeps the gentle rhythm of walking. Water beads on his pale skin; a wet black strand lies across his cheek. Shallow depth of field, gentle focus pull to the eye. His gaze never moves. At the end, the rushing river is reflected in his dark iris, and a ripple crosses the reflection and spreads outward until it fills the frame. The eye does not glow.

## Segment-specific negatives

glowing eye, iris color change, eye closing, blinking at the end, sudden zoom, cut to close-up

## Segment-specific checklist

- [ ] The push-in is continuous, with no zoom jump.
- [ ] Walking motion is still readable in the close-ups (subtle bob).
- [ ] The extreme close-up is of the **left** eye and cheekbone.
- [ ] The eye never glows or changes color.
- [ ] If the ripple is generated: it starts in the reflection and fills the frame.

## Cross-session contract (mandatory)
Queue status is in `production/state.json`; the header is descriptive, not authorization.
Read the whole brief, COMMON, CONTINUITY, QUALITY_GATE and MEDIA_CONTRACT, inspect actual
masters and the approved model/recipe, and run `--task T11`.
Candidate sample count: **96** at 24 fps; retained final count:
**96**, range **[216, 312)**.
Both endpoint samples are displayed; no endpoint may be trimmed.
Retiming uses endpoint-to-endpoint span, not nominal container duration.
Store native and conformed attempts, payloads/locks/hashes, full-frame review and timed
beat evidence. T11 produces candidates only; Q11 independently accepts/rejects.
Inspect approved predecessor B tail and review a +/-12-frame seam loop; static endpoint matching is insufficient.
If using eye_for_post, composite the tracked reflection ripple onto moving C during T11; no frozen-frame shortcut and no unresolved ripple promise at acceptance.

## Attempts

| # | Date | Session | Model + version | Settings | Retime | Cost (OLU) | Verdict | Notes |
|---|---|---|---|---|---|---|---|---|
