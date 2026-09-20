# AnimeRPGProject

**Experimental Unreal source prototype, not the production Astral Engine runtime.**
The separate [AnimeRPG repository](https://github.com/LucasKazaki/AnimeRPG) retains
its custom C++17 engine. Read [agent rules](AGENTS.md) and
[audit evidence](Docs/AUDIT-2026-09-19.md) before expanding this experiment.

## Implemented slice

One native runtime module provides an ACharacter, controller-relative locomotion,
a spring-arm third-person camera, jump, and a launch-based dash. A native game
mode selects the character. No Marketplace content or downloaded art is required.

| Input | Action |
|---|---|
| W, A, S, D | Move |
| Mouse | Rotate camera |
| Space | Jump |
| Left Shift | Dash in the movement direction, or forward from rest |

`Source/AnimeRPGProject` holds the module/character/game mode;
`Source/*.Target.cs` holds Game and Editor targets; `Config` holds checked-in
input and engine defaults; `AnimeRPGProject.uproject` declares the module.

## Source checks, no Unreal installation required

Python 3.10+:

```powershell
python Scripts/validate_project.py
python -m unittest discover -s Tests -p "test_*.py" -v
```

The checker validates basic module/target, input, and game-mode relationships.
Regression tests cover broken metadata, missing targets/mappings, and engine
version mismatches. CI runs these source checks only. They do **not** compile C++,
run UnrealHeaderTool, launch an Editor, or establish a working packaged game.

## Native build, separate gate

The checked-in EngineAssociation is `5.8`. Treat that as this project's recorded
requirement, not a claim about the latest engine or proof of an installed SDK.
Do not silently upgrade or downgrade it. Native work requires a compatible Unreal
installation on Windows, Visual Studio Game development with C++, Windows SDK,
and the .NET Framework SDK needed by the installed Unreal Build Tool.

From the repository root in PowerShell, set the actual installed engine path.
The preflight reads its Build.version before compiling both targets and stops
on the first failure:

```powershell
$engine = "C:\Program Files\Epic Games\UE_5.8"
python Scripts/validate_project.py --engine-root $engine
if ($LASTEXITCODE -ne 0) { throw "Source or engine preflight failed." }
$build = Join-Path $engine "Engine\Build\BatchFiles\Build.bat"
$project = Join-Path $PWD "AnimeRPGProject.uproject"
foreach ($target in @("AnimeRPGProjectEditor", "AnimeRPGProject")) {
    & $build $target Win64 Development $project -WaitMutex
    if ($LASTEXITCODE -ne 0) { throw "$target build failed with exit code $LASTEXITCODE." }
}
```

Retain the installed version, source commit, full output, and each exit code.
Open the project in a compatible editor for separate interactive validation.
A Game-target binary alone is not a cooked distribution.

## Scope and evidence limits

There is no checked-in production level, UI, combat, content pipeline, cooked
package, or full RPG in this repository. A suitable editor scene and native
movement/camera/jump/dash evidence remain separate requirements. This source
experiment does not authorize resuming paused Astral Engine game-content work.

Generated Binaries, DerivedDataCache, Intermediate, Saved, and .vs directories
are local build state, not source deliverables. The audit added no Source/,
Config/, engine-version, gameplay, or third-party dependency changes.

## License

No project-level open-source license is included. Source visibility is not a grant
of reuse rights. No license or external assets are added by this audit.
