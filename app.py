import streamlit as st

st.set_page_config(
    page_title="Phiosophical User Interface Portal",
    page_icon="✨",
    # layout="wide",
    initial_sidebar_state="collapsed",
)
import streamlit_survey as ss
from streamlit_vertical_slider import vertical_slider

from philoui.io import (
    conn,
    create_button,
    create_checkbox,
    create_dichotomy,
    create_equaliser,
    create_globe,
    create_next,
    create_qualitative,
    create_quantitative,
    create_textinput,
    create_yesno,
    create_yesno_row,
    fetch_and_display_data,
)
from philoui.survey import CustomStreamlitSurvey


def main():
    st.title("Testing philoui Widgets")
    st.toast(f'Status: {st.secrets["runtime"]["STATUS"]}')

    st.markdown("""
### This helps us have difficult conversations                
                
We are currently in the testing phase of our _philosophically informed_ user interface widgets. These are designed to facilitate user interactions and coordination games. Thoughtful design and intuitive elements, to enhance user experience whilst making communication actionable.

We start by breaking down a Dichotomy, a division (a separation, of elements, sets, ...) between two that are opposed. This concept is often used to highlight the differences between two _mutually exclusive_ categories. 

Explore preferences and opinions on a spectrum between two opposing points, _including the interface_ (or boundary). This not only helps in capturing nuanced user inputs but also encourages reflective thinking and a deeper appreciation of the complexity of choices (understanding, beliefs, preferences, etc.).
    """)

    # Example usage of philoui widgets
    with st.sidebar:
        st.markdown("## philoui widgets")
    survey = CustomStreamlitSurvey()
    st.subheader("Dichotomy Widget")

    create_dichotomy(
        key="trust",
        kwargs={
            "survey": survey,
            "name": "fellow",
            "label": "Trust Level",
            "question": "How can you choose between two sides of a spectrum?",
            "rotationAngle": 0,
            "gradientWidth": 20,
            "inverse_choice": lambda x: "full 🫧"
            if x == 1
            else "none 🕳️"
            if x == 0
            else "midway ✨"
            if x == 0.5
            else "partial 💩"
            if x < 0.5
            else "partial 🥀",
            "messages": ["⛈️🔔🎐", "Sounds great!", "Going up or down?"],
            "height": 220,
            "title": "I trust",
            "invert": False,
            "shift": 30,
        },
    )

    create_dichotomy(
        key="dichotomy",
        kwargs={
            "survey": survey,
            "name": "friend",
            "label": "Trust Level",
            "question": "How is the spectrum?",
            "gradientWidth": 98,
            "inverse_choice": lambda x: "full 🫧"
            if x == 1
            else "none 🕳️"
            if x == 0
            else "midway ✨"
            if x == 0.5
            else "partial 💩"
            if x < 0.5
            else "partial 🥀",
            "messages": ["⛈️🔔🎐", "Sounds great!", "Going up or down?"],
            "height": 220,
            "title": "I trust",
            "invert": False,
            "shift": 30,
        },
    )

    create_dichotomy(
        key="dichotomy_sharp",
        kwargs={
            "survey": survey,
            "name": "investor",
            "label": "Trust Level",
            "gradientWidth": 3,
            "question": "What is the boundary?",
            "inverse_choice": lambda x: "full 🫧"
            if x == 1
            else "none 🕳️"
            if x == 0
            else "midway ✨"
            if x == 0.5
            else "partial 💩"
            if x < 0.5
            else "partial 🥀",
            "messages": ["⛈️🔔🎐", "Sounds great!", "Going up or down?"],
            "height": 220,
            "title": "I trust",
            "invert": False,
            "shift": 30,
        },
    )


if __name__ == "__main__":
    main()
