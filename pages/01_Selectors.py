import os

import streamlit as st


os.environ.setdefault("PHILOUI_COMPONENT_URL", "http://localhost:3001")
st.set_page_config(page_title="Selector laboratory", page_icon="🎛️", layout="wide")

from philoui.survey import CustomStreamlitSurvey


st.title("Selector laboratory")
st.caption("React component round-trips through the development server on port 3001.")

survey = CustomStreamlitSurvey(label="selector_lab")

with st.sidebar:
    st.header("Dichotomy controls")
    gradient_width = st.slider("Gradient width (%)", 0, 100, 30, 5)
    height = st.slider("Component height", 80, 260, 150, 10)
    rotation = st.slider("Rotation angle", -15, 15, 0)
    invert = st.toggle("Invert colours")
    st.divider()
    st.caption("Component source")
    st.code(os.environ["PHILOUI_COMPONENT_URL"], language=None)

dichotomy_tab, qualitative_tab, quantitative_tab, matrix_tab = st.tabs(
    ["Dichotomy", "Qualitative", "Quantitative", "Variant matrix"]
)

with dichotomy_tab:
    st.subheader("Configurable spectrum")
    value = survey.dichotomy(
        name="participant",
        label="Confidence",
        question="Where does your position sit between the two limits?",
        gradientWidth=gradient_width,
        height=height,
        rotationAngle=rotation,
        invert=invert,
        shift=0,
        key="lab_dichotomy",
    )
    st.write("Returned value", value)

    st.subheader("Three-column presentation")
    component_column, response_column = st.columns([3, 1])
    with component_column:
        three_column_value = survey.dichotomy(
            name="participant",
            label="Agreement",
            question="Choose a position and inspect its interpreted value.",
            gradientWidth=gradient_width,
            height=height,
            rotationAngle=rotation,
            invert=invert,
            shift=0,
            key="lab_dichotomy_columns",
        )
    with response_column:
        st.metric(
            "Interpreted value",
            f"{float(three_column_value):.0%}" if three_column_value is not None else "—",
        )
        st.write("Raw value", three_column_value)

with qualitative_tab:
    st.subheader("Nested qualitative regions")
    qualitative_values = ["outside", "near", "inside", "core"]
    qualitative = survey.qualitative_parametric(
        name="Proximity",
        question="Which region best represents your relationship to the proposal?",
        label="Region",
        areas=len(qualitative_values),
        data_values=qualitative_values,
        key="lab_qualitative",
    )
    st.write("Returned value", qualitative)
    st.caption(f"Configured values: {qualitative_values}")

with quantitative_tab:
    st.subheader("Nested quantitative levels")
    quantitative_values = [0, 1, 10, 100]
    quantitative = survey.quantitative(
        name="Commitment",
        question="Select the order of magnitude you would commit.",
        label="Amount",
        data_values=quantitative_values,
        key="lab_quantitative",
    )
    st.write("Returned value", quantitative)
    st.caption(f"Configured values: {quantitative_values}")

with matrix_tab:
    st.subheader("Boundary and transition coverage")
    st.write("Use these fixed variants to compare geometry without changing controls.")
    variants = [
        ("Hard boundary", 0, False),
        ("Narrow transition", 10, False),
        ("Wide transition", 80, False),
        ("Inverted transition", 35, True),
    ]
    for index, (label, width, inverted) in enumerate(variants):
        with st.expander(label, expanded=index == 0):
            result = survey.dichotomy(
                name="tester",
                label=label,
                question=f"gradientWidth={width}, invert={inverted}",
                gradientWidth=width,
                height=110,
                rotationAngle=0,
                invert=inverted,
                shift=0,
                key=f"matrix_dichotomy_{index}",
            )
            st.write("Returned value", result)

with st.expander("Survey diagnostics"):
    st.json(survey.data)
    st.caption("Values should update here immediately after each component click.")
