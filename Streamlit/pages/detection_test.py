import streamlit as st


def main(images):
    st.markdown("<h1 style='text-align: center;'>Test Images<h1>", unsafe_allow_html=True)
    idx = 0
    for i in range(10):
        cols = st.beta_columns(5)

        cols[0].image(images[idx], use_column_width=True)
        cols[1].image(images[idx + 1], use_column_width=True)
        cols[2].image(images[idx + 2], use_column_width=True)
        cols[3].image(images[idx + 3], use_column_width=True)
        cols[4].image(images[idx + 4], use_column_width=True)
        idx += 5
