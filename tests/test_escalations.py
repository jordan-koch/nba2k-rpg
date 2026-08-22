"""The escalation queue's pointer must be mechanical, not aspirational.

`ESCALATIONS.md` parks a decision against the moment that reopens it. That only
works if the moment is real: an entry naming an item id nobody will ever reach —
or a phase renumbered out from under it — is invisible to the drain while
looking perfectly correct on the page.

This is not a hypothetical failure, it is the one that motivated the queue.
`ROADMAP.md` parked three hypotheses in a paragraph, each said to have "a named
moment to re-decide", with the moments named only in the prose describing them.
Three more sat stranded in `_done/1.1-app-shell/`, a directory
`test_request_links.py` deliberately skips and nobody reopens. Every one of them
named a moment; not one of those pointers was checked by anything.

So the parser below is that check. It is a pure function over two strings,
proven red **and** green against `tmp_path` fakes in the
`test_layering.py:85-100` idiom — the obvious alternative, breaking a tracked
file and reverting it, is not available, because subagents have read-only git.

The dominant risk is this guard going silently vacuous: `for entry in parsed:
assert ...` over an empty list passes forever, and a format change is exactly
what would empty it. `test_the_entry_regex_matched_something` exists for that,
and the non-empty-slice assertions in the negative test exist for its subtler
cousin — a heading anchor that stops matching and takes its whole assertion
quietly out of service.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
QUEUE = REPO_ROOT / "ESCALATIONS.md"
ROADMAP = REPO_ROOT / "ROADMAP.md"

# Same shape as tests/test_request_links.py:26 — and note it carries capture
# groups, so `.findall()` returns tuples rather than blocks. Strip with `.sub()`
# and iterate with `.finditer()` + `.group(0)`.
FENCED_BLOCK = re.compile(r"^([ \t>]*)(`{3,}|~{3,}).*?^\1\2.*?$", re.DOTALL | re.MULTILINE)

HEADING = re.compile(r"^#{1,6}\s", re.MULTILINE)
TABLE_ROW = re.compile(r"^\|(?P<first>[^|]*)\|", re.MULTILINE)
PHASE_HEADING = re.compile(r"^###\s+(?P<phase>Phase \d+)\s+—", re.MULTILINE)
SECTION = re.compile(r"^##\s+(?P<name>Open|Resolved)\s*$", re.MULTILINE)
ENTRY = re.compile(r"^###\s+(?P<id>E-\d{3})\s+—\s+(?P<title>\S.*?)\s*$", re.MULTILINE)
# Every `###` heading, valid entry or not. Entry bodies are bounded by THIS and
# never by the next *valid* entry — see `parse_entries` for the corruption that
# distinction prevents.
ENTRY_LEVEL_HEADING = re.compile(r"^###\s+.*$", re.MULTILINE)
# Horizontal whitespace only, never `\s`. `\s*` after the label crosses the
# newline, so a field left blank swallows the FOLLOWING line as its value and
# the missing-field report then indicts two innocent fields for one blank one.
FIELD = re.compile(r"^-\s+\*\*(?P<name>[A-Za-z ]+):\*\*[ \t]*(?P<value>.*?)[ \t]*$", re.MULTILINE)

# An item id in ROADMAP.md's leading table cell: `1.3` or `H2`.
ITEM_ID = re.compile(r"^(?:\d+\.\d+|H\d+)$")
# A `:123` / `:123-456` citation suffix on a Source path, same idiom as
# tests/test_request_links.py's LINE_SUFFIX.
SOURCE_LINE_SUFFIX = re.compile(r":\d+(?:-\d+)?$")

REQUIRED_FIELDS = ("Bears on", "Parked", "Assumed", "Source", "Status")
STATUS_VALUES = frozenset({"open", "resolved"})

# The moment vocabulary is `item id | phase name | post-v1`. This is the third.
UNSCHEDULED = "post-v1"

MOMENT_RULE = (
    "Every entry's `Bears on:` must name a real roadmap moment — an item id "
    "(1.3, H2), a phase name (Phase 3), or post-v1. An entry naming a moment "
    "ROADMAP.md does not define can never be surfaced by the drain, which is "
    "the entire mechanism."
)


@dataclass(frozen=True)
class Entry:
    """One parsed queue entry. `section` is "" when none precedes it."""

    id: str
    title: str
    section: str
    fields: dict[str, str]


# ─── The parser, pure over strings ────────────────────────────────────────────


def _item_ids(text: str) -> set[str]:
    """Every leading table cell that *matches* an item-id pattern.

    Matching is the discriminator, not emptiness — findings F-27/F-06. The v1
    scope tables' data rows lead with bold text like `**Creation**`, and the
    open-questions table leads with `**[OPEN-2]**`, so a "skip the empty leading
    cells" rule would admit all of them as ids and the negative assertion below
    would be checking nothing.
    """
    ids: set[str] = set()
    for row in TABLE_ROW.finditer(text):
        cell = row["first"].strip()
        if ITEM_ID.fullmatch(cell):
            ids.add(cell)
    return ids


def known_moments(roadmap_text: str) -> frozenset[str]:
    """Every moment an entry may legally name.

    Returned with original casing on purpose. Casefolding the *set* would make
    the `H2 in moments` assertion below literally false; case-insensitivity
    belongs at the comparison site instead, and lives in `unknown_moments`.
    """
    body = FENCED_BLOCK.sub("", roadmap_text)
    moments = _item_ids(body)
    moments.update(match["phase"] for match in PHASE_HEADING.finditer(body))
    moments.add(UNSCHEDULED)
    return frozenset(moments)


def parse_entries(queue_text: str) -> list[Entry]:
    """Parse entries out of already-prepared text.

    Deliberately does **not** strip fenced blocks: the real pass strips them
    first, and the worked-example check feeds this the fenced block on its own.
    One function, two callers, no flag.

    **Bodies are bounded by the next `###` heading of any kind, valid or not.**
    Bounding them by the next *valid* entry instead is not a near-miss, it is a
    silent-corruption bug, and it was live here: a heading that misses the pinned
    format is skipped, so the previous entry's body ran on through it and
    `FIELD.finditer` picked up the malformed entry's bullets. Later keys win in a
    dict, so the intruder's `Source:` and `Assumed:` *overwrote* a real entry's —
    rewriting provenance in a permanent public record, and making every guard
    that did fire name the innocent entry above. `malformed_headings` is the
    other half of the fix; this is the half that stops the bleed.
    """
    sections = list(SECTION.finditer(queue_text))
    headings = list(ENTRY_LEVEL_HEADING.finditer(queue_text))
    entries: list[Entry] = []

    for index, heading in enumerate(headings):
        match = ENTRY.match(queue_text, heading.start())
        if match is None:
            # Malformed. Skipped rather than absorbed — and reported separately,
            # because a parser that quietly drops input is how this went wrong.
            continue

        stop = headings[index + 1].start() if index + 1 < len(headings) else len(queue_text)
        for section in sections:
            if heading.start() < section.start() < stop:
                stop = section.start()
                break

        body = queue_text[match.end() : stop]
        preceding = [s for s in sections if s.start() < heading.start()]

        entries.append(
            Entry(
                id=match["id"],
                title=match["title"],
                section=preceding[-1]["name"] if preceding else "",
                fields={f["name"]: f["value"] for f in FIELD.finditer(body)},
            )
        )

    return entries


def malformed_headings(queue_text: str) -> list[str]:
    """Every `###` heading inside the entry sections that isn't a valid entry.

    The entry sections hold entries and nothing else, so any `###` there that
    does not match the pinned format is malformed by definition. Without this,
    a mistyped heading is *invisible* rather than rejected — the entry count
    does not shrink, it merely fails to grow, so the seed-count floor can never
    notice it.

    This is what makes ESCALATIONS.md's own carve-out true: parking a question
    never blocks anything, but a broken *record* fails the build like any other
    malformed markdown.
    """
    sections = list(SECTION.finditer(queue_text))
    if not sections:
        return []

    first_section = sections[0].start()
    return [
        heading.group(0).strip()
        for heading in ENTRY_LEVEL_HEADING.finditer(queue_text)
        if heading.start() > first_section and ENTRY.match(queue_text, heading.start()) is None
    ]


def declared_moment(entry: Entry) -> str:
    """An entry's `Bears on:`, tolerant of the backticks the format table shows.

    The format table renders moments as code (`` `1.3` ``) and tells you to
    write `Source:` as code too, so a worker copying the register writes
    `` - **Bears on:** `1.3` `` — and a whole-string comparison then fails with
    "no such moment in ROADMAP.md", which asserts something false about the
    roadmap rather than about the formatting. Accept both; the header states
    which one is canonical.
    """
    return entry.fields.get("Bears on", "").strip().strip("`").strip()


def unknown_moments(queue_text: str, roadmap_text: str) -> list[tuple[str, str]]:
    """Every (entry id, moment) pair whose moment ROADMAP.md does not define."""
    known = {moment.lower() for moment in known_moments(roadmap_text)}
    return [
        (entry.id, declared_moment(entry))
        for entry in parse_entries(FENCED_BLOCK.sub("", queue_text))
        if declared_moment(entry).lower() not in known
    ]


def unresolved_sources(queue_text: str) -> list[tuple[str, str]]:
    """Every (entry id, `Source:`) whose path does not exist.

    `Source:` is the one pointer in a queue built on guarded pointers that
    nothing checked. It is written as a code span rather than a markdown link,
    so `test_request_links.py` cannot see it (its regex needs `](`), and the
    field guard asserts only that the field is *present*.

    Line numbers are deliberately not verified — `ROADMAP.md` is hand-edited and
    its numbering drifts — but the file ceasing to exist is the failure that
    actually strands a reader.
    """
    unresolved: list[tuple[str, str]] = []

    for entry in parse_entries(FENCED_BLOCK.sub("", queue_text)):
        raw = entry.fields.get("Source", "").strip().strip("`").strip()
        if not raw:
            continue
        # Take the path token only: a citation may carry a `:line` suffix and a
        # trailing commit or section gloss.
        path = SOURCE_LINE_SUFFIX.sub("", raw.split(" ")[0])
        if not (REPO_ROOT / path).exists():
            unresolved.append((entry.id, raw))

    return unresolved


def violation_message(violations: list[tuple[str, str]]) -> str:
    """The record — it has to name the file, the entry, and the rule."""
    return (
        f"ESCALATIONS.md has entries naming a moment ROADMAP.md does not define.\n{MOMENT_RULE}\n"
        + "\n".join(
            f"  {entry_id} bears on '{moment}' — no such moment in ROADMAP.md"
            for entry_id, moment in violations
        )
    )


def section_body(text: str, heading: str) -> str:
    """The text between `heading` and the next markdown heading of any level.

    The anchor is matched at a line boundary, not by substring: `### Out of
    scope` is a substring of `#### Out of scope`, so a plain `.find()` would
    silently re-aim at a demoted heading and keep passing while checking a
    different region — the same trap as `DESIGN.md` inside `GAME_DESIGN.md`.
    """
    match = re.search(rf"^{re.escape(heading)}\s*$", text, re.MULTILINE)
    if match is None:
        return ""
    following = HEADING.search(text, match.end())
    return text[match.end() : following.start()] if following else text[match.end() :]


def table_rows(body: str) -> list[str]:
    return [line for line in body.splitlines() if line.lstrip().startswith("|")]


# ─── Fixtures for the red/green proof ─────────────────────────────────────────
#
# Both fabricate the ROADMAP too, so the green case is hermetic (finding F-07) —
# a green that depended on the real roadmap would go red the day someone
# renumbered a row, for reasons having nothing to do with this guard.

FAKE_ROADMAP = """# Roadmap

