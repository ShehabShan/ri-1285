# Acceptance: compliance AND craft
**No automated test, score, vendor name or endpoint still can certify top artistic quality.**
Automation checks accounting/provenance; independent review judges what is actually seen.
No waiver of a FIXED item, no budget-driven acceptance, no "fix in post" without a
tested bounded repair which itself re-passes review. Unknown = hold, not pass.

## Review package (images, clips, audio, assembled/finished)
Each candidate gets a unique asset record; the producer records only `candidate`.
Commit complete request/config/job provenance, original file and conformed file, probe
results, hashes of exact upstream inputs and locks, and expanded prompts.
For images: inspect full resolution plus master-crop comparisons and all requested views.
For video: watch the ENTIRE clip at normal speed with/without sound, slow motion, and
inspect every frame for glitches (use frame-sequence playback; not one-second sampling).
Save a representative contact sheet AND dense +/-12-frame seam strips, first/last
comparisons, defect timecodes, step/beat event table and a playable seam loop.
Single-frame defects count. Sampling is navigation/evidence, never permission to skip
the rest. If the review tool cannot inspect the whole clip, hold pending human review.
For audio: listen to all stems/mix in sync; inspect waveform/sample checks, transcript,
speech finish time, footsteps and silence; use AUDIO contract.
Store the actual review evidence in repo/hashed Release artifacts, not chat only.

## Reviewer and disposition
Review occurs in a separate fresh session/task with different session ID from producer,
no sunk-cost incentive and no generation in that task. Record reviewer identity/session,
asset SHA, master/lock/input hashes, inspected frame ranges, all criterion outcomes and
evidence paths with hashes. N/A requires a visibility-based reason; brief/global criteria
and unknown visibility cannot be waived as N/A. Automated evidence cannot impersonate
user approval.
Review JSON: `production/reviews/<asset-id>.json` has asset_id, sha256, producer_session,
reviewer_session, criteria [{id,status,reason,evidence}], scores, evidence [{path,sha256}],
user_approval (masters/final only), verdict. Required criterion IDs come from state.json;
status `pass` for required criteria; report additional scoped spec checks by criterion ID.
Any fail => reject; any unknown/unreviewed => hold/candidate; all pass => accepted.
Master/user approval contains a source citation and exact reviewed asset hash.
Do not let a candidate producer invent an approval. Independent bot review is a minimum,
not equivalent to a human art director; user can reject any output.

## Non-negotiable checks (all applicable frames)
Brief FIXED 1–10, format/event timing, shared COMMON checklist and each segment's
specific beats. Hands and face remain coherent; robe shoulder rules; boots invisible;
world-correct upstream/current; heavy grounded gait with consistent phase; no unintended
cut, duplicate figure, pose reset, sudden lens jump, or changed emotion.
C reaches anatomical LEFT eye by 12s; reflected ripple fills frame by 13s, not a glowing eye.
E reaches face by 20s, chest begins only in prescribed 20–25s interval. F stays medium
until 25s; rays originate inside the body, walking/river continue through flare.
Do not fail valid D for the intentional warmer palette/crying/tied hair; no lip-sync.

## Positive craft floor (1–5, EACH >=4; never an average)
1 = broken, 2 = visibly weak, 3 = usable but generic/inconsistent, 4 = polished and
convincingly matches approved masters, 5 = exceptional feature-quality execution.
A reviewer must provide crop/timecode evidence and a sentence justifying each score.
Dimensions: identity/drawing; composition/cinematography; line/shading/material craft;
colour/light/depth; grounded acting/motion; fluid/cloth/hair coherence; temporal stability;
seam integration (for applicable neighbors); emotional/pacing fidelity.
Static assets mark motion/seam dimensions inapplicable with reasons, not fictitious scores.
Audio uses performance/timbre, arrangement, timing/sync, intelligibility, mix/cleanliness.
A 4 is assessed against USER-APPROVED master examples, not the latest mediocre generation.
Rubbery limbs, boiling linework, smeared facial features, glossy CGI skin, texture crawl,
unmotivated camera float, overbloom hiding mistakes, lifeless mannequin walk, generic
particle haze or overly smooth interpolation are reject reasons even with no obvious cut.
If no candidate reaches 4 in every applicable dimension: reject all and hand off.

## Gates
Q03/Q04/Q05: design, style/crop masters + explicit user approval before downstream work.
Q06–Q08: contact sheet across all K frames, coherent environment/identity, verified
file formats and planned boundary contracts, no optional endpoint missing.
Q09: first river A + comparative model evidence + motion anchor; freeze recipe only now.
Q10/Q11/Q14: predecessor+candidate seam AND individual quality, not isolated playback.
Q13: match to A's master motion language and K8 continuation. Q12: identity/rendering
matches master despite intentional flashback changes.
Q15: exact speech/cues/sync/silence, authorized assets, technical audio checks.
Q16/Q17: full film one-hand coherence, every frame/seam/event after ANY finishing.
Q18: final exact file export tested again and explicit user signoff; never claim final
from a rough proxy. Review status and bytes must agree; accepted metadata is not magic.
