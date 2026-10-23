# Model survey (T02, 2026-10-23)

This survey covers what the PromptQL built-in Higgsfield integration (`run_http(integration="__higgsfield")`, base `https://api.higgsfield.ai`) exposes. The catalog lists 87 models (`GET /models`). Costs come from `POST /estimate/<model-path>` with the same body as the submit. **No generation was run in this task**, so the quality notes below are expectations from the documentation, not observed results. The bake-off in T03 (images) and T09 (video) settles quality.

## Cost and billing facts

- The estimate returns Higgsfield credits plus USD. 16 credits = $1.00 (e.g. 8.96 credits = $0.56).
- PromptQL charges OLUs from that estimate when a submit is accepted, and refunds them if a poll observes `failed` / `nsfw` / `canceled`. The OLU-per-USD rate is not visible to users. **The first session that submits must record the OLUs actually charged** (see "Measuring spend" below), then fill in the OLU column here.
- **PromptQL refuses a submit when the estimate is not a plain decimal USD amount.** Some models return only a pricing description (`"type": "description"`). Treat these as **probably not submittable through PromptQL** until a session proves otherwise. Affected: Seedance 2.5 (all routes), Marketing Studio Image (GPT Image 2.5).
- Estimate calls take about 6–20 s each and sometimes hang. Wrap each one in a timeout (about 40 s) and run at most 4 in parallel.

## Video: segments (need first frame + last frame)

All estimates are for 5 s, sound off.

| Model path | First / last frame params | Duration | Resolution | Est. 5 s | Notes |
|---|---|---|---|---|---|
| `kling-video/v3.0/4k/image-to-video` | `image_url` / `last_image_url` | 3–15 s, integer | 4K (fixed) | 33.6 cr = **$2.10** | Highest resolution offered. Has `cfg_scale` (0–1, default 0.5). `sound` defaults to **on**, so send `"sound":"off"`. No aspect param; framing follows the image. |
| `kling-video/v3.0/pro/image-to-video` | `image_url` / `last_image_url` | 3–15 s | pro tier | 8.96 cr = $0.56 | Same API as 4K, lower resolution. |
| `kling-video/o3/first-last-frame` | `first_frame_url` / `last_frame_url` | 3–15 s | `mode` std/pro (4k returned **409 unavailable**) | 8.96 cr = $0.56 | `aspect_ratio` 16:9. Multi-shot support. `sound` default off. |
| `kling-video/omni/first-last-frame` | `first_frame_url` / `last_frame_url` | 5 or 10 s only | `mode` std/pro | 8.96 cr = $0.56 | Only two durations are allowed. |
| `minimax/h3/image-to-video` | `image_url` / `end_image_url` | 5–15 s | 2K only | 10.4 cr = $0.65 | No audio. Aspect follows the keyframe. |
| `alibaba/wan-3.0-prime/image-to-video` | `image_url` / `end_image_url` | 2–30 s | ≤1080p | 8.96 cr = $0.56 | Has `seed` and `aspect_ratio`. `generate_audio` defaults to true, so send false. |
| `pixverse/v6/image-to-video` | `image_url` / `end_image_url` | 1–15 s, fractional | ≤1080p | 6.12 cr = $0.38 | Has `negative_prompt` and `seed`. Fractional duration allows exact lengths. |
| `bytedance/seedance-2.5/image-to-video` | `image_url` / `end_image_url` | 4–30 s | ≤1080p | description only, ≈ $1.14/s at 1080p | **Probably not submittable** (see billing facts). |

**Recommendation.** Use the T09 bake-off on segment A with the same K1/K2 keyframes. Run **Kling 3.0 4K** (top resolution) first, then **Kling O3 pro**; MiniMax H3 is excluded for 4s A under the current ±15% retime rule unless a qualified shorter native duration becomes available. Pick the model by the acceptance checklist plus visual quality, then lock it for every river segment. At these prices one clip costs about $0.4–2.1. The OLU equivalent is still unmeasured.

## Images: character sheets and keyframes (need reference images)

