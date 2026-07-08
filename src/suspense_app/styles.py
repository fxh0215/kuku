"""界面主题样式（悬疑风格 CSS）。"""

from __future__ import annotations

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
