from typing import Literal
import streamlit as st

MARGINS = {
    "top": "0",
    "bottom": "0",
}

STICKY_CONTAINER_HTML = """
<style>
    div[data-testid="stBlock"] > div {{
        overflow: auto; /* May need specifics depending on your layout */
        position: relative;
        padding-top: 1rem; /* Optional additional spacing */
    }}
    div[data-testid="stBlock"] div:has(> div.fixed-header-{i}) {{
        position: sticky;
        {position}: {margin};
        background-color: white;
        z-index: 999;
        padding: 0.5rem;
        border: 1px solid #ccc;
    }}
</style>
<div class="fixed-header-{i}"></div>
""".strip()

count = 0

def sticky_container(
    *,
    height: int | None = None,
    border: bool | None = None,
    mode: Literal["top", "bottom"] = "top",
    margin: str | None = None,
):
    if margin is None:
        margin = MARGINS[mode]

    global count
    html_code = STICKY_CONTAINER_HTML.format(position=mode, margin=margin, i=count)
    count += 1

    container = st.container()
    container.markdown(html_code, unsafe_allow_html=True)
    with container:
        if height is not None:
            st.write(f'<div style="min-height: {height}px;"></div>', unsafe_allow_html=True)
        if border:
            st.write(f'<div style="border: 1px solid #ccc;"></div>', unsafe_allow_html=True)
    return container