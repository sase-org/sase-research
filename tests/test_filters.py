"""Prove the intentional glob divergence between the ref inventory and the
file-hook filters: the ref provider's inventory keeps `__a`/`__b` swarm
drafts (citing a specific researcher's draft is legitimate), while the
research-highlights file hook excludes them (no Highlights PDF per draft).
"""

from __future__ import annotations

from sase.artifact_ref_operations import filter_artifact_ref_paths

from sase_research_artifacts.provider import (
    RESEARCH_HIGHLIGHTS_HOOK_SPEC,
    RESEARCH_REF_PROVIDER_SPEC,
)

_CANDIDATES = (
    "202608/widgets/widgets.md",
    "202608/widgets/widgets__a.md",
    "202608/widgets/widgets__b.md",
    "202608/widgets/widgets_infographic.md",
    "202608/widgets/widgets.png.md",
    "notes/scratch.md",
)


def test_ref_inventory_globs_keep_swarm_drafts() -> None:
    globs = RESEARCH_REF_PROVIDER_SPEC["ref"]["inventory"]["globs"]

    result = filter_artifact_ref_paths("research", _CANDIDATES, path_globs=globs)

    assert result.allowed == (
        "202608/widgets/widgets.md",
        "202608/widgets/widgets__a.md",
        "202608/widgets/widgets__b.md",
    )
    assert "202608/widgets/widgets_infographic.md" in result.filtered
    assert "202608/widgets/widgets.png.md" in result.filtered
    assert "notes/scratch.md" in result.filtered


def test_file_hook_globs_exclude_swarm_drafts() -> None:
    globs = RESEARCH_HIGHLIGHTS_HOOK_SPEC["file_hook"]["filters"]["path_globs"]

    result = filter_artifact_ref_paths(
        "research-highlights", _CANDIDATES, path_globs=globs
    )

    assert result.allowed == ("202608/widgets/widgets.md",)
    assert "202608/widgets/widgets__a.md" in result.filtered
    assert "202608/widgets/widgets__b.md" in result.filtered
    assert "202608/widgets/widgets_infographic.md" in result.filtered
    assert "202608/widgets/widgets.png.md" in result.filtered
    assert "notes/scratch.md" in result.filtered


def test_file_hook_filters_restrict_to_committed_routes() -> None:
    filters = RESEARCH_HIGHLIGHTS_HOOK_SPEC["file_hook"]["filters"]

    assert filters["producers"] == ["commit", "sdd", "finalizer"]
    assert filters["sidecars"] == ["research"]
    assert filters["ops"] == ["ADD"]
    assert filters["agent_name_globs"] == ["!research.*.cld", "!research.*.cdx"]
