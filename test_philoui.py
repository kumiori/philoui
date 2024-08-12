import streamlit as st
st.set_page_config(
    page_title="Phiosophical User Interface Portal",
    page_icon="✨",
    # layout="wide",
    initial_sidebar_state="collapsed"
)

import streamlit_survey as ss
from streamlit_vertical_slider import vertical_slider

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
import streamlit_shadcn_ui as ui
from streamlit_timeline import timeline

if 'location' not in st.session_state:
    st.session_state.location = None

if 'coordinates' not in st.session_state:
    st.session_state.coordinates = None

current_year = datetime.now().year

timeline_data = {
    "title": {
        "media": {
          "url": "",
          "caption": " <a target=\"_blank\" href=''>credits</a>",
          "credit": ""
        },
        "text": {
          "headline": "Welcome to<br>Athena's Timeline",
          "text": "<p>A Timeline component by integrating ... from ...</p>"
        }
    },
    "events": [
      {
        "media": {
          "url": "https://vimeo.com/143407878",
          "caption": "How to Use TimelineJS (<a target=\"_blank\" href='https://timeline.knightlab.com/'>credits</a>)"
        },
        "start_date": {
          "year": "2016",
          "month":"1"
        },
        "text": {
          "headline": "Athena's Collective<br> participatory timelines.",
          "text": "<p>Athena's Collective is ... </p>"
        }
      },
      {
        "media": {
          "url": "https://www.youtube.com/watch?v=CmSKVW1v0xM",
          "caption": "Streamlit Components (<a target=\"_blank\" href='https://streamlit.io/'>credits</a>)"
        },
        "start_date": {
          "year": "2020",
          "month":"7",
          "day":"13"
        },
        "text": {
          "headline": "Streamlit Components<br>version 0.63.0",
          "text": "Streamlit lets you turn data scripts into sharable web apps in minutes, not weeks. It's all Python, open-source, and free! And once you've created an app you can use our free sharing platform to deploy, manage, and share your app with the world."
        }
      },
      {
        "media": {
          "url": "https://github.com/innerdoc/streamlit-timeline/raw/main/component-logo.png",
          "caption": "github/innerdoc (<a target=\"_blank\" href='https://www.github.com/innerdoc/'>credits</a>)"
        },
        "start_date": {
          "year": "2021",
          "month":"2"
        },
        "text": {
          "headline": "Streamlit TimelineJS component",
          "text": "Started with a demo on https://www.innerdoc.com/nlp-timeline/ . <br>Then made a <a href='https://github.com/innerdoc/streamlit-timeline'>Streamlit component</a> of it. <br>Then made a <a href='https://pypi.org/project/streamlit-timeline/'>PyPi package</a> for it."
        }
      }
    ]
}

def main():
    st.title("Testing philoui Widgets")
    st.toast(f'Status: {st.secrets["runtime"]["STATUS"]}')
    
    st.markdown("""
### This helps us have very difficult conversations                
                
We are currently in the testing phase of our _philosophically informed_ user interface widgets. These widgets are designed to facilitate engaging and meaningful user interactions within the context of our upcoming coordination games. By leveraging thoughtful design and intuitive elements, we aim to enhance user experience and foster deeper connections and understanding through our platform.

We start by breaking down _decision systems_ unpacking the Concept of 'Dichotomy' 
A dichotomy refers to a division (a separation) between two things (elements, sets, ...) that are represented as being entirely different or opposed. This concept is often used to highlight the differences between two _mutually exclusive_ categories, ideas, or phenomena. 

In our widgets, the 'dichotomy' functionality allows users to explore their preferences and opinions on a spectrum between two opposing points, _including the interface_ (or boundary). This not only helps in capturing nuanced user inputs but also encourages reflective thinking and a deeper appreciation of the complexity of choices and understanding (beliefs, preferences, etc.).
    """)
    
    st.markdown("""
Three approaches to presenting dichotomous choices with interface design cater to different user preferences and contexts, providing engaging and reflective experiences that align with our philosophical inquiry.


    """)
    # Example usage of philoui widgets
    with st.sidebar:
        st.markdown("## philoui widgets")
    survey = CustomStreamlitSurvey()
    st.subheader("Dichotomy Widget")

    create_dichotomy(key = 'trust', kwargs={'survey': survey, 
                                            'name': 'fellow', 
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
    create_textinput("open_text_input", kwargs={"survey": survey})

    # Example 6: Create Text Input
    st.subheader("Location Widget")
    create_textinput("Location", kwargs={"survey": survey})

    # Example 7: Create Checkbox
    st.subheader("Checkbox Widget")
    create_checkbox("demo_checkbox", kwargs={"survey": survey})

    st.subheader("Badges Widget")
    ui.badges(badge_list=[("applications", "default"), ("theory", "destructive")], class_name="flex gap-2", key="main_badges")

    st.subheader("Card Widget")
    ui.card(title="Inside", content="+1", description="+∞ from last checkpoint", key="card").render()

    st.subheader("Timeline Widget")
    timeline(timeline_data, height=800)


if __name__ == "__main__":
    main()