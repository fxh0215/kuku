@echo off
setlocal
title 午夜疑案 · 悬疑推理
cd /d "%~dp0"

echo ============================================
echo    午夜疑案 . 正在点亮烛火...
echo ============================================
echo.

where uv >nul 2>nul
if errorlevel 1 (
    echo [错误] 未检测到 uv，请先安装: https://docs.astral.sh/uv/
    echo.
    pause
    exit /b 1
)

echo [1/2] 正在同步依赖...
set UV_LINK_MODE=copy
uv sync
if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败，请检查网络后重试。
    pause
    exit /b 1
)

echo.
echo [2/2] 正在启动应用，浏览器将自动打开...
echo 若未自动打开，请手动访问终端提示的地址 ^(默认 http://localhost:8501^)
echo 关闭本窗口即可停止应用。
echo.

uv run python -m streamlit run app.py

echo.
echo 应用已停止。
pause
