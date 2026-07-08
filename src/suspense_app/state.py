"""会话状态管理，隔离 Streamlit 的 session_state 细节。"""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

_STARTED = "sa_started"
_EXAMINED = "sa_examined"
_SOLVED = "sa_solved"
_ACCUSED = "sa_accused"


@dataclass(slots=True)
class GameState:
    """一局游戏的可变状态封装。"""

    started: bool
    examined: set[str]
    solved: bool
    accused: str | None

    @classmethod
    def load(cls) -> GameState:
        st.session_state.setdefault(_STARTED, False)
        st.session_state.setdefault(_EXAMINED, set())
        st.session_state.setdefault(_SOLVED, False)
        st.session_state.setdefault(_ACCUSED, None)
        return cls(
            started=st.session_state[_STARTED],
            examined=st.session_state[_EXAMINED],
            solved=st.session_state[_SOLVED],
            accused=st.session_state[_ACCUSED],
        )

    def start(self) -> None:
        st.session_state[_STARTED] = True

    def examine(self, name: str) -> None:
        st.session_state[_EXAMINED].add(name)

    def has_examined(self, name: str) -> bool:
        return name in st.session_state[_EXAMINED]

    def mark_solved(self, accused: str) -> None:
        st.session_state[_SOLVED] = True
        st.session_state[_ACCUSED] = accused

    @property
    def examined_count(self) -> int:
        return len(st.session_state[_EXAMINED])

    def progress(self, total: int) -> float:
        return self.examined_count / total if total else 0.0

    @staticmethod
    def reset() -> None:
        for key in (_STARTED, _EXAMINED, _SOLVED, _ACCUSED):
            st.session_state.pop(key, None)