| Model path | Reference images | Resolution / aspect | Est. | Notes |
|---|---|---|---|---|
| `alibaba/qwen-image-3/edit` | `image_urls` 1–3 (required) | `1k`/`2k`, 16:9 available | 1.2 cr = $0.075 | Has `seed` and `prompt_extend` (default true). |
| `xai/grok-imagine-image-2.0` | `image_urls` 0–10 | `1k`/`2k`, 16:9 available | 1.44 cr = $0.09 | `quality` low/medium. Accepts more references, which helps when conditioning on sheet + style frame together. |
| `marketing-studio/image/flare` (GPT Image 2.5) | `image_urls` ≤16 | up to 4k, quality up to `max` | description only | **Probably not submittable.** |

**Recommendation.** In T03, generate the front view with both Qwen Image 3 edit and Grok Image 2.0 at 2k, compare, then hand off to Q03 for independent review and user approval before locking the winner.

## Video-to-video: consistency pass (T17)

| Model path | Inputs | Est. | Status |
|---|---|---|---|
| `bytedance/seedance-2.5/video-edit` | `video_url` + `image_urls` refs, ≤1080p, output length = source | description only (≈ $0.68/s combined in+out at 1080p) | Probably not submittable. |
| `kling-video/o3/video-edit` | `video_urls` [1] (3–15.5 s, ≤200 MB) + `image_urls` ≤4, mode std/pro/4k | estimate returned **HTTP 500** | Unverified. Input is capped at 15.5 s, so the pass would run per take (Take 1 = 13 s, Take 2 = 12 s), which fits. |
| `higgsfield/genjutsu/restyle/v1.0` | `video_url` (4–30 s) + `preset_id` (required; list via `GET /models/higgsfield/genjutsu/restyle/v1.0/presets`) + `image_urls` ≤5 | not estimated | Restyles to fixed presets only, which is a risk to the locked look. |

These are unverified historical candidates, not a required route. T17 defaults to conservative deterministic finishing/review, with any generative experiment requiring explicit user approval and full regression QA.

## Audio

The catalog has **no standalone music, SFX or TTS model**. Several video models can generate native sound, but that is not usable for the brief's precise score and monologue. T15 needs a source decision from the user.

## Inputs: getting keyframes to the API

All models take public HTTPS URLs. There are two options:
1. Raw GitHub URLs of committed files. This only works if the repo is public.
2. Higgsfield upload: `POST /files/generate-upload-url` with `{"content_type":"image/png"}` returns `{public_url, upload_url, upload_headers}`. PUT the bytes to `upload_url` with exactly `upload_headers` and no credentials, then pass `public_url`. The upload URL expires after 1 h. Supported types: jpeg/png/webp/gif, wav, mp4. This route is documented but not yet exercised.

## Measuring spend

A session's own OLU use can be read with `promptql.playground.query_graphql`:

```graphql
query($t: uuid!, $since: timestamptz!) {
  olu_usage_aggregate(where: {thread_id: {_eq: $t}, timestamp: {_gte: $since}}) { aggregate { sum { olus } } }
}
```

## Locked choices (summary only; registry is authoritative)

| Stage | Model | Locked by | Settings |
|---|---|---|---|
| Sheets and keyframes | — | Q03 | — |
| River segments | — | Q09 | — |
| Flashback (D) | — | Q12 | — |
| Consistency finishing | — | Q17 | — |

## Measured OLU per call

| Model + settings | Est. USD | OLU charged | Session |
|---|---|---|---|

## Hardening: selection is not permission
All catalog/price observations above are dated survey results, not live capability proof.
P01 must verify actual native durations, endpoint controls and total OLU upper bounds.
5s-minimum MiniMax/Omni cannot supply 4s A/C within the speed limit. Compare actual
endpoint sample spans, including A/B/E boundary samples and F\'s 156 displayed samples.
Q03 and Q09 freeze image/river recipes in `production/assets.json` ONLY after review;
this empty summary table is not an accepted lock. Include endpoint/version (or unpinned
service evidence), all supported settings, prompt expansion off, explicit sound-off,
no multi-shot, seeds and ordered role references. Unsupported controls require a
recorded mitigation, not invented request fields. Requalify silently revised services.
The first controlled paid attempt requires a reliable OLU bound or explicit user decision
before submitting; USD pricing alone cannot authorize unknown spend.
