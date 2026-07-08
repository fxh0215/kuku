import random
import time
from datetime import datetime

import streamlit as st

st.set_page_config(
    page_title="午夜疑案",
    page_icon="🕯️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&display=swap');

.stApp {
    background:
        radial-gradient(circle at 20% 10%, rgba(80,0,20,0.25), transparent 40%),
        radial-gradient(circle at 80% 90%, rgba(0,30,60,0.25), transparent 40%),
        linear-gradient(160deg, #0a0a0f 0%, #12101a 50%, #05050a 100%);
    color: #cdcdd6;
    font-family: 'Noto Serif SC', serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d14 0%, #14101c 100%);
    border-right: 1px solid rgba(150,20,40,0.35);
}

h1, h2, h3 {
    font-family: 'Noto Serif SC', serif !important;
    color: #e8e2d0 !important;
    text-shadow: 0 0 12px rgba(150,20,40,0.5);
    letter-spacing: 2px;
}

.title-flicker {
    font-size: 3rem;
    font-weight: 900;
    text-align: center;
    color: #f0e6d2;
    text-shadow: 0 0 8px #a3162a, 0 0 20px rgba(150,20,40,0.6);
    animation: flicker 4s infinite;
    letter-spacing: 8px;
}

@keyframes flicker {
    0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { opacity: 1; text-shadow: 0 0 8px #a3162a, 0 0 24px rgba(150,20,40,0.7); }
    20%, 24%, 55% { opacity: 0.4; text-shadow: none; }
}

.clue-card {
    background: rgba(20,18,26,0.85);
    border-left: 3px solid #8c1220;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    font-size: 1.05rem;
    line-height: 1.7;
}

.whisper {
    color: #7a7a88;
    font-style: italic;
    text-align: center;
    letter-spacing: 3px;
}

.blood {
    color: #c0392b;
    font-weight: 700;
}

.stButton>button {
    background: linear-gradient(135deg, #2a0810, #4a0f1a);
    color: #e8d8c0;
    border: 1px solid #8c1220;
    border-radius: 3px;
    font-family: 'Noto Serif SC', serif;
    letter-spacing: 2px;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #4a0f1a, #7a1526);
    box-shadow: 0 0 16px rgba(150,20,40,0.6);
    color: #fff;
    border-color: #c0392b;
}

hr { border-color: rgba(150,20,40,0.3); }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

SUSPECTS = {
    "管家 · 陈伯": {
        "desc": "在庄园服侍了三十年，沉默寡言，指节上有陈年的伤疤。",
        "alibi": "案发时声称自己在酒窖清点藏酒。",
        "clue": "酒窖的灰尘上，只有一行进去的脚印，却没有出来的。",
    },
    "养女 · 苏晚": {
        "desc": "去世老人唯一的继承人，眼神里藏着不安。",
        "alibi": "她说自己一直在阁楼弹钢琴。",
        "clue": "那架钢琴的琴键，落满了三个月未擦的灰。",
    },
    "医生 · 林墨": {
        "desc": "老人的私人医生，随身皮箱从不离手。",
        "alibi": "他称自己在书房整理病历。",
        "clue": "书房壁炉里，还残留着未烧尽的处方纸角。",
    },
    "远房侄子 · 顾寒": {
        "desc": "深夜才赶到庄园，浑身被雨淋透。",
        "alibi": "他说自己的车在半路抛锚了。",
        "clue": "可他的鞋底，一点泥水都没有沾上。",
    },
}

INTRO = [
    "雨，下了整整一夜。",
    "庄园主人在书房里咽下了最后一口气，桌上的红茶还温着。",
    "警笛被大雨吞没，只有你——一个不请自来的访客，留在这栋孤宅里。",
    "四个人，四段说辞，只有一个真相。",
]

CULPRIT = "远房侄子 · 顾寒"


def typewriter(text, placeholder, delay=0.03):
    shown = ""
    for ch in text:
        shown += ch
        placeholder.markdown(f"<div class='clue-card'>{shown}▌</div>", unsafe_allow_html=True)
        time.sleep(delay)
    placeholder.markdown(f"<div class='clue-card'>{shown}</div>", unsafe_allow_html=True)


def main():
    if "started" not in st.session_state:
        st.session_state.started = False
    if "examined" not in st.session_state:
        st.session_state.examined = set()
    if "solved" not in st.session_state:
        st.session_state.solved = False

    st.markdown("<div class='title-flicker'>午 夜 疑 案</div>", unsafe_allow_html=True)
    st.markdown("<p class='whisper'>—— 真相，藏在无人愿意直视的角落 ——</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 🕯️ 案件档案")
        st.markdown(f"**时间**：{datetime.now():%Y-%m-%d %H:%M}")
        st.markdown("**地点**：迷雾庄园 · 书房")
        st.markdown("**状态**：<span class='blood'>调查进行中</span>", unsafe_allow_html=True)
        st.markdown("---")
        progress = len(st.session_state.examined) / len(SUSPECTS)
        st.markdown("**线索收集进度**")
        st.progress(progress)
        st.caption(f"已审视 {len(st.session_state.examined)} / {len(SUSPECTS)} 名嫌疑人")

    if not st.session_state.started:
        st.markdown("### 序 章")
        for line in INTRO:
            st.markdown(f"<div class='clue-card'>{line}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 推开那扇门，开始调查"):
            st.session_state.started = True
            st.rerun()
        return

    st.markdown("### 🔍 审视嫌疑人")
    st.caption("逐一查看每个人的证词，寻找说谎的破绽。")

    cols = st.columns(2)
    for i, (name, info) in enumerate(SUSPECTS.items()):
        with cols[i % 2]:
            with st.expander(f"👤 {name}", expanded=False):
                st.markdown(f"*{info['desc']}*")
                st.markdown(f"**证词**：{info['alibi']}")
                if st.button(f"仔细勘察", key=f"btn_{name}"):
                    st.session_state.examined.add(name)
                    ph = st.empty()
                    typewriter(f"🔦 {info['clue']}", ph)

    st.markdown("<hr>", unsafe_allow_html=True)

    if len(st.session_state.examined) == len(SUSPECTS):
        st.markdown("### ⚖️ 指认凶手")
        st.markdown("<p class='whisper'>所有线索已收集完毕。现在，说出那个名字。</p>", unsafe_allow_html=True)
        choice = st.radio("你认为凶手是谁？", list(SUSPECTS.keys()), index=None)
        if st.button("🗡️ 揭晓真相"):
            if choice == CULPRIT:
                st.balloons()
                st.success(f"**真相大白。** 凶手正是 {CULPRIT}。")
                st.markdown(
                    "<div class='clue-card'>雨夜里，一个鞋底干净的人，"
                    "绝不可能是从抛锚的车上走来的。他早已潜伏在庄园，"
                    "只为那份即将改写的遗嘱。</div>",
                    unsafe_allow_html=True,
                )
                st.session_state.solved = True
            else:
                st.error("凶手在你的注视下，露出了一丝冷笑……再想想那些对不上的细节。")
    else:
        st.info("线索尚不充分，先勘察完所有嫌疑人吧。")


if __name__ == "__main__":
    main()
