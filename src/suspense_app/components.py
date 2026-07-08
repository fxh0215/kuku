"""界面组件：将悬疑风格的 UI 拆分为可复用的渲染函数。"""

from __future__ import annotations

import time
from datetime import datetime

import streamlit as st

from suspense_app.models import Case, Scene, Suspect
from suspense_app.state import GameState
from suspense_app.styles import CSS

_TYPE_DELAY = 0.02


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

        found = state.found_count
        total = case.total_evidence
        if state.solved:
            status = "<span class='blood'>✦ 真相已揭晓</span>"
        elif found >= total:
            status = "<span class='blood'>● 证据齐备，可以定案</span>"
        else:
            status = "<span class='blood'>● 调查进行中</span>"
        st.markdown(f"**案件状态**：{status}", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**🔎 证物收集**")
        st.progress(state.progress(total))
        st.caption(f"已找到 {found} / {total} 件证物")

        st.markdown("**🗣️ 审讯进度**")
        total_q = sum(len(s.questions) for s in case.suspects)
        st.progress(state.interrogated_count / total_q if total_q else 0.0)
        st.caption(f"已问出 {state.interrogated_count} / {total_q} 条口供")

        remaining = case.max_accusations - state.attempts
        st.markdown(
            f"**🗡️ 定案机会**：<span class='blood'>{remaining}</span> 次", unsafe_allow_html=True
        )

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


def _typewriter(text: str, placeholder: st.delta_generator.DeltaGenerator, prefix: str) -> None:
    shown = ""
    for ch in text:
        shown += ch
        placeholder.markdown(
            f"<div class='clue-card'>{prefix} {shown}▌</div>", unsafe_allow_html=True
        )
        time.sleep(_TYPE_DELAY)
    placeholder.markdown(f"<div class='clue-card'>{prefix} {shown}</div>", unsafe_allow_html=True)


def _render_scene(scene: Scene, state: GameState) -> None:
    found_here = sum(1 for e in scene.evidence if state.has_evidence(e.id))
    header = f"{scene.icon} {scene.name}　·　线索 {found_here}/{len(scene.evidence)}"
    with st.expander(header, expanded=False):
        st.markdown(f"<div class='clue-card'><em>{scene.intro}</em></div>", unsafe_allow_html=True)
        for evi in scene.evidence:
            found = state.has_evidence(evi.id)
            label = f"{evi.icon} {evi.name}" + ("　✔" if found else "")
            slot = st.empty()
            if st.button(label, key=f"evi_{evi.id}", use_container_width=True):
                newly = not found
                state.find_evidence(evi.id)
                if newly:
                    _typewriter(evi.detail, slot, evi.icon)
                else:
                    slot.markdown(
                        f"<div class='clue-card'>{evi.icon} {evi.detail}</div>",
                        unsafe_allow_html=True,
                    )
            elif found:
                slot.markdown(
                    f"<div class='clue-card'>{evi.icon} {evi.detail}</div>",
                    unsafe_allow_html=True,
                )


def render_investigation(case: Case, state: GameState) -> None:
    """搜证：逐个场景勘察，找出隐藏证物。"""
    st.markdown("#### 🔦 现场搜证")
    st.caption("进入每一处场景，点击可疑之物仔细勘察。线索会自动记入侦探笔记。")
    cols = st.columns(2, gap="large")
    for i, scene in enumerate(case.scenes):
        with cols[i % 2]:
            _render_scene(scene, state)


def _render_suspect(suspect: Suspect, state: GameState) -> None:
    asked = sum(
        1 for i in range(len(suspect.questions)) if state.has_interrogated(f"{suspect.id}:{i}")
    )
    header = f"👤 {suspect.name}　·　口供 {asked}/{len(suspect.questions)}"
    with st.expander(header, expanded=False):
        st.markdown(f"<div class='clue-card'><em>{suspect.desc}</em></div>", unsafe_allow_html=True)
        st.markdown(f"**证词**：{suspect.alibi}")
        st.markdown(
            f"<div class='clue-card blood-hint'>🔦 破绽：{suspect.clue}</div>",
            unsafe_allow_html=True,
        )
        for i, qa in enumerate(suspect.questions):
            key = f"{suspect.id}:{i}"
            answered = state.has_interrogated(key)
            slot = st.empty()
            label = f"❓ {qa.question}" + ("　✔" if answered else "")
            if st.button(label, key=f"q_{key}", use_container_width=True):
                newly = not answered
                state.interrogate(key)
                if newly:
                    _typewriter(qa.answer, slot, "🗯️")
                else:
                    slot.markdown(
                        f"<div class='clue-card'>🗯️ {qa.answer}</div>", unsafe_allow_html=True
                    )
            elif answered:
                slot.markdown(f"<div class='clue-card'>🗯️ {qa.answer}</div>", unsafe_allow_html=True)


def render_interrogation(case: Case, state: GameState) -> None:
    """审讯：向嫌疑人提问，套出口供中的破绽。"""
    st.markdown("#### 🗣️ 审讯嫌疑人")
    st.caption("向每位嫌疑人抛出问题，从他们的回答里捕捉说谎的破绽。")
    cols = st.columns(2, gap="large")
    for i, suspect in enumerate(case.suspects):
        with cols[i % 2]:
            _render_suspect(suspect, state)


def render_notebook(case: Case, state: GameState) -> None:
    """侦探笔记：汇总已收集的证物与口供。"""
    st.markdown("#### 📓 侦探笔记")
    if state.found_count == 0 and state.interrogated_count == 0:
        st.info("笔记还是空白的。去现场搜证、审讯嫌疑人，线索会自动记录在此。")
        return

    st.markdown("**已收集的证物**")
    if state.found_count == 0:
        st.caption("——尚无证物——")
    for scene in case.scenes:
        for evi in scene.evidence:
            if state.has_evidence(evi.id):
                st.markdown(
                    f"<div class='clue-card'>{evi.icon} <strong>{evi.name}</strong>"
                    f"（{scene.name}）：{evi.detail}</div>",
                    unsafe_allow_html=True,
                )

    st.markdown("**关键口供**")
    any_q = False
    for suspect in case.suspects:
        for i, qa in enumerate(suspect.questions):
            if state.has_interrogated(f"{suspect.id}:{i}"):
                any_q = True
                st.markdown(
                    f"<div class='clue-card'>👤 <strong>{suspect.name}</strong> —— "
                    f"{qa.question}<br>🗯️ {qa.answer}</div>",
                    unsafe_allow_html=True,
                )
    if not any_q:
        st.caption("——尚无口供——")


def _render_result(case: Case, result: dict[str, bool], state: GameState) -> None:
    correct = sum(result.values())
    if all(result.values()):
        st.balloons()
        st.success("**真相大白！** 你完整还原了这桩午夜疑案。")
        st.markdown(f"<div class='clue-card'>{case.reveal}</div>", unsafe_allow_html=True)
        state.mark_solved()
        return

    labels = {"culprit": "凶手", "weapon": "凶器", "motive": "动机"}
    hits = "、".join(labels[k] for k, v in result.items() if v) or "无"
    st.warning(f"三项中你答对了 **{correct}/3**（正确：{hits}）。")
    remaining = case.max_accusations - state.attempts
    if remaining > 0:
        st.error(f"凶手在暗处冷笑……你还有 **{remaining}** 次定案机会。再核对笔记里的细节。")
    else:
        st.error("定案机会已用尽，凶手消失在雨夜中……")
        with st.expander("🕯️ 查看真相", expanded=True):
            st.markdown(
                f"凶手是 **{case.culprit_name}**，凶器为 **{case.weapon}**，"
                f"动机是 **{case.motive}**。"
            )
            st.markdown(f"<div class='clue-card'>{case.reveal}</div>", unsafe_allow_html=True)


def render_verdict(case: Case, state: GameState) -> None:
    """定案：同时指认凶手、凶器与动机。"""
    st.markdown("#### ⚖️ 最终定案")

    if state.solved:
        st.success("案件已侦破。真相已然大白，正义得到伸张。")
        st.markdown(f"<div class='clue-card'>{case.reveal}</div>", unsafe_allow_html=True)
        return

    if state.attempts >= case.max_accusations:
        st.error("定案机会已用尽。可点击左侧「重新展开卷宗」再来一次。")
        return

    ready = state.found_count >= case.total_evidence
    if not ready:
        missing = case.total_evidence - state.found_count
        st.info(f"证据尚不充分：还有 {missing} 件证物未找到。集齐全部证物方可定案。")
        return

    st.markdown("<p class='whisper'>证据已齐。现在，说出完整的真相。</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        culprit = st.radio("🧑‍⚖️ 凶手是谁？", case.suspect_names, index=None)
    with c2:
        weapon = st.radio("🔪 凶器是什么？", case.weapons, index=None)
    with c3:
        motive = st.radio("💭 动机为何？", case.motives, index=None)

    if st.button("🗡️ 提交定案", use_container_width=True):
        if not (culprit and weapon and motive):
            st.warning("请把凶手、凶器、动机三项都选好，再提交定案。")
            return
        state.record_attempt()
        result = case.check_solution(culprit, weapon, motive)
        _render_result(case, result, state)
