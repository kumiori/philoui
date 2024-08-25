import streamlit as st
st.set_page_config(
    page_title="Phiosophical User Interface Portal",
    page_icon="✨",
    # layout="wide",
    initial_sidebar_state="collapsed"
)

import streamlit_survey as ss

from philoui.io import create_qualitative
from philoui.survey import CustomStreamlitSurvey
import streamlit.components.v1 as components

st.subheader("Qualitative Parametric Widget")
qualitative_key = "demo_qualitative"

survey = CustomStreamlitSurvey()

if st.secrets["runtime"]["STATUS"] == "Production":
    st.write(os.path.basename(__file__))
    root_dir = os.path.dirname(__file__)

    # Print the root directory
    st.write("Root directory:", root_dir)
    build_dir = os.path.join(os.path.split(root_dir)[0], "philoui/philoui_selectors/frontend/build")
    st.write("Build directory:", build_dir)
    _qualitative_selector = components.declare_component("qualitative", path=build_dir)
else:
    _qualitative_selector = components.declare_component(
        "philoui_selectors",
        url='http://localhost:3001'
    )
    
    
create_qualitative(qualitative_key, kwargs={"survey": survey})

def _quantitative(name, question, label, data_values, key=None):
    return _qualitative_selector(component = "qualitative",
    name = name,
    label = label,
    key=key,
    data_values  = data_values,
    question = question)

    
def _qualitative(name, question, label, areas, data_values = [1, 2, 10], key=None):
    return _qualitative_selector(component = "parametric",
    name = name,
    label = label,
    key=key,
    areas = areas,
    data_values  = data_values,
    question = question)

_qualitative("Qualitative", "How much do you like this?", "Like", areas = [1, 2, 3], data_values = [1, 1, 100], key=qualitative_key)
_quantitative("Quantitative", "How much do you like this?", "Like", [1, 2, 10])