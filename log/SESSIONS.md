# Session log

Newest entry first. See the format in `docs/SESSION_PROTOCOL.md`.

## Session 7 — 2026-10-27 — sequential handoff (no production task)
- Bot: https://prompt.ql.app/project/p-fc80a416-c97c/promptql-playground/thread/a5cd703a-1957-4fa8-80d2-33e683f8fd6a
- Did: User asked for strictly sequential creation where each session knows what the previous one made. Added DECISIONS D9, production/sequence.json skeleton, docs/CONTINUITY_LOG.md and media/{stills,clips,frames}.
- Tests: GitHub Release asset upload is blocked (uploads.github.com not on the integration allow-list; test release and tag deleted). A 12 MB binary committed on a throwaway branch pushed in ~10 s with a larger http.postBuffer, was served by raw.githubusercontent.com (branch and commit-pinned) with matching SHA-256 within 10 s, and came back intact in a fresh clone. Throwaway branch deleted.
- Cost: no paid generation.
- Next: S01 — implement D1-D9; no paid submits.

## Session 6 — 2026-10-27 — decisions locked (no production task)
- Bot: https://prompt.ql.app/project/p-fc80a416-c97c/promptql-playground/thread/a5cd703a-1957-4fa8-80d2-33e683f8fd6a
- Did: User delegated all open decisions. Wrote docs/DECISIONS.md (D1-D8): Kling 3.0 4K with whole-film Pro fallback, 6-clip shot plan with exact frame map, still bake-off, Kokoro TTS + synthesized/CC0 audio, spending authorization ($60 estimate ceiling), delegated fresh-session review, conform rules, session order. Updated S01/T03/T15 handoffs, queue and AGENTS.
- Live checks: Kling 3.0 4K 5 s sound off estimate = $2.10 (endpoint works again; the sound-on 4K estimate timed out once). Pro $0.84, Std $0.63, Qwen Image 3 edit $0.075, Grok Image 2.0 $0.09. No audio/TTS model in the 91-model catalog; no TTS or music integration connected.
- Cost: no paid generation.
- Next: S01 — implement docs/DECISIONS.md; no paid submits.

## Session 5 — 2026-10-27 — audio decision record (no production task)
- Bot: https://prompt.ql.app/project/p-fc80a416-c97c/promptql-playground/thread/a5cd703a-1957-4fa8-80d2-33e683f8fd6a
- Starting commit: 2f6d7ed.
- Did: Pre-start review. Found S01 still undone and listed contradictions (audio vs. brief, frame budget, ripple handles, per-clip review, fresh start stills, output conform). User decided audio: Kling sound on for ambience only, brief cues added at assembly. Recorded in SEQUENTIAL_DESIGN, state.json (S01, T15) and the queue.
- Live checks: Higgsfield catalog 91 models, Kling 3.0 4K i2v present; estimate endpoint still HTTP 500; Opus 5.5 llm_config id here is 0edabd39-3d21-42cb-9cfd-bc2c494eda84 (b90a5408-… is from another project).
- Cost: no paid generation.
- Next: S01 — implement the sequential design with the fixes in its handoff; no paid submits.

## Session 4 — 2026-10-23 — planning for S01 (no production task)
- Bot: https://prompt.ql.app/project/p-3a501402-0511/promptql-playground/thread/eeec6cca-29b2-48b3-9939-4064732345b0
- Starting commit: 2d950d9.
- Did: Verified Kling 3.0 4K on Higgsfield, Opus 5.5 availability, and that Higgsfield has no standalone audio model. User approved sequential clip-by-clip creation and Kling built-in sound. Recorded the approved design in docs/SEQUENTIAL_DESIGN.md and added task S01 to implement it. T03 is blocked behind S01; T15 no longer needs a user audio decision.
- Not done (stopped early, user's OLU running low): the actual repo rewrite (sequence.json, protocol, timeline, validator, assembler, tests). That is S01.
- Cost: no paid generation. Price estimate endpoint failed (HTTP 500, then timeout); $2.10/5 s not re-verified.
- Next: S01 — implement docs/SEQUENTIAL_DESIGN.md exactly; no paid submits in S01.

## Session 3 — 2026-10-23 — H01
- Bot: https://prompt.ql.app/project/p-ed43b976-7f56/promptql-playground/thread/18829eed-928e-461d-8c78-78356208c32c
- Starting commit: 68e9cee8a79dbbd488319a4ecbd9a0cc330279de.
- Did: User-requested fresh-session audit and hardening, not a generation task. Added approved visual/motion master contracts, per-boundary motion handoffs, independent T/Q review gates and craft floor, hashed state/lineage/provenance, charged-job recovery and exact media/audio/assembly accounting. See docs/AUDIT.md for the failure-route closure matrix. Added stdlib validator, mechanical assembler, generated queue, schemas, an installable CI template and 25 tests. Automatic CI is not enabled: the integration refused workflow-file writes; see docs/ci/README.md.
- Inputs/outputs: Existing brief/bibles/specs/reference audited; all changes are documentation, state scaffolding and tooling. No media or design locks created, no assets marked accepted.
- Verification: 25 local tests pass, including real synthetic FFmpeg 720-frame assembly and PCM silence/endpoint ownership; scaffold validator and git diff --check pass; release gate fails as expected with missing final media/approval. Brief SHA256 unchanged: 4027727c897c20c10a9f2ef1037851ed14a3cfc273a47e82d5d2b56380419432.
- Cost: 5.69 OLU ledger snapshot during this interaction, own work only; zero paid media generation. Snapshot excludes remaining validation/publication and closing messages; not a final settled total.
- Result: hardening complete; publication is verified separately by remote commit check; native Git requests timed out, so an atomic GitHub API commit is used if authorized. Scaffolding tests certify mechanics/provenance, not artistic quality or an unseen clip.
- Next: T03 produces candidate present-day views and image bake-off evidence; Q03 independently reviews, obtains user approval, then locks image recipe. Do not submit until total OLU cost bound is reliable. T15 still needs user authorization of audio source/voice/rights. Later actual capability/temporal quality and visual approvals remain real gates.

## Session 2 — 2026-10-23 — T02
- Bot: https://prompt.ql.app/project/p-5dbcae94-40af/promptql-playground/thread/eaca8889-2209-4662-b1d1-6be78488a20f (same bot as session 1)
- Did: Surveyed the Higgsfield catalog (87 models) and extracted parameters for the first/last-frame video, reference-image and video-to-video candidates. Ran cost estimates and wrote `docs/MODELS.md`.
- Cost: ~27 OLU, own work only; no generation.
- Result: done. Seedance 2.5 and GPT Image 2.5 return description-only estimates, so they are probably not submittable through PromptQL. Kling O3 4K mode returned 409 and Kling O3 video-edit's estimate returned 500. There is no audio model.
- Next: T03, an image bake-off (Qwen Image 3 edit vs Grok Image 2.0) and then the present-day sheet. It must record the OLUs actually charged per submit. T15 needs an audio decision from the user.

## Session 1 — 2026-10-23 — T01
- Bot: https://prompt.ql.app/project/p-5dbcae94-40af/promptql-playground/thread/eaca8889-2209-4662-b1d1-6be78488a20f
- Did: Scaffolded the repo. Added the brief verbatim, the reference image, the character and world bibles, the pipeline and session protocol, keyframe plan K1–K9, segment specs A–F with acceptance checklists, and the task queue T01–T18.
- Cost: own work only; no generation.
- Result: done.
- Next: T02, the model survey. The user wants the generator chosen by quality at run time, so T02 records which top-quality models are available and what each call costs in OLU.