"""命令行入口：``suspense-app`` 启动 Streamlit 应用。"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    """通过 Streamlit CLI 启动应用。"""
    from streamlit.web import cli as st_cli

    entry = Path(__file__).resolve().parent / "app.py"
    sys.argv = ["streamlit", "run", str(entry)]
    st_cli.main()


if __name__ == "__main__":
    main()
