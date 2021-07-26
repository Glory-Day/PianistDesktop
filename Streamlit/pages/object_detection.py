import streamlit as st
import pandas as pd

from PIL import Image


def main(images):
    # main title
    st.markdown("<h1 style='text-align: center;'>Object Detection<h1>", unsafe_allow_html=True)
    # subtitle
    st.markdown("## **1. Virtual Machine**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    # image - align center
    col1, col2, col3 = st.beta_columns([1, 6, 1])
    with col1:
        st.write("")
    with col2:
        st.image(images[0])
    with col3:
        st.write("")
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Google Cloud Platform<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.markdown("```\n"
                "                                      Environment\n"
                "CPU : 48 vCPU\n"
                "GPU : NVIDIA Tesla A100 x 4\n"
                "RAM : 340GB memory\n"
                "Disk : 20GB balanced persistent disk\n"
                "OS : Ubuntu 18.04 LTS\n"
                "Pytorch : 1.8.1 version\n"
                "CUDA: 11.1 version"
                "```")

    st.write("작은 이미지를 검출해야하기 때문에 큰 이미지를 넣어 작은 이미지를 강제로 키우는 방식을 사용했습니다."
             " 큰 이미지를 학습하기 때문에 GPU Memory를 많이 사용하여 VM 환경에서 학습했습니다.")
    st.markdown("---")
    st.markdown("## **2. YOLO V5 학습 및 결과**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Train Graph<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    # TODO: Insert graph image
    st.markdown("```\n"
                "$ python -m torch.distributed.launch main.py --batch 2"
                " --data data.yaml --weights yolov5x.pt --device 0,1,2,3\n"
                "hyperparameter: {Epoch: 1000, Image-Size: 2048x2048, Batch-Size: 2}\n"
                "```")
    st.write("객체 검출이나 분류의 오차는 점점 줄어들고, 평균 정확도는 점점 상승하는 그래프를 보이고 있습니다. 향후 계획은"
             " 큰 이미지다 보니 Batch-Size를 더 크게할 수 없었는데, 다양한 Batch-Size를 두고 학습을 해보고 싶습니다.")

