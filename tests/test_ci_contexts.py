"""AC 4 — the workflow's jobs and the required contexts agree exactly.

`ops/branch-protection.json` lists required checks by their **display name**,
and the file is inert until somebody re-applies it with `gh api -X PUT`. So
there are two ways to lose the gate, and this closes the tracked half:

* Rename or add a job in `ci.yml` without updating the contexts array and the
  protection rule waits forever for a check that will never report — every PR
  hangs, and `ops/README.md` warns about it in prose. Prose does not fail a
  build.
* Typo a context ("Web app" vs "Web App") and you get the same hang, from a
  file that looks correct at a glance.

**Set equality, not containment.** Containment passes in exactly the typo case
above, which is the failure worth catching.

The comparison lives in module-level pure functions so the honesty check —
"does this actually go red?" — is itself a test against `tmp_path`, rather than
something a human has to prove once by editing the tracked workflow and
watching it fail.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"
BRANCH_PROTECTION = REPO_ROOT / "ops" / "branch-protection.json"


def job_display_names(workflow: Path) -> set[str]:
    """The names GitHub reports each job under — which is what a context is.

    A job may legally omit `name:`, in which case the check reports under the
    job key, so the fallback is not cosmetic.

    (Aside for whoever debugs this: PyYAML parses a workflow's `on:` key as
    boolean True under YAML 1.1. Harmless here — only `jobs` is read.)
    """
    doc: dict[str, Any] = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    return {job.get("name", key) for key, job in doc["jobs"].items()}


def required_contexts(protection: Path) -> set[str]:
    doc: dict[str, Any] = yaml.safe_load(protection.read_text(encoding="utf-8"))
    contexts: list[str] = doc["required_status_checks"]["contexts"]
    return set(contexts)


def diff_message(ci: set[str], protection: set[str]) -> str:
    """Name which side carries the extra entry — the whole point on a typo."""
    only_in_ci = sorted(ci - protection)
    only_in_protection = sorted(protection - ci)
    return (
        "ci.yml's job names and ops/branch-protection.json's required contexts "
        "must match exactly.\n"
        f"  jobs in ci.yml with no required context: {only_in_ci}\n"
        f"  required contexts with no matching job:  {only_in_protection}\n"
        "A context naming no job leaves every PR pending forever on a check "
        "that never reports. Remember the protection file is inert until "
        "re-applied with `gh api -X PUT` — editing it alone changes nothing."
    )


# ─── The real assertion ──────────────────────────────────────────────────────


def test_ci_jobs_and_required_contexts_match_exactly() -> None:
    ci = job_display_names(CI_WORKFLOW)
    protection = required_contexts(BRANCH_PROTECTION)

    assert ci == protection, diff_message(ci, protection)


def test_step_names_are_not_collected_as_jobs() -> None:
    """Proves the parser is structure-aware rather than grepping quoted strings.

    These are all *step*-level names in ci.yml. A regex over the file would
    happily hand them back as contexts.
    """
    names = job_display_names(CI_WORKFLOW)

    for step_name in ("Gitleaks", "Install", "Mypy"):
        assert step_name not in names, (
            f"{step_name!r} is a step name, not a job name. The parser is "
            "reading the wrong level of the workflow."
        )


# ─── The honesty proof: it goes red when it should ───────────────────────────


def test_the_comparison_fails_on_a_typod_context(tmp_path: Path) -> None:
    """A typo is the failure containment would miss, so it is the one pinned."""
    workflow = tmp_path / "ci.yml"
    workflow.write_text(
        "jobs:\n  python:\n    name: Lint, types, tests\n  web:\n    name: Web app\n",
        encoding="utf-8",
    )
    protection = tmp_path / "protection.json"
    protection.write_text(
        '{"required_status_checks": {"contexts": ["Lint, types, tests", "Web App"]}}',
        encoding="utf-8",
    )

    ci = job_display_names(workflow)
    contexts = required_contexts(protection)

    assert ci != contexts, "a case typo must not compare equal"

    message = diff_message(ci, contexts)
    assert "'Web app'" in message, "the message must name the job side's entry"
    assert "'Web App'" in message, "the message must name the protection side's entry"


def test_containment_would_have_passed_the_same_typo(tmp_path: Path) -> None:
    """Pins *why* the assertion is equality — the weaker check is silent here."""
    workflow = tmp_path / "ci.yml"
    workflow.write_text("jobs:\n  python:\n    name: Web app\n", encoding="utf-8")
    protection = tmp_path / "protection.json"
    protection.write_text(
        '{"required_status_checks": {"contexts": ["Web app", "Web App"]}}', encoding="utf-8"
    )

    ci = job_display_names(workflow)
    contexts = required_contexts(protection)

    assert ci <= contexts, "containment passes — which is the bug"
    assert ci != contexts, "equality catches it"


def test_a_job_without_a_name_reports_under_its_key(tmp_path: Path) -> None:
    workflow = tmp_path / "ci.yml"
    workflow.write_text("jobs:\n  secrets:\n    runs-on: ubuntu-latest\n", encoding="utf-8")

    assert job_display_names(workflow) == {"secrets"}
