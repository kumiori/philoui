import streamlit as st
st.set_page_config(
    page_title="Phiosophical User Interface Portal",
    page_icon="✨",
    # layout="wide",
    initial_sidebar_state="collapsed"
)

import streamlit_survey as ss
from streamlit_vertical_slider import vertical_slider

import philoui as philoui

from philoui.io import (conn, create_button, create_checkbox, create_dichotomy, create_equaliser, create_globe,
                    create_next, create_qualitative, create_textinput, create_yesno, fetch_and_display_data)
from philoui.survey import CustomStreamlitSurvey
from philoui.io import create_button, create_dichotomy, create_qualitative, create_yesno, create_yesno_row, create_next, create_globe, create_textinput, create_checkbox, create_equaliser, fetch_and_display_data, conn

def main():
    st.title("Testing philoui Widgets")
    
    # Example usage of philoui widgets
    with st.sidebar:
        st.markdown("## philoui widgets")
    survey = CustomStreamlitSurvey()
    create_dichotomy(key = 'trust', kwargs={'survey': survey, 
                                            'name': 'investor', 
                                           'label': 'Trust Level', 
                                           'question': 'How much do you trust the Trustee?', 
                                           'rotationAngle': 0, 
                                           'gradientWidth': 10,
                                           "inverse_choice": lambda x: 'full 🫧' if x == 1 else 'none 🕳️' if x == 0 else 'midway ✨' if x == 0.5 else 'partial 💩' if x < 0.5 else 'partial 🥀',  
                                           'messages': ["⛈️🔔🎐", "Sounds great!", "Going up or down?"],
                                           'height': 220, 
                                           'title': 'I trust',
                                           'invert': False, 
                                           'shift': 30})
    
    equaliser_data = [
            ("Social Media Presence", ""),
            ("Conceptual/Business", ""),
            ("Investor Relations", ""),
            ("Product Development", ""),
            ("Event Planning", ""),
        ]
    create_equaliser(key = "equaliser", kwargs={"survey": survey, "data": equaliser_data})
    
    create_globe("Settimia", kwargs={'database': 'gathering'})
    
if __name__ == "__main__":
    main()