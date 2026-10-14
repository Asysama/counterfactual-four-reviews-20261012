# PR 665 generator review

**Decision:** PASS (contributor self-check; owner review pending)

**Reviewed head:** `b559e50012402d8437d9151995ce48a764ef5520`

**Generator:** `air_gap_plate_attraction_reversal`

**Generator correctness:** PASS

**Runtime-provenance policy scope:** NEW/REPLACEMENT

**Runtime provenance:** PASS

**Declared scaling target:** 100000 accepted cases; 100000 CPU static recipes audited, two native rendered cases (seeds42,98), plus six controlled rendered axes. No claim of100000 rendered videos.

**Smaller-target rationale:** Not applicable.

**Declared-target scale readiness:** PASS

**Production readiness:** PRODUCTION READY for the declared generator contract; this is not Sara approval or submission.

## Blocking findings

No unresolved hard-gate finding at the reviewed head. 喷口夹着一条黄色实体飘带，开气后抬起并飘动；正常双板内收，异常双板外张。

Earlier visual shortcomings were fixed and every affected formal case was regenerated. The retained independent decoder report deliberately records its then-pending human visual/browser stage; those fields are closed by the later exact-head `visual.json` and `browser.json`, not silently rewritten.

A superseded independent audit used exact equality for differently ordered floating-point pressure products. The current audit uses1e-12 coefficient tolerance, while decoded prefix and binary-mask requirements remain exact. The original failed audit log is preserved; no generator/media change was made to suppress that finding.

## Six-gate result

| Gate | Result | Evidence |
|---|---|---|
| Output contract | PASS | `review-evidence/independent.json`: eight native2048×2048 H264/RGB streams,24fps,120frames,5s |
| Violating-object-only mask | PASS | All-frame strict binary checks, exact active interval, mask-only red overlay; `visual.json`, native-inspection crops and `mesh.json` |
| Real scaling | PASS | `scale.json`, `axis-probes/axis-probes.json` and `six-axis-independent.json`; visible independent physical/composition axes |
| Official unpatched environment | PASS | Clean source, successful `runtime-witness.json`, component records and case index; official generation environment |
| Decoded matched control | PASS | Every decoded True/CF frame before intervention is RGB-identical; trajectories share prefix |
| Semantic consistency | PASS | `generator-README.md`, `generator-DESIGN.md`, exact prompt.txt/metadata strings and observed outcomes |

## Production-quality behavioral baseline

| Check | Result | Evidence |
|---|---|---|
| True completes its prompt outcome | PASS | Symmetric gap flow reduces pressure and the cards settle inward. |
| Exactly one CF physical error | PASS | Only the gap-pressure sign reverses; cards settle outward. |
| Both prompts independently align | PASS | Each branch carries a complete apparatus/action/outcome description; prompt text equals metadata; two native cases visually inspected. |
| Matched setup and correct labels | PASS | Shared scene/profile/camera/ribbon or reference; exact pre-intervention control; branch-specific operator only. |
| No unrelated visible defect | PASS | Native full-scene and consecutive crops; evaluated swept geometry; actual browser playback. |
| Completion and observation tail | PASS | Evidence precedes final frame; target remains visible through frame119; decoded border/area checks. |
| Phenomenon-specific plausibility | PASS | Independent pressure/hinge torque ODE and gap clearance. Yellow ribbon is a qualitative attached airflow indicator, shared by both branches, not a resolved fluid simulation. |

## Formal cases and timebase

| Seed | Intervention | First visible change | Evidence | Physical seconds/video second | Source interval | Internal integration |
|---|---|---|---|---|---|---|
| 42 | 24 | 24 | 26 | 1.0 | 0.041666666666666664 | 40 steps × 0.0010416666666666667 |
| 98 | 28 | 28 | 29 | 1.0 | 0.041666666666666664 | 40 steps × 0.0010416666666666667 |

Time mapping is explicitly declared and shared by the pair. Rattleback uses intentional4× slow motion; the other two use real time. Solver integration steps are distinct from recorded frames. Event, prefix, mask onset and final visibility are verified on the delivered timebase. No simulator-native dynamics claim is made: Blender Workbench renders generator-owned trajectories.

