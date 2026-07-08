"""会话状态管理，隔离 Streamlit 的 session_state 细节。"""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

_STARTED = "sa_started"
_FOUND = "sa_found_evidence"
_INTERROGATED = "sa_interrogated"
_ATTEMPTS = "sa_attempts"
_SOLVED = "sa_solved"


@dataclass(slots=True)
class GameState:
    """一局游戏的可变状态封装。"""

    started: bool
    solved: bool
    attempts: int

    @classmethod
    def load(cls) -> GameState:
        st.session_state.setdefault(_STARTED, False)
        st.session_state.setdefault(_FOUND, set())
        st.session_state.setdefault(_INTERROGATED, set())
        st.session_state.setdefault(_ATTEMPTS, 0)
        st.session_state.setdefault(_SOLVED, False)
        return cls(
            started=st.session_state[_STARTED],
            solved=st.session_state[_SOLVED],
            attempts=st.session_state[_ATTEMPTS],
        )

    def start(self) -> None:
        st.session_state[_STARTED] = True

    def find_evidence(self, evidence_id: str) -> None:
        st.session_state[_FOUND].add(evidence_id)

    def has_evidence(self, evidence_id: str) -> bool:
        return evidence_id in st.session_state[_FOUND]

    @property
    def found_ids(self) -> set[str]:
        return st.session_state[_FOUND]

    @property
    def found_count(self) -> int:
        return len(st.session_state[_FOUND])

    def interrogate(self, key: str) -> None:
        st.session_state[_INTERROGATED].add(key)

    def has_interrogated(self, key: str) -> bool:
        return key in st.session_state[_INTERROGATED]

    @property
    def interrogated_count(self) -> int:
        return len(st.session_state[_INTERROGATED])

    def record_attempt(self) -> int:
        st.session_state[_ATTEMPTS] += 1
        return st.session_state[_ATTEMPTS]

    def mark_solved(self) -> None:
        st.session_state[_SOLVED] = True

    def progress(self, total: int) -> float:
        return self.found_count / total if total else 0.0

    @staticmethod
    def reset() -> None:
        for key in (_STARTED, _FOUND, _INTERROGATED, _ATTEMPTS, _SOLVED):
            st.session_state.pop(key, None)
