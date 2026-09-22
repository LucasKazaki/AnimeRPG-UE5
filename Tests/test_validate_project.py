from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Scripts"))
from validate_project import validate

INPUTS = (
    "AnimeRPGProject.uproject", "Config/DefaultInput.ini", "Config/DefaultEngine.ini",
    "Source/AnimeRPGProject.Target.cs", "Source/AnimeRPGProjectEditor.Target.cs",
    "Source/AnimeRPGProject/AnimeRPGProject.Build.cs",
    "Source/AnimeRPGProject/AnimeRPGCharacter.cpp",
    "Source/AnimeRPGProject/AnimeRPGGameMode.cpp",
)


class SourceContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ue-source-contract-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        for relative in INPUTS:
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((ROOT / relative).read_bytes())

    def replace(self, relative: str, before: str, after: str) -> None:
        path = self.root / relative
        original = path.read_text(encoding="utf-8")
        self.assertIn(before, original)
        path.write_text(original.replace(before, after), encoding="utf-8")

    def test_checked_in_contract(self) -> None:
        self.assertEqual(validate(self.root), [])

    def test_missing_editor_target(self) -> None:
        (self.root / "Source/AnimeRPGProjectEditor.Target.cs").unlink()
        self.assertTrue(validate(self.root))

    def test_invalid_descriptor(self) -> None:
        (self.root / "AnimeRPGProject.uproject").write_text("[]", encoding="utf-8")
        self.assertIn("JSON object", "\n".join(validate(self.root)))

    def test_malformed_json(self) -> None:
        (self.root / "AnimeRPGProject.uproject").write_text("{", encoding="utf-8")
        self.assertIn("Invalid project JSON", "\n".join(validate(self.root)))

    def test_module_target_mismatch(self) -> None:
        self.replace("Source/AnimeRPGProject.Target.cs", 'Add("AnimeRPGProject")', 'Add("WrongModule")')
        self.assertIn("does not include module", "\n".join(validate(self.root)))

    def test_missing_dash_mapping(self) -> None:
        self.replace("Config/DefaultInput.ini", 'ActionName="Dash"', 'ActionName="NotDash"')
        self.assertIn("Missing Action mapping: Dash", validate(self.root))

    def test_wrong_input_class(self) -> None:
        self.replace("Config/DefaultInput.ini", "/Script/Engine.PlayerInput", "/Script/Other.Input")
        self.assertIn("Legacy input contract", "\n".join(validate(self.root)))

    def test_wrong_game_mode(self) -> None:
        self.replace("Config/DefaultEngine.ini", "AnimeRPGProject.AnimeRPGGameMode", "Other.GameMode")
        self.assertIn("GlobalDefaultGameMode", "\n".join(validate(self.root)))

    def test_engine_version_preflight(self) -> None:
        engine = Path(self.temp.name) / "engine with spaces"
        version = engine / "Engine/Build/Build.version"
        version.parent.mkdir(parents=True)
        batch = engine / "Engine/Build/BatchFiles/Build.bat"
        batch.parent.mkdir()
        batch.write_text("@echo fixture only\n", encoding="utf-8")
        association = json.loads((self.root / "AnimeRPGProject.uproject").read_text())["EngineAssociation"]
        major, minor = map(int, association.split("."))
        version.write_text(json.dumps({"MajorVersion": major, "MinorVersion": minor}), encoding="utf-8")
        self.assertEqual(validate(self.root, engine), [])
        version.write_text(json.dumps({"MajorVersion": major, "MinorVersion": minor + 1}), encoding="utf-8")
        self.assertIn("Engine version mismatch", "\n".join(validate(self.root, engine)))
        version.write_text("[]", encoding="utf-8")
        self.assertIn("Cannot verify installed engine", "\n".join(validate(self.root, engine)))

    def test_missing_installed_engine(self) -> None:
        self.assertIn("missing Engine/Build", "\n".join(validate(self.root, self.root / "missing")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
