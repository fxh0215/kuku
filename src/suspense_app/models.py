"""领域模型：案件与嫌疑人。"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Suspect:
    """一名嫌疑人及其证词与线索。"""

    name: str
    desc: str
    alibi: str
    clue: str


@dataclass(frozen=True, slots=True)
class Case:
    """一桩案件：包含序章、嫌疑人名单与真凶。"""

    title: str
    subtitle: str
    location: str
    intro: tuple[str, ...]
    suspects: tuple[Suspect, ...]
    culprit_name: str
    reveal: str
    suspect_index: dict[str, Suspect] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        index = {s.name: s for s in self.suspects}
        object.__setattr__(self, "suspect_index", index)
        self._validate()

    def _validate(self) -> None:
        if not self.suspects:
            raise ValueError("案件至少需要一名嫌疑人。")
        if len(self.suspect_index) != len(self.suspects):
            raise ValueError("嫌疑人姓名必须唯一。")
        if self.culprit_name not in self.suspect_index:
            raise ValueError(f"真凶 {self.culprit_name!r} 不在嫌疑人名单中。")

    @property
    def suspect_names(self) -> list[str]:
        return [s.name for s in self.suspects]

    @property
    def total_suspects(self) -> int:
        return len(self.suspects)

    def get(self, name: str) -> Suspect:
        return self.suspect_index[name]

    def is_culprit(self, name: str | None) -> bool:
        return name == self.culprit_name