## Semantic matrix

| Title/README/model | True prompt | CF prompt | Scoring/operator/render | Result |
|---|---|---|---|---|
| air_gap_plate_attraction_reversal | Symmetric gap flow reduces pressure and the cards settle inward. | Only the gap-pressure sign reverses; cards settle outward. | All identify the same single registered rule and evidence event; exact prompt-to-metadata comparison plus native video inspection. | PASS |

## Successful-render runtime provenance

Successful formal and clean-source reproduction witnesses bind exact head, clean source, command, seeds, actual interpreter/dependencies, Blender component, FFmpeg, OS, GPU/driver, encoder and artifact hashes. Every accepted formal case maps exactly once in `runtime-witness-index.json`. Downloaded case manifests and witness/index hashes were independently rechecked. Generation and reproduction recipes are distinct from runtime evidence.

## Reproduction

Seed42 was independently regenerated from clean source. Recipes, trajectories and binary masks match exactly. The measured renderer-only RGB rounding is reported below; each submitted pair still requires zero-tolerance RGB equality before intervention.

| Stream | Maximum channel difference | Total changed pixel instances over120frames | Max changed pixels in one frame |
|---|---|---|---|
| true/video.mp4 | 0 | 0 | 0 |
| counterfactual_gap_pressure_difference_sign_reversal/video.mp4 | 0 | 0 | 0 |
| counterfactual_gap_pressure_difference_sign_reversal/mask.mp4 | 0 | 0 | 0 |
| counterfactual_gap_pressure_difference_sign_reversal/mask_overlay.mp4 | 0 | 0 | 0 |

## Client-facing artifact consistency

All eight browser streams were actually played to5s in Chrome, with no media errors, and sought to frame0, each case evidence frame, and frame119. Masks display white targets on black; overlays show red only on the violating object. The1024 review RGB/overlay streams are explicitly lossy compatible derivatives; the native2048 lossless originals remain separately linked. Full anonymous HTTP downloads and SHA256 checks cover every public packet file and all native/browser video bytes.

## Scale-readiness result

| Check | Result | Evidence |
|---|---|---|
| CGC-v1 profile space and declared target | PASS | 1000000 profiles; 100000 accepted static cases; 100000 distinct effective signatures. |
| Actual independent rendered axes | PASS | Length, response, onset, depth, appearance and view; paired low/high rendered images and quantitative decoded image changes. |
| No dead or rejection-collapsed axis | PASS | {'appearance': 1.0, 'depth': 1.0, 'length': 1.0, 'onset': 1.0, 'response': 1.0, 'view': 1.0} |
| Two materially diverse formal cases | PASS | Seeds42,98 differ in multiple physical/visual parameters while retaining the phenomenon. |
| Shared nuisance and exact prompts | PASS | Within-pair scene/camera/appearance are fixed, prompts retain identical incidental setup. |
| Disjoint sharding and quota | PASS | {'count': 8, 'overlaps': [], 'seeds_probed_per_shard': 20000} |
| Safe resume and fail-closed runtime audit | PASS | Successful compatible resume and rejected incompatible resume logs; runtime manifest audit and index; independent decoded artifact audit. |

## Commands and artifacts checked

- Generator tests, canonical100000-case scaling audit, native batch generation through runtime-provenance wrapper, compatible/incompatible resume, clean-source reproduction and independent decoded/physics/contact checks. Commands and actual runtime versions are retained in witness and review-evidence logs.
- `review-evidence/independent.json`, `mesh.json`, `scale.json`, `reproduction-validated.json`, `browser-media.json`, `six-axis-independent.json`, `browser.json`, `visual.json`, `public.json`.
- `packet-manifest.json` inventories the public packet; `native-media.json` binds native release assets; case manifests bind formal source outputs.

## Re-review requirements

Owner reviews this exact-head packet before any Sara submission. A changed source head or changed formal media requires fresh applicable audits and updated checksums. No Sara form has been opened, filled or submitted.
