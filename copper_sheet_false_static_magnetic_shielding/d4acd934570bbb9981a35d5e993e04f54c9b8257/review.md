# 磁铁与铜板 — owner revision

Decision: NOT VERIFIED (final visual/browser/public checks pending)

Exact head: `d4acd934570bbb9981a35d5e993e04f54c9b8257`

放大钢球偏转，露出红蓝 N/S 两极；增加固定竖直刻线，重排支架与铜板导轨。

Formal accepted target: exactly two fully rendered cases, seeds42 and98; native2048×2048,24fps,120frames,5s. Declared population target100000; scale.json is static recipe evidence, never a claim of100000 rendered videos.

Six hard gates: native output, object-only mask, rendered scale diversity, official environment, exact decoded matched prefix and semantic consistency. Independent decoded/physical evidence: review-evidence/independent.json; evaluated swept mesh evidence: review-evidence/mesh.json; actual render provenance: runtime-witness.json and runtime-witness-index.json. Source/runtime pinning and all artifact hashes are retained.

Mask includes only the physically violating sphere/cards/right boat; support, ribbon, left reference boat, background and all shadows are excluded. Overlay is formed by replacing exact active mask pixels with red. Browser RGB/overlay are explicitly lossy1024 review derivatives; native ground truth remains authoritative.

Scale and operating evidence: review-evidence/scale.json, axis-probes/, tests.log, resume.log, incompatible-resume.log. Reproduction evidence: reproduction-validated.json; exact trajectories/recipes and masks, measured sparse renderer RGB differences reported explicitly.

