import random

import streamlit as st

st.set_page_config(page_title="Display utility laboratory", page_icon="🧪", layout="wide")

from philoui.dictionary_manip import (
    display_details_description,
    display_dictionary,
    display_dictionary_by_indices,
)
from philoui.matrices import display_matrix, encode_matrix, generate_random_matrix
from philoui.presentation import PagedContainer
from philoui.texts import corrupt_string, hash_text, mask_string, match_input


st.title("Display utility laboratory")
st.caption("Deterministic checks for display and transformation helpers.")

dictionary_tab, matrix_tab, text_tab, pagination_tab = st.tabs(
    ["Dictionary", "Matrix", "Text", "Pagination"]
)

sample_dictionary = {
    "Boundary": ["Where two positions meet."],
    "Transition": ["A region in which a response can vary."],
    "Commitment": ["A value returned by a selector."],
}

with dictionary_tab:
    full, sliced = st.columns(2)
    with full:
        st.subheader("Full dictionary")
        display_dictionary(sample_dictionary)
    with sliced:
        st.subheader("Index slice [0:2]")
        display_dictionary_by_indices(sample_dictionary, [0, 2])
    st.subheader("Detail row")
    display_details_description("Return value", "The raw value emitted by the widget.")

with matrix_tab:
    size = st.slider("Matrix size", 2, 6, 3)
    seed = st.number_input("Random seed", min_value=0, value=7, step=1)
    random.seed(seed)
    matrix = generate_random_matrix(size)
    st.subheader("Generated matrix")
    display_matrix(matrix)
    try:
        encoded = encode_matrix(matrix)
        st.subheader("Unicode encoding")
        st.dataframe(encoded, use_container_width=True)
    except ValueError as error:
        st.warning(f"Encoding requires equal-width Unicode rows: {error}")

with text_tab:
    text = st.text_area("Source text", "A careful interface makes state visible.")
    damage = st.slider("Damage", 0.0, 1.0, 0.2, 0.05)
    if st.button("Corrupt a reproducible sample"):
        random.seed(11)
        corrupted, replaced = corrupt_string(text, damage)
        st.session_state["utility_corruption"] = {
            "text": corrupted,
            "characters_replaced": replaced,
        }
    st.write(st.session_state.get("utility_corruption", "Run the sample to generate output."))
    st.code(f"SHA-256: {hash_text(text)}", language=None)
    st.write("Masked", mask_string(text))

    vocabulary = {"accept": "Yes", "decline": "No", "defer": "Not yet"}
    lookup = st.text_input("Case-insensitive translation lookup", "yes")
    st.write("Matching keys", match_input(lookup, vocabulary))

with pagination_tab:
    items = [f"Test record {number}" for number in range(1, 11)]
    per_page = st.slider("Items per page", 1, 5, 3)
    pager = PagedContainer(items, items_per_page=per_page)
    total_pages = pager.get_total_pages()
    page = st.number_input(
        "Page", min_value=1, max_value=total_pages, value=1, step=1
    )
    pager.display_page(page - 1)
    st.write({"items": len(items), "pages": total_pages, "current_page": page})
