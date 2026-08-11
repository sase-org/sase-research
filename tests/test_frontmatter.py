"""Parse a representative research document's Markdown frontmatter into the
research ref provider's declared typed property fields.
"""

from __future__ import annotations

from datetime import datetime

from sase.xprompt.loader_parsing import parse_yaml_front_matter

from sase_research.provider import RESEARCH_REF_PROVIDER_SPEC

_SAMPLE_DOCUMENT = """\
---
create_time: 2026-08-11 16:29:34
updated_time: 2026-08-11 18:02:11
status: final
tags:
  - artifact-refs
  - plugins
---

# Widgets research

Body content.
"""


def test_declared_properties_match_provider_spec() -> None:
    properties = RESEARCH_REF_PROVIDER_SPEC["ref"]["properties"]
    assert set(properties) == {"create_time", "updated_time", "status", "tags"}
    assert properties["create_time"]["type"] == "datetime"
    assert properties["updated_time"]["type"] == "datetime"
    assert properties["status"]["type"] == "string"
    assert properties["tags"]["type"] == "string_list"
    assert all(prop["source"] == "markdown_frontmatter" for prop in properties.values())


def test_sample_frontmatter_parses_into_declared_types() -> None:
    front_matter, body = parse_yaml_front_matter(_SAMPLE_DOCUMENT)

    assert front_matter is not None
    assert isinstance(front_matter["create_time"], datetime)
    assert isinstance(front_matter["updated_time"], datetime)
    assert isinstance(front_matter["status"], str)
    assert isinstance(front_matter["tags"], list)
    assert all(isinstance(tag, str) for tag in front_matter["tags"])
    assert "# Widgets research" in body


def test_detail_fields_are_all_declared_properties() -> None:
    ref = RESEARCH_REF_PROVIDER_SPEC["ref"]
    assert set(ref["detail"]["fields"]) <= set(ref["properties"])
