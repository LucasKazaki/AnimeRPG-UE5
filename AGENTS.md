# AnimeRPG-UE5 agent rules

This is a standalone Unreal source experiment. It is not the production runtime
for LucasKazaki/AnimeRPG, which retains custom C++17 Astral Engine. Do not infer
engine migration authority from this repository's existence or its UE version.

Read README.md, Docs/AUDIT-2026-09-19.md, and the active bounded task before edits.
Use an isolated branch and owned worktree. Preserve unrelated work and existing
input/module contracts. Lucas approves merges, engine changes, and scope expansion.
Do not change the engine version, install SDKs/plugins, download assets, publish
builds, or start another scheduler without explicit authorization.

`python Scripts/validate_project.py` and the Python unit tests check source
relationships only. A PASS does not mean UnrealHeaderTool, C++ compilation,
Editor/Game targets, Play In Editor, packaging, or gameplay passed.
Use --engine-root to compare the supplied installed engine's Build.version with
the descriptor before native work. Never guess a replacement engine version.

No production maps, combat, art pipeline, or packaged distribution are verified
here. Retain exact commands and exit codes, record missing native evidence, and
require independent review before an approved merge. Keep Astral Engine's
engine-first acceptance and paused game-content work separate from this experiment.
