# AnimeRPGProject

> **Experimental Unreal Engine prototype.** This repository is a small, standalone C++ exploration and is not the production runtime for the custom Astral Engine / AnimeRPG project.

AnimeRPGProject is a minimal Unreal Engine 5.8 third-person foundation implemented as one native runtime module. It demonstrates character setup, controller-relative locomotion, a spring-arm camera, jumping, and a launch-based dash without Marketplace content or downloaded game assets.

## Implemented slice

- Native `ACharacter` subclass selected by a C++ game mode.
- Controller-relative `WASD` movement with movement-facing rotation.
- Spring-arm third-person camera with mouse-controlled yaw and pitch.
- Built-in character jump and an editable dash-strength property.
- Input and game defaults expressed in checked-in Unreal configuration files.
- Separate Game and Editor targets for the single `AnimeRPGProject` module.

## Controls

| Input | Action |
|---|---|
| `W` `A` `S` `D` | Move |
| Mouse | Rotate camera |
| `Space` | Jump |
| Left `Shift` | Dash in the current movement direction, or forward from rest |

## Project layout

| Location | Purpose |
|---|---|
| `Source/AnimeRPGProject` | Runtime module, character, and game mode |
| `Source/*.Target.cs` | Game and Editor build targets |
| `Config/DefaultInput.ini` | Keyboard and mouse mappings |
| `Config/DefaultEngine.ini` | Engine defaults |
| `AnimeRPGProject.uproject` | Unreal project and module metadata |

## Build

Requirements:

- Unreal Engine 5.8 installed on Windows
- Visual Studio with the Game development with C++ workload and Windows SDK
- The .NET Framework SDK required by the installed Unreal Build Tool, including `NETFXSDK` headers and libraries

From PowerShell in the repository root, adjust the engine path if Unreal is installed elsewhere:

```powershell
& "C:\Program Files\Epic Games\UE_5.8\Engine\Build\BatchFiles\Build.bat" `
    AnimeRPGProjectEditor Win64 Development `
    "$PWD\AnimeRPGProject.uproject" -WaitMutex
```

Replace `AnimeRPGProjectEditor` with `AnimeRPGProject` to compile the standalone Game target.

You can also open `AnimeRPGProject.uproject` in the Unreal Editor and allow it to generate local project files when prompted.

## Scope and validation

This is a source-only foundation rather than a vertical slice: it contains no production level, UI, combat, content pipeline, packaged build, or automated test suite. Compiling the Game and Editor targets is the current machine-checkable gate. A Game-target binary by itself is not a cooked distribution; interactive validation should run through a compatible Unreal Editor installation or a separately prepared package.

Generated directories such as `Binaries`, `DerivedDataCache`, `Intermediate`, `Saved`, and `.vs` are local build state and are not source deliverables.

## License

No project-level open-source license is currently included. The repository is available for source review, but reuse rights have not been granted.
