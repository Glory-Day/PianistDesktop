import os.path

import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import Streamlit.pages.abstract as abstract
import Streamlit.pages.introduction as introduction
import Streamlit.pages.detection_test as detection_test
import Streamlit.pages.object_detection as object_detection
import Streamlit.pages.computer_vision as computer_vision

import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


# returns vary depending on whether csv or image file
def read_file(path: str):
    if path.split('.')[1] == 'csv':
        return pd.read_csv(path)
    else:
        return Image.open(path).convert('RGB')


def main():
    # folder paths
    abstract_path = 'Streamlit/resource/abstract'
    introduction_path = 'Streamlit/resource/introduction'
    object_detection_path = 'Streamlit/resource/object_detection'
    detection_test_path = 'Streamlit/resource/detection_test'
    computer_vision_path = 'Streamlit/resource/computer_vision'

    # load folder's files
    abstract_files = os.listdir(abstract_path)
    introduction_files = os.listdir(introduction_path)
    object_detection_files = os.listdir(object_detection_path)
    detection_test_files = os.listdir(detection_test_path)
    computer_vision_files = os.listdir(computer_vision_path)

    # set page to dictionary
    pages = {
        "Abstract": abstract,
        "Introduction": introduction,
        "Object Detection": object_detection,
        "Detection Test": detection_test,
        "Computer Vision": computer_vision
    }

    # set page's image to dictionary
    images = {
        "Abstract": [read_file(abstract_path + '/' + name) for name in abstract_files],
        "Introduction": [read_file(introduction_path + '/' + name) for name in introduction_files],
        "Object Detection": [read_file(object_detection_path + '/' + name) for name in object_detection_files],
        "Detection Test": [read_file(detection_test_path + '/' + name) for name in detection_test_files],
        "Computer Vision": [read_file(computer_vision_path + '/' + name) for name in computer_vision_files]
    }

    st.sidebar.title("Subjects list")
    selection = st.sidebar.beta_expander("Choose page's subject", False).radio('', list(pages.keys()))

    page = pages[selection]

    with st.spinner(f'Loading {selection}...'):
        page.main(images[selection])


if __name__ == "__main__":
    main()
