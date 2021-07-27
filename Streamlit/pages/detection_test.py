import streamlit as st


def main(resources):
    # set image names
    image_names = ['1st Image', '2nd Image', '3rd Image'] + [f"{i}th Image" for i in range(4, 51)]

    # set images and image names to dictionary
    dictionary_images = {}
    for i in range(len(resources)):
        dictionary_images[image_names[i]] = resources[i]

    # main title
    st.markdown("<h1 style='text-align: center;'>Test Images<h1>", unsafe_allow_html=True)

    # select box
    option = st.selectbox('Please select test image', image_names)

    st.markdown("---")

    # show selected test image
    col1, col2, col3 = st.beta_columns([1, 6, 1])
    with col1:
        st.write("")
    with col2:
        st.image(dictionary_images[option])
    with col3:
        st.write("")

    # figure image name
    st.markdown(f"<h5 style='text-align: center;'>Fig. {option}<h5>", unsafe_allow_html=True)
