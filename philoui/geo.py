from opencage.geocoder import OpenCageGeocode
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def get_coordinates(api_key, city):
    geocoder = OpenCageGeocode(api_key)
    results = geocoder.geocode(city)

    if results and len(results):
        first_result = results[0]
        lat, lng = first_result['geometry']['lat'], first_result['geometry']['lng']
        return lat, lng
    else:
        return None


def create_map(key, kwargs = {}):
    # _c = st.session_state.coordinates
    _c = kwargs.get("coordinates", None)
    
    if _c:
        with st.spinner():
            _lookup = reverse_lookup(st.secrets.opencage["OPENCAGE_KEY"], _c)
    
        data = _lookup
        # # Access relevant information from the first entry
        first_entry = data[0][0]
        sun_rise = first_entry["annotations"]["sun"]["rise"]["astronomical"]
        sun_set = first_entry["annotations"]["sun"]["set"]["astronomical"]
        geographical_region = str(list(first_entry["annotations"]["UN_M49"]["regions"])[-3]).title()
        confidence = first_entry["confidence"]
        st.markdown(f"### The Sun rises from the east and sets in the west.")
    #     st.markdown(f"## The geographical region is {geographical_region} and the political union is {political_union}.")
        st.markdown(f"## Our confidence in  level is {confidence}.")
        # sun_rise_readable = datetime.utcfromtimestamp(sun_rise).strftime('%H:%M:%S UTC')
        # sun_set_readable = datetime.utcfromtimestamp(sun_set).strftime('%H:%M:%S UTC')
        # st.markdown(f"`At {_c} the sun rises at {friendly_time(sun_rise)} in the morning, and sets at {friendly_time(sun_set)} in the evening.`")
        # st.markdown(f"The sun rises at {sun_rise_readable} and sets at {sun_set_readable} in {text}.")

        if geographical_region:
            st.markdown(f"## Forward, confirming that you connect from `{geographical_region}`")


    assert _c, "We need a location to connect our map, go Back to enter"
    
    df = pd.DataFrame({
        "col1": np.random.randn(1000) / 10 + (_c[0]),
        "col2": np.random.randn(1000) / 10 + ((_c[1]) % 360),
        "col3": np.random.randn(1000) * 100,
        "col4": np.random.rand(1000, 4).tolist(),
    })

    st.map(df,
        latitude='col1',
        longitude='col2',
        size='col3',
        color='col4',
        zoom=6,
        use_container_width=True)
    st.markdown('## A _matrix is a map where patterns emerge_')


def reverse_lookup(api_key, location):
    geocoder = OpenCageGeocode(api_key)
    results = geocoder.reverse_geocode(location[0], location[1])

    if results and len(results):
        first_result = results[0]
        return results,
    else:
        return None