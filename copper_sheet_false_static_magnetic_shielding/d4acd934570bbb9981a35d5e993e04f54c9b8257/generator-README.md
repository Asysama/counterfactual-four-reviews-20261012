# copper_sheet_false_static_magnetic_shielding

Ordinary copper falsely shields a static magnet

True: A steel sphere hangs beside a fixed red-and-blue permanent bar magnet with visible pole markings. A fixed vertical gauge shows the sphere is pulled sideways toward the magnet. An ordinary copper sheet slides along an overhead rail into the gap without touching the sphere or magnet. After the sheet stops, the sphere remains deflected toward the magnet.

Counterfactual: A steel sphere hangs beside a fixed red-and-blue permanent bar magnet with visible pole markings. A fixed vertical gauge shows the sphere is pulled sideways toward the magnet. An ordinary copper sheet slides along an overhead rail into the gap without touching the sphere or magnet. After the sheet stops, it wrongly blocks the steady magnetic attraction and the sphere returns toward the vertical gauge line.

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
