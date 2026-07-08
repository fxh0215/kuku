"""应用组装：串联主题、状态与各界面区块。"""

from __future__ import annotations

import streamlit as st

from suspense_app import components
from suspense_app.data import MIDNIGHT_CASE
from suspense_app.models import Case
from suspense_app.state import GameState


def configure_page(case: Case) -> None:
    st.set_page_config(
        page_title=case.title.replace(" ", ""),
        page_icon="🕯️",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def run(case: Case = MIDNIGHT_CASE) -> None:
    """应用主流程。"""
    configure_page(case)
    components.inject_theme()

    state = GameState.load()

    components.render_header(case)
    components.render_sidebar(case, state)

    if not state.started:
        components.render_intro(case, state)
        return

    tab_search, tab_ask, tab_notes, tab_verdict = st.tabs(
        ["🔦 现场搜证", "🗣️ 审讯", "📓 侦探笔记", "⚖️ 定案"]
    )
    with tab_search:
        components.render_investigation(case, state)
    with tab_ask:
        components.render_interrogation(case, state)
    with tab_notes:
        components.render_notebook(case, state)
    with tab_verdict:
        components.render_verdict(case, state)
