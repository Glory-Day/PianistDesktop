import streamlit as st
import pandas as pd
from PIL import Image


def main(resources):
    # main title
    st.markdown("<h1 style='text-align: center;'>Introduction<h1>", unsafe_allow_html=True)

    # subtitle
    st.markdown("## **1. 음악 기호와 객체의 관계**")
    st.markdown(" ")
    st.markdown(" ")

    # image - align center
    col1, col2, col3 = st.beta_columns([1.7, 6, 1])
    with col1:
        st.write("")
    with col2:
        st.image(resources[1].resize((400, 400), Image.ANTIALIAS))
    with col3:
        st.write("")

    # figure image name
    st.markdown("<h5 style='text-align: center;'>Fig. Music Symbols<h5>", unsafe_allow_html=True)
    st.markdown(" ")

    # content
    st.write("음악 기호란 음악을 시각적으로 표현하기위한 시각적 정보입니다."
             " 각 기호마다 뜻하는 의미가 다르고 위치 정보 또한 의미하는 바가 있습니다."
             " 이는 객체가 가지는 특성과 일치합니다.")
    st.markdown("#### **Example: 4분 음표**")
    st.markdown("* Fields:\n"
                "   - 1박자\n"
                "   - 위치: {x:80, y:160}\n"
                "* Methods:\n"
                "   - 해당 높이의 음정으로 1박자만큼 소리낸다.")
    st.write("따라서 해당 기호를 localization(bounding box)해주고, 해당 box안에 있는 객체가 무엇인지"
             " classification도 해주는 object detection을 이용해 악보를 분석하는 것이 적절하다 판단하였습니다.")

    st.markdown("---")

    # subtitle
    st.markdown("## **2. Object Detection - YOLO V5**")
    st.markdown(" ")
    st.markdown(" ")

    # image
    st.image(resources[0])

    # figure image name
    st.markdown("<h5 style='text-align: center;'>Fig. YOLO V5 Model Types<h5>", unsafe_allow_html=True)
    st.markdown(" ")

    # content
    st.write("Object Detection Model중에서 YOLO V5를 선택했습니다. R-CNN 계열, SSD 계열의"
             " Model도 좋지만 탐지 속도와 정확도를 동시에 챙기기 위해서 입니다.")

    st.markdown("---")

    # subtitle
    st.markdown("## **3. Dataset - DeepScore**")
    st.markdown(" ")
    st.markdown(" ")

    # image
    st.image(resources[2])

    # figure image name
    st.markdown("<h5 style='text-align: center;'>Fig. DeepScore Dataset<h5>", unsafe_allow_html=True)
    st.markdown(" ")

    # content
    st.write("객체를 정확하게 감지할 수 있도록 학습하기 위해서는 정확한 Dataset이 필요합니다."
             " YOLO V5에서 음악 기호들을 감지할 수 있도록 Lukas Tuggener이 제작한 Dataset인 DeepScore를 사용했습니다.")

    # dataframe
    train_df = resources[4]
    st.markdown(" ")

    # image - align center
    col1, col2, col3 = st.beta_columns([0.5, 6, 0.5])
    with col1:
        st.write("")
    with col2:
        st.dataframe(train_df)
    with col3:
        st.write("")

    # figure image name
    st.markdown("<h5 style='text-align: center;'>Fig. DeepScore Train Dataset<h5>", unsafe_allow_html=True)
    st.markdown(" ")

    # content
    st.write("bounding box의 위치 정보를 YOLO V5에 맞추기 위해 Roboflow에서 Dataset을 수정했습니다.")

    # image
    st.image(resources[3])

    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Roboflow<h5>", unsafe_allow_html=True)
    st.markdown("---")

    # subject
    st.markdown("## **4. Reference**")
    st.markdown(" ")
    st.markdown(" ")

    # content
    st.markdown("```\n"
                "PyTorch-YOLO V5 : https://github.com/ultralytics/yolov5\n"
                "DeepScore : https://tuggeluk.github.io/\n"
                "Roboflow : https://roboflow.com/\n"
                "```")




