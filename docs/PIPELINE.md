# Pipeline
## Keyframes are constraints, not a seamlessness guarantee
The six segments are produced across fresh sessions, but are **not independent creative
decisions**. Approved visual masters, one motion language, frozen model recipes,
shared boundary images AND boundary motion contracts constrain every segment.
A shared still can hide a pose mismatch but cannot match velocity, gait, fluid phase,
exposure or line treatment. Failure to achieve a convincing join means reject/rework,
not disguise a cut. Longer whole-take generation is an escalation requiring a recorded
plan and budget approval, not a silent change to the brief.

## Stages and gates
T01–T02 establish specs and catalog facts. T03–T08 produce candidate sheets/style/keyframes;
Q03–Q08 independently review them. Q03, Q04 and Q05 lock user-approved visual masters,
including a flashback look in Q04. P01 validates model capability, timing and storage.
T09 makes the first river candidate; Q09 approves and locks the river recipe and motion
anchor before any other river segment. T10/Q10 and T11/Q11 follow Take 1 in order.
T12/Q12 makes/reviews D; T13/Q13 and T14/Q14 follow Take 2 in order. T15 waits for reviewed
motion and an authorized audio source; Q15 reviews the mix. T16 assembles a reproducible
rough master and Q16 checks all seams and full-film coherence. T17/Q17 is a conservative
consistency review, not a mandatory generative repaint. T18/Q18 performs final QA and
user delivery approval. State JSON is the dependency authority.

## Model policy
At the **selection stage**, compare strongest feasible candidates using the same approved
inputs and the quality rubric, not resolution/price/brand as a proxy for artistry.
A 5-second-minimum model is not viable for A or C if 4-second conforming violates the
15% speed limit. Qualify actual first AND last frame control, native durations, spatial
resolution, fps, input count/role, output restrictions, disabled audio/multi-shot and
cost before a submit. P01 must record evidence for every segment's feasibility.
Q03 locks an image recipe only after comparisons and user master approval.
Q09 locks a river recipe only after independent acceptance. One candidate is insufficient
to claim a comparative bake-off was completed; budget-limited comparisons remain open.
Record the endpoint, model version (or explicitly unpinned provider service + observed
revision/time), settings, resolved prompts, reference roles/order and actual media specs.
Unpinned services need an anchor regression check each fresh session; exposed model
revision change or unexplained output drift blocks generation pending requalification.
No silent substitution, "newer is better", reduced quality tier, or weaker default.
D may differ in model only with a documented superiority comparison and matching line/
identity language. A model change is a lock revision and invalidates affected outputs.
MODELS.md survey recommendations are not locks; assets.json is the lock registry.

## Conform and assembly
Follow MEDIA_CONTRACT and timeline.json exactly. Normalize with documented fps/time mapping,
never use source-container duration alone as frame math. Accept retiming only if
`0.85 <= source_motion_span / target_motion_span <= 1.15`, the endpoints survive,
and the resulting gait/camera cadence still pass visual review. Keep original and
conformed clips. No trimming a required endpoint, freeze-padding, blind interpolation
or upscaling as a substitute for genuine detail.
A/B/E carry one extra endpoint sample. Assembly discards the **predecessor's last**
duplicate, NOT the next clip's first frame. Exact final allocation is 720 frames.
Read MEDIA_CONTRACT for ripple handles, white hold, sample-accurate audio, codecs and
all event coordinates. No ordinary xfade that shortens the timeline.
Inspect at least +/-12 frames around A/B, B/C, E/F and both transitions at full speed,
slow motion and frame-by-frame. Match motion on both sides, not just an endpoint.
No unconditional optical-flow escape hatch: a narrowly scoped repair needs candidate/
review evidence and may not introduce double outlines, watery faces or a new transition.

## Consistency pass
Source clips must already be coherent before T16. A late restyle cannot rescue weak
anatomy, motion, bad direction, or a seam. Default T17: compare, then deterministic
global finishing only if needed (recorded grade/grain/bloom, no content/timing changes).
A generative video-to-video experiment is optional, requires explicit user approval,
cost/capability preflight and a reversible branch. Never blindly restyle all 30 seconds
or merge warm D into the cold river look. Retain rough master and original audio.
Any processed output must re-pass the entire per-frame, seam, style, event and final
gate; otherwise retain the already accepted rough cut. No tool availability => no
automatic blocker if no harmonisation is needed, but no "skipped QA" either.

## Storage and portability
Commit assets <=50 MB. Larger files require immutable GitHub Release asset references,
byte size and SHA256, a small review proxy and reproducible download instructions.
Check an unauthenticated URL only for confirmed public assets; never publish tokens,
private content or expiring signed URLs. Raw GitHub input URLs MUST use a full commit
SHA, not main. Test uploaded bytes against local hashes; record stable input identity,
not temporary transport. Provider expiry requires immediate download/verification.
A clean clone plus declared Release downloads must reproduce the work with no former
bot filesystem, chat attachment, prior model cache or personal directory.
