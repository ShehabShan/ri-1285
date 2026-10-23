# Segment B — Take 1 backward tracking, five steps (0:04–0:09)

| Field | Value |
|---|---|
| Status | blocked (needs T02, K2, K3) |
| Part | Take 1, unbroken river take |
| Timeline | 0:04.000–0:09.000 (120 frames at 24 fps) |
| Start keyframe | K2 |
| End keyframe | K3 |
| Before | A (invisible join) |
| After | C (invisible join) |
| Model | follow the river lock in `docs/MODELS.md` |

## Beat (from the brief)

The camera holds in front of him in a backward tracking move at his walking pace, slightly low, framing him from head to waterline. Five heavy steps against the current, with water erupting around his shins on each one. Soaked hems trail in the flow. Hair and outer robe stream behind him. Rim light on his hair, face edge and white-covered shoulders. Droplets glint on his skin.

## Generation prompt

[STYLE] [CHARACTER] [RIVER]
One continuous backward tracking shot at his walking pace, slightly low, framing Fang Yuan from head to waterline. The distance and framing stay constant. He takes five heavy, deliberate steps upstream against the current. On each step his submerged foot plants, his weight shifts through his torso, and water erupts around his shins. Soaked robe hems trail in the flow. His long wet hair and the charcoal outer robe stream behind him. Cool-white rim light on his hair, face edge and white-covered shoulders. Droplets glint on his pale skin. His gaze stays fixed forward.

## Segment-specific negatives

camera orbit, camera cut to side view, zoom, changing distance, fast walk

## Segment-specific checklist

- [ ] Exactly five planted heavy steps in B, each with a visible water burst; record their frame times.
- [ ] The framing stays head to waterline throughout.
- [ ] The rim light is constant on hair, face edge and shoulders.

## Cross-session contract (mandatory)
Queue status is in `production/state.json`; the header is descriptive, not authorization.
Read the whole brief, COMMON, CONTINUITY, QUALITY_GATE and MEDIA_CONTRACT, inspect actual
masters and the approved model/recipe, and run `--task T10`.
Candidate sample count: **121** at 24 fps; retained final count:
**120**, range **[96, 216)**.
Last sample is boundary-only and discarded from THIS clip at assembly.
Retiming uses endpoint-to-endpoint span, not nominal container duration.
Store native and conformed attempts, payloads/locks/hashes, full-frame review and timed
beat evidence. T10 produces candidates only; Q10 independently accepts/rejects.
Inspect approved predecessor A tail and review a +/-12-frame seam loop; static endpoint matching is insufficient.

## Attempts

| # | Date | Session | Model + version | Settings | Retime | Cost (OLU) | Verdict | Notes |
|---|---|---|---|---|---|---|---|---|
