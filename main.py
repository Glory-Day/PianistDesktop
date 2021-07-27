import os.path

import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import Streamlit.pages.abstract as abstract
import Streamlit.pages.introduction as introduction
import Streamlit.pages.detection_test as detection_test
import Streamlit.pages.object_detection as object_detection
import Streamlit.pages.debugging as debugging

import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def introduction_page():
    st.title("Intro page")


def iterator_page():
    st.title("Iterator")


def main():
    test_files = os.listdir('Streamlit/resource/image/test')

    pages = {
        "Abstract": abstract,
        "Introduction": introduction,
        "Object Detection": object_detection,
        "Detection Test": detection_test,
        "Debugging": debugging
    }

    images = {
        "Abstract": [Image.open('Streamlit/resource/image/piano.jpg')],
        "Introduction": [Image.open('Streamlit/resource/image/music_symbol.png'),
                         Image.open('Streamlit/resource/image/model_comparison.png').convert("RGBA"),
                         Image.open('Streamlit/resource/image/overview.png'),
                         pd.read_csv('Streamlit/resource/data/test_names.csv'),
                         Image.open('Streamlit/resource/image/roboflow.png')],
        "Object Detection": [Image.open('Streamlit/resource/image/google-cloud-platform.jpg')],
        "Detection Test": [Image.open('Streamlit/resource/image/test/' + path) for path in test_files],
        "Debugging": [Image.open('Streamlit/resource/image/detection_image.jpg'),
                      pd.read_csv('Streamlit/resource/data/label.csv')]
    }

    st.sidebar.title("Subjects list")
    selection = st.sidebar.beta_expander("Choose page's subject", False).radio('', list(pages.keys()))

    page = pages[selection]

    with st.spinner(f'Loading {selection}...'):
        page.main(images[selection])


if __name__ == "__main__":
    main()
