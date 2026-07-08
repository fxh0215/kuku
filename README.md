# 🕯️ 午夜疑案 · Suspense App

一个悬疑推理风格的 Streamlit 网页应用。你将扮演一名不请自来的访客，被困在雨夜的迷雾庄园中，通过审视嫌疑人、收集线索，最终揪出隐藏在暗处的凶手。

## ✨ 特性

- **沉浸式悬疑氛围**：暗色渐变背景、血红点缀、烛光闪烁标题动画与衬线字体。
- **多场景搜证**：书房、酒窖、阁楼、雨中花园四大场景，藏有 9 件可勘察的证物。
- **嫌疑人审讯**：向 4 名嫌疑人抛出多个问题，从口供中捕捉说谎的破绽。
- **侦探笔记**：已收集的证物与关键口供自动归档，随时回看推理。
- **三要素定案**：需同时指认「凶手 / 凶器 / 动机」，仅有 3 次定案机会。
- **打字机式揭示**：证物细节与口供以逐字浮现的方式呈现，紧张感十足。
- **进度追踪**：侧边栏实时显示证物收集、审讯进度与剩余定案机会。

## 📦 环境要求

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)（依赖与虚拟环境管理）

## 🚀 快速开始

Windows 用户可直接双击 `run.bat` 一键运行；或使用命令行：

```bash
# 克隆仓库
git clone git@github.com:fxh0215/kuku.git
cd kuku

# 安装依赖（uv 会自动创建虚拟环境）
uv sync

# 启动应用
uv run streamlit run app.py
```

启动后在浏览器打开终端提示的地址（默认 http://localhost:8501）即可开始调查。

## 🎮 玩法说明

1. 在序章中推开庄园大门，进入案发现场。
2. 在「现场搜证」标签逐一进入各场景，点击可疑之物勘察，集齐全部证物。
3. 在「审讯」标签向嫌疑人提问，套出口供里的破绽。
4. 随时切到「侦探笔记」回顾已掌握的证物与口供。
5. 证据齐备后，在「定案」标签同时选出凶手、凶器与动机并提交。
6. 三项全对即真相大白；答错会消耗定案机会，用尽则凶手逃逸。

## 📁 项目结构

采用 `src` 布局，按职责分层，界面、状态、数据与领域模型彼此解耦：

```
.
├── app.py                     # 薄入口：uv run streamlit run app.py
├── run.bat                    # Windows 一键运行脚本
├── src/suspense_app/
│   ├── __init__.py            # 包元信息与版本
│   ├── app.py                 # 应用组装：标签页编排（搜证/审讯/笔记/定案）
│   ├── cli.py                 # 命令行入口（suspense-app）
│   ├── models.py              # 领域模型：Case/Scene/Evidence/Suspect（含校验）
│   ├── data.py                # 案件剧本数据（场景、证物、审讯、真相）
│   ├── state.py               # 会话状态管理，隔离 session_state
│   ├── components.py          # 界面组件（搜证/审讯/笔记/定案/侧栏）
│   └── styles.py              # 悬疑风格主题 CSS
├── tests/                     # pytest 单元测试
├── pyproject.toml             # 元数据、依赖、脚本、ruff/pytest 配置
├── uv.lock                    # 依赖锁定文件
└── README.md
```

## 🧪 开发

```bash
# 安装含开发依赖（pytest、ruff）
uv sync --group dev

# 代码检查与格式化
uv run ruff check .
uv run ruff format .

# 运行测试
uv run pytest
```

也可通过安装后的命令行脚本启动：

```bash
uv run suspense-app
```

## 🛠️ 技术栈

- [Streamlit](https://streamlit.io/) —— 构建交互式网页界面
- [uv](https://docs.astral.sh/uv/) —— 依赖与虚拟环境管理
- [Ruff](https://docs.astral.sh/ruff/) —— 代码检查与格式化
- [pytest](https://docs.pytest.org/) —— 单元测试
- 自定义 CSS —— 打造悬疑视觉风格
