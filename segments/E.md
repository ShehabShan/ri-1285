# Segment E — Take 2 leg splash to the kindling light (0:18–0:23)

| Field | Value |
|---|---|
| Status | blocked (needs T02, K7, K8) |
| Part | Take 2, unbroken river take |
| Timeline | 0:18.000–0:23.000 (120 frames at 24 fps) |
| Start keyframe | K7 |
| End keyframe | K8 |
| Before | D (hard cut) |
| After | F (invisible join) |
| Model | follow the river lock in `docs/MODELS.md` |

## Beat (from the brief)

- **0:18:** Hard cut back to the river. The take opens on a waterline close-up of his leading lower leg driving against the current. His boot plants unseen beneath the surface; displaced water bursts around his shin toward the lens. Same knee-deep water, same downstream flow, cold palette.
- **0:18–0:20:** Without cutting, the camera tilts and rises up his body, past the soaked robes and white collar, to a frontal close-up of his face: neutral, eyes forward, mouth closed, wet hair, storm sky behind. He has not stopped walking.
- **0:20–0:23:** The camera eases back to a medium shot and drifts around to a frontal three-quarter view, tracking backward with him. A faint pure-white light kindles inside his chest, glowing through his skin and the white inner robe. The river stays violent.

## Generation prompt

[STYLE] [CHARACTER] [RIVER]
One continuous shot. It opens on a waterline close-up of Fang Yuan's leading lower leg driving forward against the current. The boot plants unseen beneath the opaque water, and displaced water bursts around his shin toward the lens. Without cutting, the camera tilts and rises up his body, past the soaked dark robes and the white collar, to a frontal close-up of his neutral face: eyes forward, mouth closed, wet hair, storm sky behind. He keeps walking. The camera then eases back to a medium shot and drifts around to a frontal three-quarter view, tracking backward with him. A faint pure-white light kindles inside his chest, glowing softly through his skin and the white inner robe. The river stays violent at full force.

## Segment-specific negatives

visible boot, visible foot, light outside his body, glowing eyes, glowing object, sunrise, warm light

## Segment-specific checklist

- [ ] The first frame is a waterline close-up with no boot visible.
- [ ] The tilt-up is continuous and reaches a frontal close-up of the face by about 0:20.
- [ ] The face is unchanged from Take 1: neutral, no tears.
- [ ] The light starts faint, inside the chest only, and grows gently.
- [ ] The river is at full force throughout.

## Cross-session contract (mandatory)
Queue status is in `production/state.json`; the header is descriptive, not authorization.
Read the whole brief, COMMON, CONTINUITY, QUALITY_GATE and MEDIA_CONTRACT, inspect actual
masters and the approved model/recipe, and run `--task T13`.
Candidate sample count: **121** at 24 fps; retained final count:
**120**, range **[432, 552)**.
Last sample is boundary-only and discarded from THIS clip at assembly.
Retiming uses endpoint-to-endpoint span, not nominal container duration.
Store native and conformed attempts, payloads/locks/hashes, full-frame review and timed
beat evidence. T13 produces candidates only; Q13 independently accepts/rejects.
Match the approved full-film motion language and visual master; no standalone style reinterpretation.
Face reached by global480 (20s); white chest light only thereafter; K8 remains faint and continues in F. The first plant is at global432.

## Attempts

| # | Date | Session | Model + version | Settings | Retime | Cost (OLU) | Verdict | Notes |
|---|---|---|---|---|---|---|---|---|
