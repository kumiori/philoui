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
                    create_next, create_qualitative, create_quantitative, create_textinput, create_yesno, create_yesno_row, fetch_and_display_data)
from philoui.survey import CustomStreamlitSurvey
from datetime import datetime
from philoui.geo import reverse_lookup
from philoui.texts import friendly_time
from philoui.presentation import PagedContainer
from philoui.authentication import _Authenticate
from philoui.matrices import generate_random_matrix, encode_matrix, display_matrix
from philoui.dictionary_manip import display_dictionary, display_dictionary_by_indices, display_details_description
from philoui.survey import CustomStreamlitSurvey
from philoui.texts import _stream_example, corrupt_string
from philoui.geo import get_coordinates

def main():
    st.title("Testing philoui Widgets")
    st.toast(f'Status: {st.secrets["runtime"]["STATUS"]}')
    
    # Example usage of philoui widgets
    with st.sidebar:
        st.markdown("## philoui widgets")
    survey = CustomStreamlitSurvey()
    st.subheader("Dichotomy Widget")

    create_dichotomy(key = 'trust', kwargs={'survey': survey, 
                                            'name': 'investor', 
                                           'label': 'Trust Level', 
                                           'question': 'How much do you trust the Trustee?', 
                                           'rotationAngle': 0, 
                                           'gradientWidth': 20,
                                           "inverse_choice": lambda x: 'full 🫧' if x == 1 else 'none 🕳️' if x == 0 else 'midway ✨' if x == 0.5 else 'partial 💩' if x < 0.5 else 'partial 🥀',  
                                           'messages': ["⛈️🔔🎐", "Sounds great!", "Going up or down?"],
                                           'height': 220, 
                                           'title': 'I trust',
                                           'invert': False, 
                                           'shift': 30})
    
    create_dichotomy(key = 'dichotomy', kwargs={'survey': survey, 
                                            'name': 'investor', 
                                           'label': 'Trust Level', 
                                           'question': 'How much do you trust the Trustee?', 
                                           'gradientWidth': 98,
                                           "inverse_choice": lambda x: 'full 🫧' if x == 1 else 'none 🕳️' if x == 0 else 'midway ✨' if x == 0.5 else 'partial 💩' if x < 0.5 else 'partial 🥀',  
                                           'messages': ["⛈️🔔🎐", "Sounds great!", "Going up or down?"],
                                           'height': 220, 
                                           'title': 'I trust',
                                           'invert': False, 
                                           'shift': 30})
    
    create_dichotomy(key = 'dichotomy_sharp', kwargs={'survey': survey, 
                                            'name': 'investor', 
                                           'label': 'Trust Level', 
                                           'gradientWidth': 3,
                                           'question': 'How much do you trust the Trustee?', 
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

    st.subheader("Equaliser Widget")

    create_equaliser(key = "equaliser", kwargs={"survey": survey, "data": equaliser_data})
    
    st.subheader("Next Widget")
    
    create_next("next", kwargs={"survey": survey})
    
    st.subheader("Globe Visualization Widget")

    create_globe("Settimia", kwargs={'database': 'gathering'})
    
        
    # Example 1: Create Button
    st.subheader("Button Widget")
    button_key = "demo_button"
    button_clicked = create_button(button_key)
    if button_clicked:
        st.success("Button clicked!")

    # Example 3: Create Qualitative Parametric
    st.subheader("Qualitative Parametric Widget")
    qualitative_key = "demo_qualitative"
    
    create_qualitative(qualitative_key, kwargs={"survey": survey})

    quantitative_key = "demo_quantitative"
    create_quantitative(quantitative_key, kwargs={"survey": survey})

    # Example 4: Create Yes/No Buttons
    st.subheader("Yes/No Buttons Widget")
    create_yesno_row("demo_yesno_row", kwargs={"survey": survey})

    create_yesno("demo_yesno", kwargs={"survey": survey})

    # Example 6: Create Text Input
    st.subheader("Text Input Widget")
    create_textinput("demo_textinput", kwargs={"survey": survey})

    # Example 7: Create Checkbox
    st.subheader("Checkbox Widget")
    create_checkbox("demo_checkbox", kwargs={"survey": survey})

if __name__ == "__main__":
    main()