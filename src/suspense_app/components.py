"""界面组件：将悬疑风格的 UI 拆分为可复用的渲染函数。"""

from __future__ import annotations

import time
from datetime import datetime

import streamlit as st

from suspense_app.models import Case, Suspect
from suspense_app.state import GameState
from suspense_app.styles import CSS

_TYPE_DELAY = 0.028


def inject_theme() -> None:
    """注入全局悬疑主题样式。"""
    st.markdown(CSS, unsafe_allow_html=True)


def render_header(case: Case) -> None:
    """渲染闪烁标题与副标题。"""
    st.markdown(f"<div class='title-flicker'>{case.title}</div>", unsafe_allow_html=True)
    st.markdown(f"<p class='whisper'>{case.subtitle}</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)


def render_sidebar(case: Case, state: GameState) -> None:
    """渲染侧边栏案件档案与调查进度。"""
    with st.sidebar:
        st.markdown("### 🕯️ 案件档案")
        st.markdown(f"**卷宗时间**：{datetime.now():%Y-%m-%d %H:%M}")
        st.markdown(f"**案发地点**：{case.location}")

        examined = state.examined_count
        total = case.total_suspects
        if state.solved:
            status = "<span class='blood'>✦ 真相已揭晓</span>"
        elif examined >= total:
            status = "<span class='blood'>● 待你指认</span>"
        else:
            status = "<span class='blood'>● 调查进行中</span>"
        st.markdown(f"**案件状态**：{status}", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**线索收集进度**")
        st.progress(state.progress(total))
        st.caption(f"已审视 {examined} / {total} 名嫌疑人")

        st.markdown("---")
        if st.button("🔄 重新展开卷宗", use_container_width=True):
            GameState.reset()
            st.rerun()
        st.caption("烛火摇曳，真相仍在暗处等待。")


def render_intro(case: Case, state: GameState) -> None:
    """渲染序章与开始按钮。"""
    st.markdown("### 序 章")
    for line in case.intro:
        st.markdown(f"<div class='clue-card'>{line}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("🚪 推开那扇门，开始调查", use_container_width=True):
            state.start()
            st.rerun()


def _typewriter(text: str, placeholder: st.delta_generator.DeltaGenerator) -> None:
    shown = ""
    for ch in text:
        shown += ch
        placeholder.markdown(f"<div class='clue-card'>🔦 {shown}▌</div>", unsafe_allow_html=True)
        time.sleep(_TYPE_DELAY)
    placeholder.markdown(f"<div class='clue-card'>🔦 {shown}</div>", unsafe_allow_html=True)


def _render_suspect_card(suspect: Suspect, state: GameState) -> None:
    examined = state.has_examined(suspect.name)
    badge = "✔ 已勘察" if examined else "○ 未勘察"
    with st.expander(f"👤 {suspect.name}　·　{badge}", expanded=False):
        st.markdown(f"<div class='clue-card'><em>{suspect.desc}</em></div>", unsafe_allow_html=True)
        st.markdown(f"**证词**：{suspect.alibi}")
        clue_slot = st.empty()
        if st.button("🔍 仔细勘察", key=f"btn_{suspect.name}", use_container_width=True):
            newly = not state.has_examined(suspect.name)
            state.examine(suspect.name)
            if newly:
                _typewriter(suspect.clue, clue_slot)
            else:
                clue_slot.markdown(
                    f"<div class='clue-card'>🔦 {suspect.clue}</div>",
                    unsafe_allow_html=True,
                )
        elif examined:
            clue_slot.markdown(
                f"<div class='clue-card'>🔦 {suspect.clue}</div>",
                unsafe_allow_html=True,
            )


def render_suspects(case: Case, state: GameState) -> None:
    """以两列网格渲染全部嫌疑人卡片。"""
    st.markdown("### 🔍 审视嫌疑人")
    st.caption("逐一查看每个人的证词，寻找说谎的破绽。")

    cols = st.columns(2, gap="large")
    for i, suspect in enumerate(case.suspects):
        with cols[i % 2]:
            _render_suspect_card(suspect, state)

    st.markdown("<hr>", unsafe_allow_html=True)


def render_accusation(case: Case, state: GameState) -> None:
    """渲染指认凶手环节与结果反馈。"""
    if state.examined_count < case.total_suspects:
        remaining = case.total_suspects - state.examined_count
        st.info(f"线索尚不充分，还有 {remaining} 名嫌疑人等待勘察。")
        return

    st.markdown("### ⚖️ 指认凶手")
    st.markdown(
        "<p class='whisper'>所有线索已收集完毕。现在，说出那个名字。</p>",
        unsafe_allow_html=True,
    )
    choice = st.radio("你认为凶手是谁？", case.suspect_names, index=None)

    if st.button("🗡️ 揭晓真相", use_container_width=True):
        if case.is_culprit(choice):
            st.balloons()
            st.success(f"**真相大白。** 凶手正是 {case.culprit_name}。")
            st.markdown(
                f"<div class='clue-card'>{case.reveal}</div>",
                unsafe_allow_html=True,
            )
            state.mark_solved(choice)
        else:
            st.error("凶手在你的注视下，露出了一丝冷笑……再想想那些对不上的细节。")
