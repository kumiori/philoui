from types import SimpleNamespace

import streamlit as st

st.set_page_config(page_title="Input widget laboratory", page_icon="⌨️", layout="wide")

from philoui.io import (
    create_button,
    create_checkbox,
    create_equaliser,
    create_next,
    create_textinput,
    create_yesno,
    create_yesno_row,
)
from philoui.survey import CustomStreamlitSurvey, create_flag_ui


st.title("Input widget laboratory")
st.caption("Native Streamlit helpers, callbacks, return values, and session persistence.")

survey = CustomStreamlitSurvey(label="input_lab")
st.session_state.setdefault("callback_log", [])


def record(choice):
    st.session_state.callback_log.append(choice)


button_tab, binary_tab, form_tab, equaliser_tab = st.tabs(
    ["Buttons", "Binary choices", "Text and checkbox", "Equaliser and dates"]
)

with button_tab:
    normal, disabled, forward = st.columns(3)
    with normal:
        clicked = create_button(
            "input_primary",
            {"label": "Run action", "help": "A standard action button"},
        )
        st.write("Returned value", clicked)
    with disabled:
        disabled_clicked = create_button(
            "input_disabled", {"label": "Unavailable action", "disabled": True}
        )
        st.write("Returned value", disabled_clicked)
    with forward:
        next_clicked = create_next(
            "input_next", {"label": "Continue →", "use_container_width": True}
        )
        st.write("Returned value", next_clicked)

with binary_tab:
    st.subheader("Column buttons")
    column_choice = create_yesno(
        "input_yesno",
        {
            "labels": ("Accept", "Decline"),
            "callback": (lambda: record("accepted"), lambda: record("declined")),
        },
    )
    st.write("Returned value", column_choice)

    st.subheader("Compact row")
    row_choice = create_yesno_row(
        "input_yesno_row",
        {
            "labels": ("Keep", "Discard"),
            "callback": (lambda: record("kept"), lambda: record("discarded")),
        },
    )
    st.write("Returned value", row_choice)
    st.write("Callback log", st.session_state.callback_log)
    if st.button("Clear callback log"):
        st.session_state.callback_log = []
        st.rerun()

with form_tab:
    text_value = create_textinput(
        "input_free_text",
        {
            "survey": survey,
            "label": "Describe your current position",
            "help": "Tests empty, Unicode, punctuation, and long responses.",
        },
    )
    checked = create_checkbox(
        "input_consent", {"survey": survey, "label": "I confirm this response"}
    )
    st.write({"text": text_value, "confirmed": checked})

    st.subheader("Question flagging")
    pages = SimpleNamespace(current=0)
    create_flag_ui(pages, survey)

with equaliser_tab:
    dimensions = [
        ("Clarity", ""),
        ("Urgency", ""),
        ("Confidence", ""),
        ("Effort", ""),
    ]
    values = create_equaliser(
        "input_equaliser",
        id="input_equaliser",
        kwargs={"survey": survey, "data": dimensions},
    )
    st.write("Returned values", values)

    st.subheader("Mandatory date range")
    date_range = survey.mandatory_date_range(
        name="Active interval",
        id="input_date_range",
        key="input_date_range",
    )
    st.write("Returned value", date_range)

with st.expander("State diagnostics"):
    st.write("Survey data")
    st.json(survey.data)
    st.write("Relevant session state")
    state = {
        key: value
        for key, value in st.session_state.items()
        if key.startswith("input_") or key == "callback_log"
    }
    st.json(state)
