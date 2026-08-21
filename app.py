import streamlit as st


st.set_page_config(
    page_title="philoui widget laboratory",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("philoui widget laboratory")
st.caption("Interactive coverage for the public widget helpers and components.")

st.markdown(
    """
Use the pages in the sidebar to test one concern at a time:

- **Selectors** exercises the React dichotomy, qualitative, and quantitative
  components against the development server on port 3001.
- **Inputs** covers the Python wrapper widgets, callbacks, returned values, and
  survey state.
- **Display utilities** covers deterministic non-network helpers such as
  pagination, dictionaries, matrices, and text transformations.

Every example shows its current return value. The diagnostics at the bottom of
each page make reruns and state transitions visible during manual QA.
"""
)

left, middle, right = st.columns(3)
left.metric("Selector families", 3)
middle.metric("Input helpers", 7)
right.metric("External services required", 0)

st.info(
    "The test laboratory deliberately avoids Supabase, geocoding, microphone, "
    "and authentication calls. Those integrations require credentials or host "
    "hardware and should be covered by separate integration tests."
)
