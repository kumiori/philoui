import streamlit as st
import streamlit_survey as ss
from streamlit_vertical_slider import vertical_slider

import philoui as philoui

from philoui.io import (conn, create_button, create_checkbox, create_dichotomy, create_equaliser, create_globe,
                    create_next, create_qualitative, create_textinput, create_yesno, fetch_and_display_data)

def main():
    st.title("Testing philoui Widgets")
    
    # Example usage of philoui widgets
    with st.sidebar:
        st.markdown("## philoui widgets")
        
if __name__ == "__main__":
    main()