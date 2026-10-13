# PR 665 generator review

**Decision: PASS — contributor self-check. Owner review pending; no Sara application submitted.**

**Reviewed head:** `d8b7b26c29a98bc5392e859e233ce67fcb747961`
**Generator:** `air_gap_plate_attraction_reversal`

[Review policy pinned to dev3d6eec3ef2d962a2514989463b254273feddb909](https://github.com/hipo-dev/counterfactual-data/blob/3d6eec3ef2d962a2514989463b254273feddb909/.agents/skills/review-counterfactual-generator/SKILL.md). All six hard gates and applicable runtime/scale/visual requirements were applied.

**Generator correctness:** PASS
**Runtime-provenance policy scope:** NEW/REPLACEMENT
**Runtime provenance:** PASS
**Declared scaling target:** 100000 accepted recipes; canonical static audit covers 100000 seeds.
**Declared-target scale readiness:** PASS under the documented bounded model domain.
**Production readiness:** READY for the declared contract. Exactly two representative cases are formally rendered; this is not a claim that 100000 videos were rendered.

## Blocking findings

None in this reviewed packet. Any source or artifact change invalidates this decision until affected evidence is regenerated and rechecked.

## Six-gate result

| Gate | Result | Evidence |
|---|---|---|
| Output contract | PASS | Native2048²,24fps,120frames,5s,H264; all32 streams across the four generators are independently decoded. This generator: [independent decoded/physics audit](review-evidence/air_gap_plate_attraction_reversal-independent.json). |
| Violating-object-only mask | PASS | Strict RGB0/255, identical channels, exact red overlay/off-mask equality, active through final frame; no shadows rendered; target identity and occlusion checked: [independent decoded/physics audit](review-evidence/air_gap_plate_attraction_reversal-independent.json), [all-frame evaluated geometry audit](review-evidence/air_gap_plate_attraction_reversal-geometry.json), [visual inspection](review-evidence/visual-inspection.json). |
| Real scaling | PASS | Four primary axes (length,response,onset,depth) and two nuisance axes (appearance,view),10 buckets each; actual low/high renders for all six: [100000-recipe canonical audit](review-evidence/air_gap_plate_attraction_reversal-scale.json), [controlled rendered axis probes](review-evidence/air_gap_plate_attraction_reversal-axis-probes/axis-probes.json); [independent image hash and low/high pixel comparison](review-evidence/air_gap_plate_attraction_reversal-six-axis-independent.json). |
| Official unpatched environment | PASS | Clean exact source; official Python3.11/bpy4.5.3, NVIDIA OpenGL, actual encoder hashes: [runtime witness](runtime-witness.json). |
| Decoded matched control | PASS | Every RGB frame before intervention is exactly equal; post-intervention divergence and first mask frame independently located: [independent decoded/physics audit](review-evidence/air_gap_plate_attraction_reversal-independent.json). |
| Semantic consistency | PASS | Title, README, both standalone prompts, scoring, operator and both accepted videos agree: [visual inspection](review-evidence/visual-inspection.json), physical witnesses below. |

## Production-quality behavioral baseline

| Check | Result | Evidence |
|---|---|---|
| True completes the correct prompt outcome | PASS | Independent physical witnesses, both whole clips and native completion frames: [independent decoded/physics audit](review-evidence/air_gap_plate_attraction_reversal-independent.json), [visual inspection](review-evidence/visual-inspection.json), [actual browser receipt](review-evidence/actual-browser-playback.json). |
| Counterfactual completes exactly one declared error | PASS | Pair-shared scene and conditions; only the documented operator differs. [independent decoded/physics audit](review-evidence/air_gap_plate_attraction_reversal-independent.json), [visual inspection](review-evidence/visual-inspection.json). |
| Both prompts stand alone and exactly describe their videos | PASS | Prompt files equal metadata and were visually checked on seeds42 and98: [visual inspection](review-evidence/visual-inspection.json). |
| Branch labels, setup and final visibility | PASS | Hash binding, exact prefix, actual behavior, complete 5-second playback and start/evidence/end seeks: [independent decoded/physics audit](review-evidence/air_gap_plate_attraction_reversal-independent.json), [actual browser receipt](review-evidence/actual-browser-playback.json). |
| No unintended interpenetration or disconnected supports | PASS | All-frame evaluated target/support bounds plus native consecutive contact/edge crops and whole-clip inspection: [all-frame evaluated geometry audit](review-evidence/air_gap_plate_attraction_reversal-geometry.json), [visual inspection](review-evidence/visual-inspection.json). |

## Timebase and playback integrity

| Check | Result | Evidence |
|---|---|---|
| Time mapping and solver steps | PASS | Metadata records source_dt × outer steps/frame = physical_dt; physical_dt ×24fps equals the declared ratio. [independent decoded/physics audit](review-evidence/air_gap_plate_attraction_reversal-independent.json). |
| Playback rate | PASS | Copper, electrostatic shuttle and air-gap cards use ratio1. Rattleback explicitly uses ratio0.25 (4x slow motion), shared by both branches. |
| Internal substeps | NOT APPLICABLE | The recorded40 or120 outer numerical updates/frame are not multiplied by an additional hidden engine substep count. |

## Optional simulator profile

NOT APPLICABLE. These generators explicitly use generator-owned reduced physical models and Blender Workbench rendering. No simulator-native dynamics claim is made. The rattleback is an averaged small-angle modal model with convex-contact reconstruction, not a full Newton–Euler solution; the airflow model stipulates a symmetric-gap pressure coefficient, not a CFD result.

## Semantic matrix

| Title / README | True prompt | CF prompt | Scoring / operator | Rendered behavior | Result |
|---|---|---|---|---|---|
| `air_gap_plate_attraction_reversal` / DESIGN.md; seed42 | Two light rigid cards hang from supported hinges on either side of a narrow gap. A connected air tank opens its valve and a centered upward nozzle directs air through the gap. The lower sides of the cards move inward and settle closer together without touching. | Two light rigid cards hang from supported hinges on either side of a narrow gap. A connected air tank opens its valve and a centered upward nozzle directs air through the gap. The net gap pressure difference is wrongly reversed, so the lower sides move outward and settle farther apart without touching. | `gap_pressure_difference_sign_reversal`; metadata scoring contract | Measured intervention 24, visible divergence 24, evidence 26; complete final state inspected | PASS |
| `air_gap_plate_attraction_reversal` / DESIGN.md; seed98 | Two light rigid cards hang from supported hinges on either side of a narrow gap. A connected air tank opens its valve and a centered upward nozzle directs air through the gap. The lower sides of the cards move inward and settle closer together without touching. | Two light rigid cards hang from supported hinges on either side of a narrow gap. A connected air tank opens its valve and a centered upward nozzle directs air through the gap. The net gap pressure difference is wrongly reversed, so the lower sides move outward and settle farther apart without touching. | `gap_pressure_difference_sign_reversal`; metadata scoring contract | Measured intervention 28, visible divergence 28, evidence 29; complete final state inspected | PASS |

## Successful-render runtime provenance

| Check | Result | Evidence |
|---|---|---|
| Accepted cases have exactly one successful witness | PASS | [Case mapping](runtime-witness-index.json), seeds42 and98. |
| Exact source, clean worktree, command, dependencies, actual components | PASS | [Successful witness](runtime-witness.json), each case renderer-runtime.json and formal manifests. |
| Delivered artifacts match render hashes | PASS | Per-case manifests, packet manifest and external-native-media.json; all public files are anonymously downloaded and SHA-256 checked. |
| Independent reproduction | PASS | Fresh seed42 render with its own [successful witness](review-evidence/reproduction-provenance/runtime-witness.json); all120 frames in each stream independently compared; trajectories and formal mask are exact. Sparse RGB rounding, if present, is bounded to two8-bit levels, at most4 pixels/frame and32 pixels/stream; the linked receipt records every actual difference. This does not relax exact within-pair prefixes. [independent decoded reproduction validation](review-evidence/air_gap_plate_attraction_reversal-reproduction-validated.json), [reproduction runtime audit](review-evidence/air_gap_plate_attraction_reversal-reproduce-runtime.json). |
| Nested runtime | NOT APPLICABLE | bpy executes in the recorded official interpreter; no unrecorded embedded interpreter is used. |

## Client-facing artifact consistency

| Check | Result | Evidence |
|---|---|---|
| Formal white-on-black binary mask | PASS | [independent decoded/physics audit](review-evidence/air_gap_plate_attraction_reversal-independent.json), [visual inspection](review-evidence/visual-inspection.json). |
| Consistent red overlay limited to mask | PASS | Native all-frame exact checks: [independent decoded/physics audit](review-evidence/air_gap_plate_attraction_reversal-independent.json). Browser RGB/overlay derivatives are labelled lossy and are not formal pixel labels. |
| Browser derivatives and playback/seek | PASS | [independent browser-media decode](review-evidence/air_gap_plate_attraction_reversal-browser-media.json), [actual browser receipt](review-evidence/actual-browser-playback.json). All eight displayed streams played through5s; start, evidence and last-frame seeks checked. |

## Scale-readiness result

| Check | Result | Evidence |
|---|---|---|
| Contract, profile coverage, deterministic signatures and sharding | PASS | CGC-v1,1million profile space;100000 static seeds accepted without rejection: [100000-recipe canonical audit](review-evidence/air_gap_plate_attraction_reversal-scale.json). |
| Real independent physical axes reach geometry/dynamics/event time | PASS | Four physical axes and separate nuisance controls; pair-shared recipes and actual low/high images: [controlled rendered axis probes](review-evidence/air_gap_plate_attraction_reversal-axis-probes/axis-probes.json). |
| No dead appearance/view axis | PASS | Both nuisance axes have explicit low/high rendered evidence; appearance changes shared matte floor material. [controlled rendered axis probes](review-evidence/air_gap_plate_attraction_reversal-axis-probes/axis-probes.json). |
| Two formal cases materially differ | PASS | Both scenes and trajectories compared beyond camera/color: [visual inspection](review-evidence/visual-inspection.json), case metadata. |
| Bounded operation, accepted quota and safe resume | PASS | Two accepted cases; compatible resume re-audits, mismatched quota rejects; [resume log](review-evidence/air_gap_plate_attraction_reversal-resume.log), [three-scene live-resource count check](review-evidence/air_gap_plate_attraction_reversal-bounded-resources.json). |
| Runtime and decoded checks fail closed | PASS | Official tests, canonical scale audit, runtime audit/index and separate independent decoded audit all pass at this head. [independent decoded/physics audit](review-evidence/air_gap_plate_attraction_reversal-independent.json). |

## Independent physical measurements

```json
[
  {
    "case_id": "air_gap_plate_attraction_reversal_00000042",
    "witnesses": {
      "pressure_drop_Pa": 4.42130871,
      "equilibrium_angle": 0.11664848597870804,
      "true_final_angle": 0.11665392922133466,
      "cf_final_angle": -0.11665392922133466,
      "minimum_gap": 0.7708025601449368,
      "independent_ode_errors": [
        2.4600904646732147e-11,
        2.4600904646732147e-11
      ],
      "evidence_frame": 26
    }
  },
  {
    "case_id": "air_gap_plate_attraction_reversal_00000098",
    "witnesses": {
      "pressure_drop_Pa": 6.697367040000003,
      "equilibrium_angle": 0.17567434043714641,
      "true_final_angle": 0.17566225251772594,
      "cf_final_angle": -0.17566225251772594,
      "minimum_gap": 0.46577778244626866,
      "independent_ode_errors": [
        5.85942683262175e-11,
        5.85942683262175e-11
      ],
      "evidence_frame": 29
    }
  }
]
```

## Commands and artifacts checked

Official compile,pytest,CLI help,100k scale audit, controlled axis renders, provenance-wrapped two-case native generation, runtime audit/index, compatible/incompatible resume, independent native decode and physics, evaluated geometry, bounded scene construction, fresh provenance-wrapped seed42 reproduction and independent pixel/trajectory comparison, independent browser media decode, actual Chrome playback/seeks, and anonymous public HTTP hashes.

Review URL: https://asysama.github.io/counterfactual-four-reviews-20261012/air_gap_plate_attraction_reversal/d8b7b26c29a98bc5392e859e233ce67fcb747961/index.html

## Re-review requirements

Keep these source and artifact hashes fixed. Regenerate affected native media, witnesses, derivatives, manifests, independent checks and browser receipts after any source change. Owner review is still pending; do not submit to Sara until explicitly authorized.

## Remediated finding

The superseded33054c5 render exposed a real hose/card intersection at seed42,CF frame27. Currentd8b7b26 routes the hose behind the entire card sweep and below the bottoms. Both formal cases and the reproduction were freshly rendered at this head. The four-test official suite includes complete-sweep clearance across representative and corner recipes; an independent actual-mesh BVH checks960 card/hose poses with zero intersections. [evaluated-mesh collision receipt](review-evidence/air_gap_plate_attraction_reversal-hose-bvh.json).

## Independent-run reproduction precision

Cross-run RGB bitwise equality and an initial one-level bound were extra diagnostics, not the matched-pair gate. Their failures are retained; the final explicit two-level sparse-pixel criterion is enforced by validate-reproduction.py. Copper and electrostatic and rattleback independent runs differed only at sparse pixels by1–2 eight-bit levels; exact per-frame locations/counts and original/reproduced SHA-256 values are preserved in [raw independent reproduction diagnostic](review-evidence/air_gap_plate_attraction_reversal-reproduction-diagnostic.json). Exact dynamics, recipe, formal mask and each pair’s pre-intervention RGB prefix remain mandatory. No uncommitted source patch, monkey patch or unofficial dependency substitution was applied during current-head verification.
