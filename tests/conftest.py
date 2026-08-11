"""Shared fixtures for sase-research contract tests."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
import importlib.metadata

import pytest

# Importing sase.config before sase.artifact_providers avoids a circular
# import when artifact_providers is the first sase submodule touched by a
# fresh interpreter (sase.config.file_hooks imports sase.artifact_providers
# .registry, which is still initializing on that path).
import sase.config  # noqa: F401
import sase.config.file_hooks as file_hooks_config
from sase.artifact_providers import reset_artifact_provider_registry_cache


@pytest.fixture(autouse=True)
def _reset_registry_cache() -> Iterator[None]:
    reset_artifact_provider_registry_cache()
    file_hooks_config._file_hooks_cache_token = None
    file_hooks_config._file_hooks_cache_value = None
    yield
    reset_artifact_provider_registry_cache()
    file_hooks_config._file_hooks_cache_token = None
    file_hooks_config._file_hooks_cache_value = None


@dataclass
class FakeDist:
    """A minimal stand-in for ``importlib.metadata.Distribution``."""

    name: str = "sase-research"
    version: str = "0.1.0"

    @property
    def metadata(self) -> dict[str, str]:
        return {"Name": self.name, "Version": self.version}


@dataclass
class FakeEntryPoint:
    """A minimal stand-in for ``importlib.metadata.EntryPoint``."""

    name: str
    group: str
    plugin: object
    dist: FakeDist = field(default_factory=FakeDist)
    value: str = "tests:Plugin"

    def load(self) -> object:
        if isinstance(self.plugin, BaseException):
            raise self.plugin
        return self.plugin


def real_and_fake_entry_points(
    *extra: FakeEntryPoint,
) -> object:
    """Build an ``entry_points_fn`` that layers *extra* fakes on real discovery.

    ``assemble_artifact_provider_registry(entry_points_fn=...)`` is the
    documented seam for injecting synthetic plugins without touching the real
    environment (mirrors sase's own registry test helpers).
    """

    def _entry_points_fn(*, group: str) -> tuple[object, ...]:
        real = tuple(importlib.metadata.entry_points(group=group))
        fake = tuple(ep for ep in extra if ep.group == group)
        return real + fake

    return _entry_points_fn
