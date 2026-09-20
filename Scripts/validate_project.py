#!/usr/bin/env python3
"""Check the small UE source scaffold without installing or invoking Unreal.

This is deliberately NOT a C++ compiler, UnrealHeaderTool, or packaged-build test.
An optional engine-root check compares the actual Build.version with the descriptor.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def validate(root: Path, engine_root: Path | None = None) -> list[str]:
    errors: list[str] = []

    def text(relative: str) -> str:
        try:
            return (root / relative).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            errors.append(f"Cannot read {relative}: {exc}")
            return ""

    try:
        descriptor = json.loads(text("AnimeRPGProject.uproject"))
    except json.JSONDecodeError as exc:
        return errors + [f"Invalid project JSON: {exc}"]
    if not isinstance(descriptor, dict):
        return errors + ["Project descriptor must be a JSON object."]
    modules = descriptor.get("Modules")
    if not isinstance(modules, list) or len(modules) != 1:
        return errors + ["This scaffold requires exactly one runtime module."]
    module = modules[0]
    if not isinstance(module, dict) or module.get("Type") != "Runtime":
        return errors + ["The declared module must have Type Runtime."]
    name = module.get("Name", "")
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        return errors + ["Invalid module name."]
    if descriptor.get("FileVersion") != 3:
        errors.append("Expected project descriptor FileVersion 3.")

    directory = f"Source/{name}"
    rules = text(f"{directory}/{name}.Build.cs")
    if not re.search(rf"class\s+{re.escape(name)}\s*:\s*ModuleRules", rules):
        errors.append("ModuleRules class does not match the declared module.")
    for suffix, kind in (("", "Game"), ("Editor", "Editor")):
        target = text(f"Source/AnimeRPGProject{suffix}.Target.cs")
        if not re.search(rf"Type\s*=\s*TargetType\.{kind}\s*;", target):
            errors.append(f"Missing {kind} target type.")
        if not re.search(rf'ExtraModuleNames\.Add\(\s*"{re.escape(name)}"\s*\)', target):
            errors.append(f"{kind} target does not include module {name}.")

    character = text(f"{directory}/AnimeRPGCharacter.cpp")
    inputs = text("Config/DefaultInput.ini")
    for kind in ("Axis", "Action"):
        bindings = set(re.findall(rf'Bind{kind}\(\s*TEXT\(\s*"([^"]+)"', character))
        mappings = set(re.findall(rf'{kind}Name\s*=\s*"([^"]+)"', inputs))
        if not bindings:
            errors.append(f"No {kind} bindings found in the character.")
        for binding in sorted(bindings - mappings):
            errors.append(f"Missing {kind} mapping: {binding}")
    for setting, value in (("DefaultPlayerInputClass", "/Script/Engine.PlayerInput"),
                           ("DefaultInputComponentClass", "/Script/Engine.InputComponent")):
        if not re.search(rf"^{setting}\s*=\s*{re.escape(value)}\s*$", inputs, re.MULTILINE):
            errors.append(f"Legacy input contract requires {setting}={value}.")

    engine = text("Config/DefaultEngine.ini")
    expected_mode = f"/Script/{name}.AnimeRPGGameMode"
    if not re.search(rf"^GlobalDefaultGameMode\s*=\s*{re.escape(expected_mode)}\s*$",
                     engine, re.MULTILINE):
        errors.append(f"GlobalDefaultGameMode must select {expected_mode}.")
    game_mode = text(f"{directory}/AnimeRPGGameMode.cpp")
    if not re.search(r"DefaultPawnClass\s*=\s*AAnimeRPGCharacter::StaticClass\(\)", game_mode):
        errors.append("Game mode does not select the native character.")

    association = descriptor.get("EngineAssociation")
    if not isinstance(association, str) or not association.strip():
        errors.append("EngineAssociation is missing.")
    if engine_root is not None:
        try:
            version = json.loads((engine_root / "Engine/Build/Build.version").read_text(
                encoding="utf-8-sig"))
            if not isinstance(version, dict):
                raise ValueError("Build.version must be a JSON object")
            major, minor = version["MajorVersion"], version["MinorVersion"]
            if type(major) is not int or type(minor) is not int:
                raise ValueError("MajorVersion and MinorVersion must be integers")
            if association != f"{major}.{minor}":
                errors.append(f"Engine version mismatch: project={association}, installed={major}.{minor}.")
        except (OSError, UnicodeError, ValueError, KeyError) as exc:
            errors.append(f"Cannot verify installed engine Build.version: {exc}")
        if not (engine_root / "Engine/Build/BatchFiles/Build.bat").is_file():
            errors.append("Installed engine is missing Engine/Build/BatchFiles/Build.bat.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--engine-root", type=Path)
    args = parser.parse_args()
    errors = validate(args.root.resolve(), args.engine_root)
    if errors:
        print("Source/preflight checks: FAIL", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Source/preflight checks: PASS. Unreal compilation and runtime were NOT run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
