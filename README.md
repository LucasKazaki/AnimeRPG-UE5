# AnimeRPGProject

A minimal Unreal Engine 5.8 third-person C++ foundation with one runtime module: `AnimeRPGProject`.

## Controls

- WASD: move
- Mouse: camera
- Space: jump
- Left Shift: dash

The native game mode selects `AAnimeRPGCharacter` as the default pawn. The character supplies a spring-arm third-person camera, controller-relative movement, jump, and a small launch-based dash. No Marketplace content or downloaded assets are required.

## Build

The editor target requires the Visual Studio C++ toolchain, Windows SDK, and a .NET Framework SDK 4.6 or newer (including `NETFXSDK` headers and libraries).

From Git Bash on Windows:

```sh
"C:/Program Files/Epic Games/UE_5.8/Engine/Build/BatchFiles/Build.bat" AnimeRPGProjectEditor Win64 Development "C:/AI/projects/AnimeRPG-UE5/AnimeRPGProject.uproject" -WaitMutex
```

Generated directories (`Binaries`, `Intermediate`, `Saved`, and `.vs`) are build artifacts and are not source deliverables.
