"""AC 14 — the two packaging facts no other test can see.

Both failures here are invisible locally and expensive later:

* Omitting `src/rpg_api` from the hatch `packages` list passes every test on
  this machine, because `pythonpath = ["src"]` puts the package on the path
  regardless. It fails with `ModuleNotFoundError` only on an installed
  environment — which is where `rpg-serve` runs.
* Leaving `--cov` naming only `rpg_core` means the coverage number silently
  stops describing the codebase as `rpg_api` grows. No `fail-under` is
  configured, so nothing else would ever complain.
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_PACKAGES = {"src/rpg_core", "src/rpg_api"}


def _pyproject() -> dict[str, Any]:
    with (REPO_ROOT / "pyproject.toml").open("rb") as fh:
        data: dict[str, Any] = tomllib.load(fh)
    return data


def _pytest_step_run_commands() -> list[str]:
    """Every `run:` string in the workflow that invokes pytest."""
    doc: dict[str, Any] = yaml.safe_load(
        (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    )
    commands: list[str] = []
    for job in doc["jobs"].values():
        for step in job.get("steps", []):
            run = step.get("run", "")
            if "pytest" in run:
                commands.append(run)
    return commands


def test_wheel_packages_both_source_packages() -> None:
    packages = _pyproject()["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]

    assert set(packages) == EXPECTED_PACKAGES, (
        "[tool.hatch.build.targets.wheel].packages must list both packages. "
        "Omitting one passes every test here — pythonpath = ['src'] masks it — "
        f"and fails with ModuleNotFoundError on an installed environment. Found: {packages}"
    )


def test_console_script_points_at_the_serve_entrypoint() -> None:
    scripts = _pyproject()["project"]["scripts"]

    assert scripts.get("rpg-serve") == "rpg_api.serve:main", (
        "The rpg-serve console script is spelled out in ops/README.md, README.md's "
        "Setup block, the CI smoke step, and the web app's unreachable panel. "
        f"Renaming it means renaming it in all of them. Found: {scripts}"
    )


def test_ci_coverage_measures_the_api_package() -> None:
    commands = _pytest_step_run_commands()

    assert commands, "No pytest step found in ci.yml — has the workflow been restructured?"
    assert any("--cov=rpg_api" in command for command in commands), (
        "ci.yml's pytest step must pass --cov=rpg_api. Without it the coverage "
        "number quietly stops describing the codebase as rpg_api grows, and no "
        f"fail-under is configured to catch it. Found: {commands}"
    )
