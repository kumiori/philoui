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
from philoui import texts
from philoui.texts import _stream_example, corrupt_string, stream_once_then_write
from philoui.geo import get_coordinates
import streamlit_shadcn_ui as ui
from streamlit_timeline import timeline

st.write(st.secrets["runtime"]["STATUS"])

if 'location' not in st.session_state:
    st.session_state.location = None

if 'coordinates' not in st.session_state:
    st.session_state.coordinates = None


if 'read_texts' not in st.session_state:
    st.session_state['read_texts'] = set()

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

import time
import string

def _stream_example(text, damage=0):
  # Define sleep lengths for different punctuation symbols
  sleep_lengths = {'.': 1.5, ',': 0.5, '!': 1.7, '?': 2.5, ';': 1.4, ':': 1.4}
  sleep_lengths = {key: value * (1. + damage) for key, value in sleep_lengths.items()}

  for i, word in enumerate(text.split()):
      # Check if the last character is a punctuation symbol
      last_char = word[-1] if word[-1] in string.punctuation else None

      # Yield the word with appropriate sleep length
      if last_char == '.' or last_char == '?' or last_char == '^':
          yield word + " \n "
      else:
          yield word + " "
      
      if last_char and last_char in sleep_lengths:
          time.sleep(sleep_lengths[last_char])
      else:
          time.sleep(0.3)

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

    create_equaliser(key = "equaliser", id="equaliser", kwargs={"survey": survey, "data": equaliser_data})
    
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
    
    create_qualitative(qualitative_key, kwargs={"survey": survey, "label": "Quali2", "key": "demo_qualitative_2", "data_values": [1, 2]})

    quantitative_key = "demo_quantitative"
    create_quantitative(quantitative_key, kwargs={"survey": survey})


    quanti_2 = create_quantitative(quantitative_key, kwargs={"survey": survey, "label": "Quanti2", "key": "demo_quantitative_2",  "data_values": [1, 2], "name": "Sovereign,"})
    st.write(quanti_2)
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

    
    st.subheader("""Default Stream then Write""")
    
    text = """
There are really 4 philosophical questions
who started it?
are we gonna make it?
where are we gonna put it?
who's gonna clean up?
                           """
                           
    stream_once_then_write(text)
    
    # st.markdown("""
    # <pre>
    # def _stream_example(text, damage):
    #     # Define sleep lengths for different punctuation symbols
    #     sleep_lengths = {'.': 1., ',': 0.3, '!': 1.7, '?': 1.5, ';': 0.4, ':': 0.4}
    #     sleep_lengths = {key: value * (1. + damage) for key, value in sleep_lengths.items()}

    #     for i, word in enumerate(text.split()):
    #         # Check if the last character is a punctuation symbol
    #         last_char = word[-1] if word[-1] in string.punctuation else None

    #         # Yield the word with appropriate sleep length
    #         if last_char == '.' or last_char == '?' or last_char == '^':
    #             yield word + " \n "
    #         else:
    #             yield word + " "
            
    #         if last_char and last_char in sleep_lengths:
    #             time.sleep(sleep_lengths[last_char])
    #         else:
    #             time.sleep(0.3)
    #     </pre>            
    # """, unsafe_allow_html=True) 
    
    stream_once_then_write("""
cute .. of confronting ourself with the most radical problem of humans' rekation to their world
yet at the same tiem thiss vast extension of jknowledge adn power
beig out of control
lacking the wisdom 
enormity of our information
and our technical skill

                           """, stream_function=_stream_example)
                  
if __name__ == "__main__":
    main()