### In scope — the engine

| | Why it can't be cut |
|---|---|
| **Creation** — vitals, position, archetype | The class pick is the central decision |

### Phase 1 — Skeleton — **IN-PROGRESS**

| # | Item | Deliverable | Needs | Status |
|---|---|---|---|---|
| 1.3 | `correction-by-append` | Superseding-event model | 1.2 | NOT STARTED |

#### Harness — Phase 1

| # | Item | Deliverable | Needs | Blocks | Status |
|---|---|---|---|---|---|
| H2 | `domain-engineer` | Write-capable subagent | 1.2 | 1.4 | NOT STARTED |

### Phase 3 — Season — **NOT STARTED**

| # | Item | Deliverable | Needs | Status |
|---|---|---|---|---|
| 3.1 | `badge-system` | Unlock thresholds | 2.8 | NOT STARTED |
"""


def _fake_entry(entry_id: str, moment: str) -> str:
    return f"""### {entry_id} — A fabricated question

- **Bears on:** {moment}
- **Parked:** 2026-08-21
- **Assumed:** none — not hit yet
- **Source:** `nowhere.md`
- **Status:** open
"""


def _fake_queue(moments: list[str]) -> str:
    entries = "\n".join(
        _fake_entry(f"E-{index + 1:03d}", moment) for index, moment in enumerate(moments)
    )
    return f"# Escalations\n\n## Open\n\n{entries}\n## Resolved\n\n*None yet.*\n"


# ─── The guard, proven both ways against tmp_path ─────────────────────────────


def test_an_unknown_moment_is_reported(tmp_path: Path) -> None:
    queue = tmp_path / "ESCALATIONS.md"
    roadmap = tmp_path / "ROADMAP.md"
    queue.write_text(_fake_queue(["9.9"]), encoding="utf-8")
    roadmap.write_text(FAKE_ROADMAP, encoding="utf-8")

    violations = unknown_moments(
        queue.read_text(encoding="utf-8"), roadmap.read_text(encoding="utf-8")
    )

    assert violations == [("E-001", "9.9")]


def test_every_flavour_of_real_moment_is_accepted(tmp_path: Path) -> None:
    queue = tmp_path / "ESCALATIONS.md"
    roadmap = tmp_path / "ROADMAP.md"
    queue.write_text(_fake_queue(["1.3", "H2", "Phase 3", "post-v1"]), encoding="utf-8")
    roadmap.write_text(FAKE_ROADMAP, encoding="utf-8")

    violations = unknown_moments(
        queue.read_text(encoding="utf-8"), roadmap.read_text(encoding="utf-8")
    )

    assert violations == []


def test_a_malformed_heading_is_reported_not_silently_skipped(tmp_path: Path) -> None:
    """The hole this guard was built to close, kept red by a regression test.

    `### E-9999 - Intruder` misses the pinned format twice — four digits, and a
    hyphen where the format pins an em dash. Before the fix it was *invisible*:
    the entry count stayed at eight, so nothing could notice it.
    """
    queue = tmp_path / "ESCALATIONS.md"
    queue.write_text(
        _fake_queue(["1.3"]).replace(
            "## Resolved",
            "### E-9999 - Intruder\n\n- **Bears on:** 9.9\n- **Status:** bogus\n\n## Resolved",
        ),
        encoding="utf-8",
    )

    assert malformed_headings(queue.read_text(encoding="utf-8")) == ["### E-9999 - Intruder"]


def test_a_well_formed_queue_reports_no_malformed_headings(tmp_path: Path) -> None:
    queue = tmp_path / "ESCALATIONS.md"
    queue.write_text(_fake_queue(["1.3", "H2"]), encoding="utf-8")

    assert malformed_headings(queue.read_text(encoding="utf-8")) == []


def test_a_malformed_heading_cannot_overwrite_the_previous_entry(tmp_path: Path) -> None:
    """The second half of the same defect, and the dangerous half.

    A malformed heading's field bullets used to bleed into the preceding entry,
    silently replacing its `Source:` and `Assumed:` — provenance, in a file that
    is world-readable and permanent. Worse, the guards that *did* fire then
    named the innocent entry: `unknown_moments` reported the intruder's `9.9`
    against the real entry above it.
    """
    queue = tmp_path / "ESCALATIONS.md"
    roadmap = tmp_path / "ROADMAP.md"
    queue.write_text(
        _fake_queue(["1.3"]).replace(
            "## Resolved",
            "### E-9999 - Intruder\n\n- **Bears on:** 9.9\n"
            "- **Assumed:** INTRUDER\n- **Source:** `INTRUDER.md`\n- **Status:** bogus\n\n"
            "## Resolved",
        ),
        encoding="utf-8",
    )
    roadmap.write_text(FAKE_ROADMAP, encoding="utf-8")

    body = queue.read_text(encoding="utf-8")
    survivor = parse_entries(FENCED_BLOCK.sub("", body))[-1]

    assert survivor.id == "E-001"
    assert survivor.fields["Source"] == "`nowhere.md`", "The intruder overwrote a real Source:."
    assert survivor.fields["Assumed"] == "none — not hit yet"
    assert survivor.fields["Status"] == "open"
    assert survivor.fields["Bears on"] == "1.3"
    assert unknown_moments(body, roadmap.read_text(encoding="utf-8")) == [], (
        "A real entry was blamed for a malformed neighbour's moment."
    )


def test_the_failure_message_names_the_entry_the_moment_and_the_rule() -> None:
    message = violation_message([("E-042", "9.9")])

    assert "ESCALATIONS.md" in message
    assert "E-042" in message
    assert "9.9" in message
    assert MOMENT_RULE in message


# ─── The parser against the real ROADMAP ──────────────────────────────────────


def test_known_moments_parses_the_real_roadmap() -> None:
    moments = known_moments(ROADMAP.read_text(encoding="utf-8"))

    assert moments, "No moments parsed from ROADMAP.md — the table format drifted."
    for known_good in ("0.1", "1.3", "H2", "4.6", "Phase 1", "Phase 3", "post-v1"):
        assert known_good in moments, f"ROADMAP.md defines {known_good} but the parser missed it."
    # Deliberately a floor, not an exact count: an exact set fires in unrelated
    # PRs every time a row is added (finding F-28).
    assert len(moments) >= 30


def test_the_non_item_tables_contribute_no_ids() -> None:
    """The negative half, and the one that goes vacuous if an anchor drifts.

    Each slice is asserted non-empty *before* it is asserted id-free — the
    anchors carry em dashes, and a silent miss would turn `_item_ids("") == set()`
    into a test that proves nothing (finding [4]).
    """
    body = ROADMAP.read_text(encoding="utf-8")

    for anchor in (
        "### In scope — the engine",
        "### In scope — the application",
        "### Out of scope",
        "## Open questions, by the phase that answers them",
    ):
        slice_ = section_body(body, anchor)

        assert slice_.strip(), f"Heading anchor {anchor!r} matched nothing in ROADMAP.md."
        assert table_rows(slice_), f"Section {anchor!r} has no table rows — the anchor drifted."
        assert _item_ids(slice_) == set(), (
            f"Section {anchor!r} contributed item ids. Its rows lead with bold text, "
            "not ids, so the leading cell must be matched against a pattern rather "
            "than tested for emptiness."
        )


# ─── The real assertions ──────────────────────────────────────────────────────


def test_the_entry_regex_matched_something() -> None:
    """Anti-vacuity. Without this, a format drift makes every check below pass."""
    entries = parse_entries(FENCED_BLOCK.sub("", QUEUE.read_text(encoding="utf-8")))

    assert entries, (
        "No entries parsed — the entry format drifted from the regex. Every "
        "per-entry assertion in this module silently passes over an empty list, "
        "so this is the guard on the guard."
    )
    assert len(entries) >= 9, f"Expected the nine seed entries or more, parsed {len(entries)}."


def test_every_source_citation_resolves_to_a_file_that_exists() -> None:
    """The queue mechanizes `Bears on:` — this does the same for its provenance.

    Shipping a feature whose thesis is "an unchecked pointer rots invisibly"
    with its own provenance field unchecked is the gap this closes. Three seeds
    cite line ranges in `ROADMAP.md`, a hand-edited file this very change
    rewrote, so the citations being correct today is not evidence they stay so.
    """
    unresolved = unresolved_sources(QUEUE.read_text(encoding="utf-8"))

    assert not unresolved, (
        f"Entry Source: citation(s) whose path does not exist: {unresolved}. "
        "`Source:` records where a decision surfaced; a citation pointing at a "
        "file that is gone strands the next reader with no way to recover it."
    )


def test_the_real_queue_has_no_malformed_entry_headings() -> None:
    """The count floor above cannot see this: a malformed heading does not shrink
    the count, it fails to grow it. This is the assertion that actually notices."""
    malformed = malformed_headings(FENCED_BLOCK.sub("", QUEUE.read_text(encoding="utf-8")))

    assert not malformed, (
        "Heading(s) in ESCALATIONS.md's entry sections that are not valid entries: "
        f"{malformed}. The pinned format is `### E-NNN — <title>` with an em dash. "
        "A heading that misses it is skipped by the parser, so every other guard "
        "in this module passes over it without looking."
    )


def test_every_entry_names_a_real_roadmap_moment() -> None:
    violations = unknown_moments(
        QUEUE.read_text(encoding="utf-8"), ROADMAP.read_text(encoding="utf-8")
    )

    assert not violations, violation_message(violations)


def test_every_entry_carries_every_required_field_and_a_unique_id() -> None:
    entries = parse_entries(FENCED_BLOCK.sub("", QUEUE.read_text(encoding="utf-8")))

    incomplete = {
        entry.id: [name for name in REQUIRED_FIELDS if name not in entry.fields]
        for entry in entries
        if any(name not in entry.fields for name in REQUIRED_FIELDS)
    }
    assert not incomplete, f"Entries missing required field(s): {incomplete}"

    ids = [entry.id for entry in entries]
    duplicates = sorted({entry_id for entry_id in ids if ids.count(entry_id) > 1})
    assert not duplicates, (
        f"Duplicate entry id(s): {duplicates}. Ids are assigned by hand and "
        "sequential numbering merges into collisions across branches."
    )

    # Presence is not enough: the scope calls `Assumed:` the load-bearing field,
    # and `- **Assumed:**` with nothing after it is present and useless.
    blank = {
        entry.id: [name for name in REQUIRED_FIELDS if not entry.fields.get(name, "").strip()]
        for entry in entries
        if any(not entry.fields.get(name, "").strip() for name in REQUIRED_FIELDS)
    }
    assert not blank, f"Entries with a required field left empty: {blank}"


def test_every_status_comes_from_the_closed_vocabulary() -> None:
    entries = parse_entries(FENCED_BLOCK.sub("", QUEUE.read_text(encoding="utf-8")))

    # `.get` on BOTH sides. Guarding with `.get` and reading with `[...]` means
    # an entry missing the field satisfies the condition and then raises
    # KeyError instead of printing this module's own diagnostic.
    wrong = {
        entry.id: entry.fields.get("Status", "<missing>")
        for entry in entries
        if entry.fields.get("Status") not in STATUS_VALUES
    }
    assert not wrong, f"Status values outside {sorted(STATUS_VALUES)}: {wrong}"


def test_each_entry_sits_in_the_section_its_status_claims() -> None:
    """State is stored once (finding F-08).

    `Status:` is the single source of truth; the section is a rendering of it.
    The same invariant `test_index_stage_cells_match_their_artifact_status_headers`
    already enforces between the Index and the artifact headers.
    """
    entries = parse_entries(FENCED_BLOCK.sub("", QUEUE.read_text(encoding="utf-8")))

    disagreements = {
        entry.id: (entry.fields.get("Status"), entry.section)
        for entry in entries
        if entry.fields.get("Status", "").capitalize() != entry.section
    }
    assert not disagreements, (
        "Entries whose Status disagrees with the section they sit in "
        f"(status, section): {disagreements}. An `open` entry belongs under "
        "`## Open` and a `resolved` one under `## Resolved`."
    )


def test_the_worked_example_parses_exactly_like_a_real_entry() -> None:
    """Goal 1 is mechanical or it is a wish (finding F-01).

    "The third move exists" reduces to: a worker copies the template and cannot
    thereby produce a malformed entry. That is only true if the template is held
    to the same guards, so it is parsed here rather than trusted.
    """
    body = QUEUE.read_text(encoding="utf-8")

    blocks = [
        block.group(0) for block in FENCED_BLOCK.finditer(body) if ENTRY.search(block.group(0))
    ]
    assert len(blocks) == 1, f"Expected exactly one fenced worked example, found {len(blocks)}."

    example = parse_entries(blocks[0])
    assert len(example) == 1, "The worked example did not parse as exactly one entry."

    entry = example[0]
    missing = [name for name in REQUIRED_FIELDS if name not in entry.fields]
    assert not missing, f"The worked example is missing required field(s): {missing}"
    assert entry.fields["Status"] in STATUS_VALUES
    assert entry.fields["Bears on"].lower() in {
        moment.lower() for moment in known_moments(ROADMAP.read_text(encoding="utf-8"))
    }, "The worked example names a moment ROADMAP.md does not define — copying it would fail."


def test_the_queue_draws_its_boundary_against_the_five_other_registers() -> None:
    """Asserted against the register-map *table rows*, not the file (finding [3]).

    Two vacuity traps live here. `"DESIGN.md"` is a substring of
    `"GAME_DESIGN.md"`, so it passes on the wrong row; and `"Escalation"` appears
    in the queue's own prose, so it passes without a register map existing at
    all. The anchors below are the distinctive ones.
    """
    body = QUEUE.read_text(encoding="utf-8")
    rows = table_rows(section_body(body, "## The register map"))

    assert rows, "The queue has no register-map table — the boundary is the load-bearing part."

    for anchor in ("GAME_DESIGN.md", "§2", "§4", "Stage plan", "diagnose-bug"):
        assert any(anchor in row for row in rows), (
            f"No register-map row names {anchor!r}. The queue is the sixth place a "
            "question can be parked here; the map is what keeps it from becoming a "
            "duplicate of the other five."
        )

    offenders = [
        entry.id for entry in parse_entries(FENCED_BLOCK.sub("", body)) if "[OPEN-" in entry.title
    ]
    assert not offenders, (
        f"Entry title(s) carrying an [OPEN-N] id: {offenders}. GAME_DESIGN.md §8 "
        "owns that series; this file cross-references it and never absorbs it."
    )


def test_all_nine_seeds_survived_the_migration() -> None:
    body = QUEUE.read_text(encoding="utf-8")

    for seed in (
        "serviceability gate",  # E-001, from ROADMAP.md's parked paragraph
        "design/UX specialist",  # E-002, same
        "stage dispatch be autonomous",  # E-003, same
        "OpenAPI snapshot test",  # E-004, stranded in _done/1.1-app-shell
        "generated from OpenAPI",  # E-005, same
        "blanket `build/`",  # E-006, same
        "tenth open question",  # E-007, the measured orphan
        "superseding correction event",  # E-008, the real question at moment 1.3
        "pin the ruleset version live",  # E-009, the ADR 0003/0004 tension at 1.3
    ):
        assert seed in body, f"Seed entry missing from the queue: {seed!r}"


def test_the_roadmap_no_longer_carries_the_migrated_hypotheses() -> None:
    """What stops the migration leaving two sources of truth.

    The paragraph's substantive observation — that "serviceable" is a v1
    constraint in both directions and is nowhere defined or tested — is
    deliberately *kept*; only the enumeration moves.
    """
    body = ROADMAP.read_text(encoding="utf-8")

    for migrated in ("serviceability gate", "design/UX", "autonomous stage dispatcher"):
        assert migrated not in body, (
            f"ROADMAP.md still enumerates {migrated!r}. It now lives in ESCALATIONS.md, "
            "and two sources of truth is the failure the migration exists to end."
        )

    assert "ESCALATIONS.md" in body, "ROADMAP.md must point at the queue it no longer duplicates."
    assert "serviceable" in body, (
        "The paragraph's substantive observation was dropped rather than reduced "
        "to a pointer — 'serviceable' is a v1 constraint in both directions and is "
        "nowhere defined or tested."
    )


# ─── The read seams ───────────────────────────────────────────────────────────
#
# These live in this module rather than in three others (decision G6): one place
# a cold agent reads to see everything holding the queue up.
#
# Asserted on the bare filename (decision G7) — it appears in none of the three
# skill files today, so it is a clean anchor that survives rewording. Stated
# weakness: it also passes if the filename survives in a sentence that no longer
# instructs anyone. The seam is a read rather than a gate, so a substring is
# proportionate; a stricter assertion would pin prose nobody should hesitate to
# edit.


def _skill(name: str) -> str:
    return (REPO_ROOT / ".claude" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def test_intake_reads_the_queue_when_grounding_an_item() -> None:
    """Decision 1 — the minimum antidote to the inertness risk.

    A queue nothing reads is the `ops/branch-protection.json` failure: correct,
    tracked, and inert until someone remembers it. Intake is where the drain
    fires, because it is what runs at an item boundary.
    """
    assert "ESCALATIONS.md" in _skill("make-feature-request"), (
        "/make-feature-request Step 2 no longer reads the queue. Without it the "
        "queue is written and never read, which all three scopers independently "
        "named as the feature-killing risk."
    )


def test_commit_surfaces_open_entries_before_closing_a_row() -> None:
    """Decision 5 — the drain hole (finding F-32).

    An entry naming 1.3 goes permanently invisible the moment 1.3 flips to DONE,
    because intake never asks about a closed item again. `/commit` Step 4 is the
    one thing running at exactly that moment.
    """
    assert "ESCALATIONS.md" in _skill("commit"), (
        "/commit Step 4 no longer checks the queue when flipping a row to DONE. "
        "That is the drain hole: entries against a closed item stop being findable."
    )


def test_diagnose_bug_has_somewhere_to_hand_a_murky_cause() -> None:
    """Decision 3 — a pointer, not a second evidence trail.

    The RCA keeps its Escalation section; the queue only records that the bug is
    waiting, and against which moment. The non-blocking property is preserved
    exactly — the bug still waits.
    """
    assert "ESCALATIONS.md" in _skill("diagnose-bug"), (
        "/diagnose-bug's Escalation hand-off has no destination again — a murky "
        "cause goes back to being recorded nowhere that anything reopens."
    )
