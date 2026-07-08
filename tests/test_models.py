"""模型与案件数据的单元测试。"""

from __future__ import annotations

import pytest

from suspense_app.data import MIDNIGHT_CASE
from suspense_app.models import Case, Suspect


def _suspect(name: str = "甲") -> Suspect:
    return Suspect(name=name, desc="描述", alibi="证词", clue="线索")


def test_case_indexes_suspects_by_name() -> None:
    case = MIDNIGHT_CASE
    for name in case.suspect_names:
        assert case.get(name).name == name


def test_total_suspects_matches_data() -> None:
    assert MIDNIGHT_CASE.total_suspects == len(MIDNIGHT_CASE.suspects)


def test_is_culprit() -> None:
    case = MIDNIGHT_CASE
    assert case.is_culprit(case.culprit_name) is True
    assert case.is_culprit("不存在的人") is False
    assert case.is_culprit(None) is False


def test_culprit_must_be_a_suspect() -> None:
    with pytest.raises(ValueError):
        Case(
            title="t",
            subtitle="s",
            location="l",
            intro=("i",),
            suspects=(_suspect("甲"),),
            culprit_name="乙",
            reveal="r",
        )


def test_duplicate_names_rejected() -> None:
    with pytest.raises(ValueError):
        Case(
            title="t",
            subtitle="s",
            location="l",
            intro=("i",),
            suspects=(_suspect("甲"), _suspect("甲")),
            culprit_name="甲",
            reveal="r",
        )


def test_empty_suspects_rejected() -> None:
    with pytest.raises(ValueError):
        Case(
            title="t",
            subtitle="s",
            location="l",
            intro=("i",),
            suspects=(),
            culprit_name="甲",
            reveal="r",
        )


def test_suspect_is_immutable() -> None:
    suspect = _suspect()
    with pytest.raises((AttributeError, TypeError)):
        suspect.name = "改名"  # type: ignore[misc]
