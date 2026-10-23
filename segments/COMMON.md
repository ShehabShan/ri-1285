# Shared blocks for every segment

## Prompt blocks

Resolve these blocks into every river prompt; D uses STYLE plus its younger/flashback block, not CHARACTER/RIVER. Preserve semantic constraints; store the expanded payload and recipe delta. Use negatives contextually: D must retain crying, tied hair and warm dusk. Never submit literal [STYLE] placeholders.

**STYLE**
Premium modern Japanese anime feature film, ufotable / MAPPA quality. Hand-drawn 2D characters with clean tapered line art and cel shading with soft gradients. Detailed hand-painted matte backgrounds with deep atmospheric perspective. Richly simulated but stylized anime water: sculpted foam shapes, crisp droplets with painted highlights, layered mist planes, soft bloom. Cinematic lens, smooth stabilized camera, shallow depth of field in close-ups, light film grain. Slow, heavy, deliberate pacing. One continuous shot, no cuts.

**CHARACTER (river segments)**
Fang Yuan: tall slender young man, pale cool-toned skin, long narrow face, sharp jaw, straight nose, thin closed lips, narrow dark eyes open under straight brows. Very long, straight, jet-black, center-parted loose hair, soaked and streaming behind him. Loose pure-white cross-collar inner robe with wide sleeves, open at the collar, covering his torso and shoulders. Dark charcoal-black outer robe with a faint deep-teal tint and mottled texture, worn open and slipped down below both shoulders, hanging at his upper arms, its long fabric trailing behind him in the current. Dark trousers. Neutral, emotionless face, gaze fixed forward, mouth closed. Steady, heavy walk, about one step per second, slight forward lean into the current.

**RIVER**
A vast mythic river of deep ink-blue to black-teal opaque water, with white-crested rapids, standing waves, sheets of spray and low surface mist. The water is knee-deep on him. He walks upstream: the current strikes the front of his legs and flows past him toward his back. The river fades into endless mist upstream; dark jagged cliffs stand at the far left and right. Heavy slate-grey storm overcast, cold diffused silver light, no sun. Faint pale-gold motes drift downstream in the spray. Cold, desaturated palette of blue-black, slate grey, steel teal and bone white. Cool-white rim light on his hair, face edge and shoulders.

## Negative prompt (all segments)

jump cuts, extra cuts, rapid cutting, montage, AMV-style editing, music-video editing, scene jumps, flash frames, sudden camera resets, photorealistic, live-action, real human, 3D CGI face, plastic skin, Western cartoon, chibi, bright saturated colors, sunny sky, blue sky, smiling, screaming, lip-sync, tears in river scenes, short hair, outer robe pulled up onto the shoulders, modern clothing, armor, jewelry, weapons, extra limbs, extra fingers, deformed hands, face morphing, identity drift, extra people, crowd, spectators, duplicate characters, walking downstream, water flowing the same direction he walks, transparent water, visible riverbed, visible boots, changing water level, frozen water, parted river, still mirror water, glowing eyes, visible creature, sliding feet, floating walk, stiff mannequin pose, crushed black shadows, face hidden by mist, text, subtitles, watermark, logo, jittery camera

## Acceptance checklist (all segments)

A clip is accepted only if **every** applicable item passes AND the positive craft floor in `docs/QUALITY_GATE.md` passes in a separate fresh-session review. One-second samples alone cannot justify acceptance. The complete brief, bibles, approved masters, boundary motion contract, technical/evidence gate and segment beats are mandatory inputs.

**Continuity**
- [ ] No cuts, jump cuts, flash frames or camera resets inside the clip.
- [ ] The first frame matches the start keyframe in composition, pose, lighting and water.
- [ ] The last frame matches the end keyframe in the same respects.
- [ ] The camera moves smoothly, with no jitter.

**Character**
- [ ] One person only. No duplicates or background figures.
- [ ] The face matches the locked sheet throughout, with no morphing or identity drift.
- [ ] *River:* the outer robe is below both shoulders, the white inner robe covers the shoulders, and the hair is long, loose and center-parted.
- [ ] *River:* neutral face, mouth closed, no tears, no lip movement, eyes open and not glowing.
- [ ] *River:* he walks continuously at about one step per second. Feet plant; no sliding, floating, stopping or stumbling.
- [ ] Hands are anatomically correct wherever they are visible.

**River**
- [ ] He walks upstream: the current hits the front of his legs and flows behind him.
- [ ] The water is knee-deep, opaque and at a constant level. The boots and riverbed are never visible.
- [ ] The river never slows, parts, freezes or turns still.
- [ ] Storm-grey sky with no sun or blue. The gold motes are the only warm color.

**Look**
- [ ] Anime: not photoreal, no 3D faces, no watercolor or cream palette from the reference.
- [ ] Mist never covers his face.
- [ ] No text, subtitles, logos or watermarks.

## Additional acceptance gates
- [ ] All frames reviewed, positive craft dimensions each >=4 with evidence.
- [ ] Exact native + conformed specs/provenance and hash lineage recorded.
- [ ] Camera/gait/hair/cloth/current/light continue through boundary motion windows.
- [ ] Named timed beats and actual plant times measured, not merely prompt intent.
- [ ] Native audio removed; no lip-sync; D intentional appearance changes preserved.
- [ ] No boiling/smear/plastic skin/CGI gloss/texture crawl/generic float/overbloom concealment.
- [ ] Separate reviewer evidence package passes; unresolved = candidate/hold.
- [ ] Upstream assets and locks remain current; downstream invalidation checked.

Technical checks do not grant artistic acceptance. If camera limits hide feet, grounded
walking must still read in torso/cloth/splash; do not fabricate a visible boot to prove it.
