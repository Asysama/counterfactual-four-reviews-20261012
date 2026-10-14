# 摇摆舟同步对照 — owner revision

Decision: NOT VERIFIED (final visual/browser/public checks pending)

Exact head: `2c75089e1d46863035970236a3dd5bba83a2ac59`

两只相同配重、相同朝向的舟同步释放；正常同向，异常只有右舟反向。采用较高视角观察。

Formal accepted target: exactly two fully rendered cases, seeds42 and98; native2048×2048,24fps,120frames,5s. Declared population target100000; scale.json is static recipe evidence, never a claim of100000 rendered videos.

Six hard gates: native output, object-only mask, rendered scale diversity, official environment, exact decoded matched prefix and semantic consistency. Independent decoded/physical evidence: review-evidence/independent.json; evaluated swept mesh evidence: review-evidence/mesh.json; actual render provenance: runtime-witness.json and runtime-witness-index.json. Source/runtime pinning and all artifact hashes are retained.

Mask includes only the physically violating sphere/cards/right boat; support, ribbon, left reference boat, background and all shadows are excluded. Overlay is formed by replacing exact active mask pixels with red. Browser RGB/overlay are explicitly lossy1024 review derivatives; native ground truth remains authoritative.

Scale and operating evidence: review-evidence/scale.json, axis-probes/, tests.log, resume.log, incompatible-resume.log. Reproduction evidence: reproduction-validated.json; exact trajectories/recipes and masks, measured sparse renderer RGB differences reported explicitly.

Measured clean-source reproduction (seed42): exact recipe, trajectory and binary mask. RGB differences are sparse GPU-renderer rounding, not dynamics differences.

| Stream | Maximum channel difference | Total changed pixel instances across120frames | Maximum changed pixels in one frame |
|---|---:|---:|---:|
| true/video.mp4 | 2 | 7 | 2 |
| counterfactual_rocking_spin_chiral_coupling_sign_reversal/video.mp4 | 1 | 3 | 1 |
| counterfactual_rocking_spin_chiral_coupling_sign_reversal/mask.mp4 | 0 | 0 | 0 |
| counterfactual_rocking_spin_chiral_coupling_sign_reversal/mask_overlay.mp4 | 1 | 3 | 1 |

Within each submitted True/CF pair, pre-intervention equality still has zero tolerance.

Independent direction evidence: review-evidence/direction.json; composite inertia plus no-slip Newton-Euler solve under declared wood/brass densities and static friction0.60. Mirror and step-halving checks. This validates spin direction plausibility, not exact transient agreement with the rendered reduced modal model. Both rendered branches use physical/video time ratio0.25.
