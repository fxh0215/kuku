"""界面主题样式（悬疑风格 CSS）。"""

from __future__ import annotations

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&display=swap');

.stApp {
    background:
        radial-gradient(circle at 20% 10%, rgba(120,20,40,0.28), transparent 45%),
        radial-gradient(circle at 80% 90%, rgba(20,60,110,0.28), transparent 45%),
        linear-gradient(160deg, #1c1c26 0%, #232030 50%, #16141d 100%);
    color: #ece8e0;
    font-family: 'Noto Serif SC', serif;
}

.stApp, .stApp p, .stApp li, .stApp span, .stApp label, .stMarkdown {
    color: #ece8e0;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #24222e 0%, #2a2536 100%);
    border-right: 1px solid rgba(200,60,80,0.45);
}

[data-testid="stSidebar"] * {
    color: #ece8e0 !important;
}

h1, h2, h3 {
    font-family: 'Noto Serif SC', serif !important;
    color: #fbf6ea !important;
    text-shadow: 0 0 14px rgba(200,60,80,0.55);
    letter-spacing: 2px;
}

.title-flicker {
    font-size: 3rem;
    font-weight: 900;
    text-align: center;
    color: #fff8ec;
    text-shadow: 0 0 10px #e0455a, 0 0 26px rgba(220,70,90,0.7);
    animation: flicker 4s infinite;
    letter-spacing: 8px;
}

@keyframes flicker {
    0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { opacity: 1; text-shadow: 0 0 10px #e0455a, 0 0 28px rgba(220,70,90,0.8); }
    20%, 24%, 55% { opacity: 0.65; text-shadow: none; }
}

.clue-card {
    background: rgba(48,44,58,0.9);
    border-left: 4px solid #c8324a;
    border-radius: 5px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    box-shadow: 0 4px 18px rgba(0,0,0,0.45);
    font-size: 1.08rem;
    line-height: 1.8;
    color: #f2eee6;
}

.whisper {
    color: #b8b2c4;
    font-style: italic;
    text-align: center;
    letter-spacing: 3px;
}

.blood {
    color: #ff6b7d;
    font-weight: 700;
}

.blood-hint {
    border-left-color: #ff6b7d !important;
    color: #ffd7dd !important;
}

.stButton>button {
    background: linear-gradient(135deg, #5a1626, #7a1f33);
    color: #fdf3e6;
    border: 1px solid #c8324a;
    border-radius: 4px;
    font-family: 'Noto Serif SC', serif;
    font-weight: 700;
    letter-spacing: 2px;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #7a1f33, #a52a44);
    box-shadow: 0 0 18px rgba(220,70,90,0.7);
    color: #ffffff;
    border-color: #ff6b7d;
}

[data-testid="stExpander"] {
    background: rgba(40,37,50,0.6);
    border: 1px solid rgba(200,60,80,0.35);
    border-radius: 6px;
}
[data-testid="stExpander"] summary {
    color: #f2eee6 !important;
    font-weight: 700;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #c8324a, #ff6b7d);
}

.stRadio label, .stCaption, [data-testid="stCaptionContainer"] {
    color: #cfc9d6 !important;
}

hr { border-color: rgba(200,60,80,0.4); }
</style>
"""
