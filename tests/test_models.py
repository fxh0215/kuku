"""模型与案件数据的单元测试。"""

from __future__ import annotations

import pytest

from suspense_app.data import MIDNIGHT_CASE
from suspense_app.models import Case, Evidence, Interrogation, Scene, Suspect


def _suspect(sid: str = "s1", name: str = "甲") -> Suspect:
    return Suspect(
        id=sid,
        name=name,
        desc="描述",
        alibi="证词",
        clue="线索",
        questions=(Interrogation(question="问？", answer="答。"),),
    )


def _scene() -> Scene:
    return Scene(
        id="sc1",
        name="房间",
        intro="简介",
        evidence=(Evidence(id="e1", name="证物", detail="细节"),),
    )


def _make_case(**overrides: object) -> Case:
    base: dict[str, object] = {
        "title": "t",
        "subtitle": "s",
        "location": "l",
        "intro": ("i",),
        "scenes": (_scene(),),
        "suspects": (_suspect(),),
        "weapons": ("刀",),
        "motives": ("钱",),
        "culprit_name": "甲",
        "weapon": "刀",
        "motive": "钱",
        "reveal": "r",
    }
    base.update(overrides)
    return Case(**base)  # type: ignore[arg-type]


def test_case_indexes_suspects_by_name() -> None:
    for name in MIDNIGHT_CASE.suspect_names:
        assert MIDNIGHT_CASE.get(name).name == name


def test_totals_match_data() -> None:
    assert MIDNIGHT_CASE.total_suspects == len(MIDNIGHT_CASE.suspects)
    expected_evi = sum(len(s.evidence) for s in MIDNIGHT_CASE.scenes)
    assert MIDNIGHT_CASE.total_evidence == expected_evi


def test_is_culprit() -> None:
    case = MIDNIGHT_CASE
    assert case.is_culprit(case.culprit_name) is True
    assert case.is_culprit("不存在的人") is False
    assert case.is_culprit(None) is False


def test_check_solution_all_correct() -> None:
    case = MIDNIGHT_CASE
    result = case.check_solution(case.culprit_name, case.weapon, case.motive)
    assert result == {"culprit": True, "weapon": True, "motive": True}


def test_check_solution_partial() -> None:
    case = MIDNIGHT_CASE
    wrong_weapon = next(w for w in case.weapons if w != case.weapon)
    result = case.check_solution(case.culprit_name, wrong_weapon, case.motive)
    assert result == {"culprit": True, "weapon": False, "motive": True}


def test_evidence_ids_unique_in_case() -> None:
    ids = [e.id for sc in MIDNIGHT_CASE.scenes for e in sc.evidence]
    assert len(ids) == len(set(ids))


def test_culprit_must_be_a_suspect() -> None:
    with pytest.raises(ValueError):
        _make_case(culprit_name="乙")


def test_weapon_must_be_candidate() -> None:
    with pytest.raises(ValueError):
        _make_case(weapon="不存在")


def test_motive_must_be_candidate() -> None:
    with pytest.raises(ValueError):
        _make_case(motive="不存在")


def test_duplicate_names_rejected() -> None:
    with pytest.raises(ValueError):
        _make_case(suspects=(_suspect("a", "甲"), _suspect("b", "甲")))


def test_empty_suspects_rejected() -> None:
    with pytest.raises(ValueError):
        _make_case(suspects=())


def test_suspect_is_immutable() -> None:
    suspect = _suspect()
    with pytest.raises((AttributeError, TypeError)):
        suspect.name = "改名"  # type: ignore[misc]
