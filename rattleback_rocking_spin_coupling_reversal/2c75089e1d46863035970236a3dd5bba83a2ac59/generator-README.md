# rattleback_rocking_spin_coupling_reversal

A rattleback converts rocking into the wrong spin direction

True: Two identical boat-shaped rattlebacks with identical fixed diagonal brass weights stand side by side on separate solid tables, tilted equally on retractable supports. Both supports withdraw together, releasing the same initial rocking. Both boats gradually develop rotation in the same direction.

Counterfactual: Two identical boat-shaped rattlebacks with identical fixed diagonal brass weights stand side by side on separate solid tables, tilted equally on retractable supports. Both supports withdraw together, releasing the same initial rocking. The left reference boat develops rotation, but the right boat develops rotation in the opposite direction despite its identical shape, weights, orientation and release; only its rocking-to-spin coupling is reversed.

Read DESIGN.md before source. Blender Workbench renders deterministic 3D geometry;
physics is supplied by the declared generator-owned model, never claimed as native Blender physics.
Official Linux x86-64 Python3.11, bpy4.5.3. System libraries: ffmpeg, libxfixes3,
libxi6, libxrender1, libxxf86vm1, libgl1, libegl1, libxkbcommon0; a headless OpenGL
session may be provided by xvfb-run. Install `pip install -r requirements.txt`.

Generate: `python examples/generate.py --num-cases 2 --seeds 42,98 --output /absolute/new-output`.
Audit: `python examples/audit.py --case /absolute/case-directory`.
Reproduce: `python examples/reproduce.py --case /absolute/case-directory --output /absolute/new-output`.
Compare: `python examples/compare.py ORIGINAL REBUILT`.
Scale: `python examples/audit_scaling.py . --output /absolute/scale-audit.json`.
Probes: `python examples/probe_axes.py --output /absolute/new-probes`.
Native formal:2048x2048,24fps,120frames,5s,H264. --smoke is512 and never formal acceptance.
Strict binary RGB object-only masks exclude shadows and unrelated objects; overlays change only
active mask pixels to red. Browser1024-square YUV420 copies are explicitly lossy review derivatives.
Each seed samples geometry, physical response, event timing, cross-section, appearance and viewpoint
once, shared within its pair. CGC-v1 target100000 accepted cases, one million unique final recipes;
static auditing is NOT a100000-video claim. Deterministic sharding, manifests and guarded resume.
Intervention is the actual operator event; mask starts at first decoded divergence, while evidence
is recomputed from the physical outcome. Prompts independently describe complete branch outcomes.
Archive formal media, manifests, successful runtime witnesses and indices before stopping compute.
No external assets or files above this directory are required for standalone generation.
Status: NOT VERIFIED until current-head independent formal, physical, visual and scale checks pass.
Code/data license:CC BY-NC4.0, Hippocampal, Inc.; LICENSE and CITATION.cff bundled.
