"""Low-level access to the bundled philoui selector component."""

import os
from pathlib import Path

import streamlit.components.v1 as components


_development_url = os.getenv("PHILOUI_COMPONENT_URL")
_component_options = (
    {"url": _development_url}
    if _development_url
    else {"path": str(Path(__file__).parent / "frontend" / "build")}
)
_my_component = components.declare_component("qualitative", **_component_options)


def my_component(name, greeting="Hello", key=None):
    return _my_component(name=name, greeting=greeting, default=0, key=key)
