import streamlit as st
import streamlit.components.v1 as components
from streamlit_vertical_slider import vertical_slider 
import streamlit_survey as ss
import os 
from streamlit_extras.mandatory_date_range import date_range_picker 

component_url = os.getenv("PHILOUI_COMPONENT_URL")
if component_url:
    _qualitative_selector = components.declare_component(
        "philoui_selectors",
        url=component_url,
    )
else:
    build_dir = os.path.join(
        os.path.dirname(__file__), "philoui_selectors", "frontend", "build"
    )
    _qualitative_selector = components.declare_component(
        "qualitative", path=build_dir
    )

def _dichotomy(widget_label, question, name="", rotationAngle = 0, gradientWidth = 40, height = 100, invert = False, shift = 0, key=None):
    return _qualitative_selector(component = "dichotomy",
    name = name,
    label = widget_label,
    key=key,
    height=height,
    question = question,
    rotationAngle = rotationAngle,
    gradientWidth = gradientWidth,
    invert = invert,
    shift = shift
    )
    
def _qualitative(widget_label, question, areas, name="", data_values=None, height=120, key=None):
    if data_values is None:
        data_values = [1, 2, 10]
    return _qualitative_selector(component = "parametric",
    name = name,
    label = widget_label,
    key=key,
    areas = areas,
    data_values = data_values,
    question = question,
    height = height)

def parametric_quantitative(widget_label, question, data_values, name="", height=120, key=None):
    return _qualitative_selector(component = "qualitative",
    name = name,
    label = widget_label,
    key=key,
    data_values  = data_values,
    question = question,
    height = height)

def _date_range_picker(widget_label,
                       name = None,
                        default_start = None, 
                        default_end = None,
                        min_date = None,
                        max_date = None,
                        error_message = "",
                        id=None, key=None):
        
    return date_range_picker(
        name or widget_label,
        default_start = default_start,
        default_end = default_end,
        min_date = min_date,
        max_date = max_date,
        error_message = error_message,
        key=key,
        )

Dichotomy = ss.SurveyComponent.from_st_input(_dichotomy)
VerticalSlider = ss.SurveyComponent.from_st_input(vertical_slider)
ParametricQualitative = ss.SurveyComponent.from_st_input(_qualitative)
ParametricQuantitative = ss.SurveyComponent.from_st_input(parametric_quantitative)
Button = ss.SurveyComponent.from_st_input(st.button)
MandatoryDateRange = ss.SurveyComponent.from_st_input(_date_range_picker)
# MandatoryDateRange = ss.SurveyComponent.from_st_input(_date_range_picker)

class CustomStreamlitSurvey(ss.StreamlitSurvey):
    shape_types = ["circle", "square", "pill"]

    def dichotomy(self, label: str = "", id: str = None, **kwargs) -> str:
        return Dichotomy(self, label, id, **kwargs).display()
    
    def equaliser(self, label: str = "", id: str = None, **kwargs) -> str:
        return VerticalSlider(self, label, id, **kwargs).display()

    def qualitative_parametric(self, label: str = "", id: str = None, key=None, **kwargs):
        return ParametricQualitative(self, label, id, key=key, **kwargs).display()

    def quantitative(self, label: str = "", id: str = None, key=None, **kwargs):
        return ParametricQuantitative(self, label, id, key=key, **kwargs).display()

    def button(self, label: str = "", id: str = None, **kwargs) -> str:
        return Button(self, label, id, **kwargs).display()

    def mandatory_date_range(self, name: str = "", id: str = None, **kwargs) -> str:
        return MandatoryDateRange(self, label=name, id=id, **kwargs).display()

def create_flag_ui(pages, survey):
    # Checkbox to flag the question
    flag_question = st.checkbox(f"This question (Q{pages.current + 1}) is inappropriate, misplaced, ill-formed, abusive, unfit, or unclear")

    # If the question is flagged, show a text input for the user to provide details
    flag_reason = ""
    
    if "flagged_questions" not in survey.data:
        survey.data["flagged_questions"] = {}

    if flag_question:
        flag_reason = st.text_area("Let me specify why I think this question is inappropriate or unclear...")
        survey.data["flagged_questions"][f"Question {pages.current + 1}"] = {
                        "reason": flag_reason
                    }
