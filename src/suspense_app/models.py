"""领域模型：案件、场景、证物、嫌疑人与审讯。"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Evidence:
    """一件可在场景中搜出的证物。"""

    id: str
    name: str
    detail: str
    icon: str = "🔎"


@dataclass(frozen=True, slots=True)
class Scene:
    """一处可供勘察的案发场景，内含若干证物。"""

    id: str
    name: str
    intro: str
    evidence: tuple[Evidence, ...]
    icon: str = "📍"


@dataclass(frozen=True, slots=True)
class Interrogation:
    """针对嫌疑人的一个可选审讯问题及其回答。"""

    question: str
    answer: str


@dataclass(frozen=True, slots=True)
class Suspect:
    """一名嫌疑人及其证词、破绽与可审讯的问题。"""

    id: str
    name: str
    desc: str
    alibi: str
    clue: str
    questions: tuple[Interrogation, ...] = ()


@dataclass(frozen=True, slots=True)
class Case:
    """一桩案件：多场景搜证、嫌疑人审讯，并以三要素定案。"""

    title: str
    subtitle: str
    location: str
    intro: tuple[str, ...]
    scenes: tuple[Scene, ...]
    suspects: tuple[Suspect, ...]
    weapons: tuple[str, ...]
    motives: tuple[str, ...]
    culprit_name: str
    weapon: str
    motive: str
    reveal: str
    max_accusations: int = 3

    suspect_index: dict[str, Suspect] = field(init=False, repr=False)
    evidence_index: dict[str, Evidence] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "suspect_index", {s.name: s for s in self.suspects})
        evi = {e.id: e for scene in self.scenes for e in scene.evidence}
        object.__setattr__(self, "evidence_index", evi)
        self._validate()

    def _validate(self) -> None:
        if not self.suspects:
            raise ValueError("案件至少需要一名嫌疑人。")
        if len(self.suspect_index) != len(self.suspects):
            raise ValueError("嫌疑人姓名必须唯一。")
        if self.culprit_name not in self.suspect_index:
            raise ValueError(f"真凶 {self.culprit_name!r} 不在嫌疑人名单中。")
        if self.weapon not in self.weapons:
            raise ValueError(f"凶器 {self.weapon!r} 不在候选列表中。")
        if self.motive not in self.motives:
            raise ValueError(f"动机 {self.motive!r} 不在候选列表中。")
        if self.max_accusations < 1:
            raise ValueError("指认次数至少为 1。")

    @property
    def suspect_names(self) -> list[str]:
        return [s.name for s in self.suspects]

    @property
    def total_suspects(self) -> int:
        return len(self.suspects)

    @property
    def total_evidence(self) -> int:
        return len(self.evidence_index)

    def get(self, name: str) -> Suspect:
        return self.suspect_index[name]

    def is_culprit(self, name: str | None) -> bool:
        return name == self.culprit_name

    def check_solution(
        self, name: str | None, weapon: str | None, motive: str | None
    ) -> dict[str, bool]:
        """校验三要素，返回每一项是否正确。"""
        return {
            "culprit": name == self.culprit_name,
            "weapon": weapon == self.weapon,
            "motive": motive == self.motive,
        }
