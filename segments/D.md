# Segment D — Flashback: the grave (0:13–0:18)

| Field | Value |
|---|---|
| Status | blocked (needs T02, T04, K5, K6) |
| Part | Flashback |
| Timeline | 0:13.000–0:18.000 (120 frames at 24 fps) |
| Start keyframe | K5 |
| End keyframe | K6 |
| Before | C (ripple dissolve, done at assembly) |
| After | E (hard cut) |
| Model | may differ from the river lock if quality is clearly better; record why |

## Beat (from the brief)

Mountain wilderness at dusk. Wind moves through tall golden grass. There is a fresh mound of earth with a simple wooden grave marker. Fang Yuan's younger self stands before the grave: the same face, younger and softer, long black hair tied back, plain worn grey-brown traveler's clothes. Fists clenched at his sides, he cries openly: tears on his cheeks, lips trembling, shoulders shaking. The camera makes one slow arc from behind his shoulder to a three-quarter profile, catching the tears in the dusk light. No cuts.

## Generation prompt

[STYLE]
Flashback. Faded amber-sepia dusk, soft bloom, heavier film grain, gentle vignette, soft painted background texture. Mountain wilderness; wind sways tall golden grass. A fresh mound of earth with a simple wooden grave marker. The young Fang Yuan stands before it: a slender youth with a long narrow face, sharp jaw, straight nose and narrow dark eyes under straight brows, younger and softer. His long black hair is tied back. He wears plain, worn grey-brown traveler's clothes. Fists clenched at his sides, he cries openly: tears on his cheeks, lips trembling, shoulders shaking. One slow, continuous camera arc from behind his shoulder around to a three-quarter profile, catching the tears glinting in the dusk light.

## Segment-specific negatives

river, water, storm, white robe, charcoal robe, loose hair, adult face, second person, mourners, wailing open mouth, speech, lip-sync, rain

## Segment-specific checklist

- [ ] Only the younger self is present; no other people.
- [ ] Hair tied back; grey-brown traveler's clothes, not the river robes.
- [ ] The face is clearly the same person as the present-day sheet, younger.
- [ ] Crying reads clearly (tears, trembling lips, shaking shoulders) without the mouth moving as if speaking.
- [ ] One slow arc, behind the shoulder → three-quarter profile, with no cut.
- [ ] Amber-sepia dusk palette with grain and vignette.

## Cross-session contract (mandatory)
Queue status is in `production/state.json`; the header is descriptive, not authorization.
Read the whole brief, COMMON, CONTINUITY, QUALITY_GATE and MEDIA_CONTRACT, inspect actual
masters and the approved model/recipe, and run `--task T12`.
Candidate sample count: **120** at 24 fps; retained final count:
**120**, range **[312, 432)**.
Both endpoint samples are displayed; no endpoint may be trimmed.
Retiming uses endpoint-to-endpoint span, not nominal container duration.
Store native and conformed attempts, payloads/locks/hashes, full-frame review and timed
beat evidence. T12 produces candidates only; Q12 independently accepts/rejects.
Match the approved full-film motion language and visual master; no standalone style reinterpretation.
Include D_entry: the 120-frame D with reviewed in-place ripple reveal on its first six frames; no shortened xfade or ghosted second person. Preserve plain D too.

## Attempts

| # | Date | Session | Model + version | Settings | Retime | Cost (OLU) | Verdict | Notes |
|---|---|---|---|---|---|---|---|---|
