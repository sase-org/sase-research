"""Load all packaged xprompts through sase's public plugin loader and prove
the swarm's segment count and wait/fork dependency graph survive packaging.
"""

from __future__ import annotations

from sase.agent.multi_prompt import split_segments_protecting_fences
from sase.xprompt.loader_sources import load_xprompts_from_plugins


def _research_xprompts() -> dict:
    xprompts = load_xprompts_from_plugins()
    return {name: xp for name, xp in xprompts.items() if name.startswith("research")}


def test_all_five_research_xprompts_load() -> None:
    assert set(_research_xprompts()) == {
        "research",
        "research/image",
        "research/more",
        "research/prompt",
        "research_swarm",
    }


def test_research_prompt_declares_typed_input() -> None:
    xp = _research_xprompts()["research/prompt"]
    assert [(arg.name, arg.type.value) for arg in xp.inputs] == [("prompt", "text")]


def test_research_swarm_declares_typed_input() -> None:
    xp = _research_xprompts()["research_swarm"]
    assert [(arg.name, arg.type.value) for arg in xp.inputs] == [("prompt", "text")]


def test_research_swarm_has_four_top_level_segments() -> None:
    xp = _research_xprompts()["research_swarm"]
    segments = split_segments_protecting_fences(xp.content)
    assert len(segments) == 4


def test_research_swarm_dependency_graph_preserved() -> None:
    xp = _research_xprompts()["research_swarm"]
    cdx, cld, final, image = split_segments_protecting_fences(xp.content)

    assert "%clan(research.{@1}" in cdx
    assert "%id:research.{@1}.cdx" in cdx

    assert "%id(cld, clan=research.{@1})" in cld

    assert "%id(final, clan=research.{@1})" in final
    assert "%wait:research.{@1}.cdx" in final
    assert "%wait:research.{@1}.cld" in final

    assert "%id(image, clan=research.{@1})" in image
    assert "%wait:research.{@1}.final" in image
    assert "#fork:research.{@1}.final" in image
    assert "#research/image" in image
