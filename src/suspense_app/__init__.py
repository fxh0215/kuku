"""《午夜疑案》—— 悬疑推理风格的 Streamlit 应用。"""

from suspense_app.models import Case, Evidence, Interrogation, Scene, Suspect

__all__ = ["Case", "Evidence", "Interrogation", "Scene", "Suspect", "__version__"]

__version__ = "0.3.0"
