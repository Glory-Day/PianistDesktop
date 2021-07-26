import streamlit as st
import os.path
import cv2

import sys
import pandas as pd
from PIL import Image


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from PianistDesktop.utils.score import Score


def main(images):
    label_path = 'resource/data/0005.txt'
    image_path = 'resource/image/0005.jpg'

    notes = ''

    score = Score(label_path=label_path, image_path=image_path)

    # main title
    st.markdown("<h1 style='text-align: center;'>Debugging<h1>", unsafe_allow_html=True)
    # subtitle
    st.markdown("## **1. Detection Objects**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    st.image(images[0])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Detected by YOLO V5<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.write("악보에 있는 객체들의 종류와 위치 정보를 알기위해 YOLO V5를 이용해서 Object Detection을 수행한다."
             " 위의 이미지는 Detection된 객체들을 시각적으로 보도록 Boundiong Box를 감싼 이미지이고,"
             " 정보는 TXT파일 형태로 저장된다.")
    st.write(images[1])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Detected Data<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.markdown("---")
    # subtitle
    st.markdown("# **2. Iterator I**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    st.image(score.debugging.images[0])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Iterator I<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.write("대략적인 오선의 위치를 추정하기 위해 높은 음자리와 낮음음자리의 위치 정보를"
             " 이용, 각 음자리표의 중앙값을 구한다음 그 사이를 범위의 경계로 설정한다.")
    st.markdown("---")
    # subtitle
    st.markdown("# **3. 오선 좌표 검출**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    st.image(score.debugging.images[1])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Detected Actual Lines<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.write("악보 이미지를 수평으로 정렬을 하면 가장 긴 선들을 특정할 수 있다. 정렬한 방향의 반대로 수직으로"
             " 검은 점의 위치를 탐색하여, 일정한 규칙을 가진 5개의 좌표 집합을 오선의 좌표로 저장한다.")
    st.markdown("---")
    # subtitle
    st.markdown("# **4, 허프 변환을 이용한 사각형 검출**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    st.image(score.debugging.images[2])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Detected Rectangle Objects<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.write("Beam(8분음표나 16음표 등을 연결됬다고 표현하는 사각형의 기호), 2분쉼표, 온쉼표는 너무 작고 변칙적이라"
             " Object Detection을 사용하는데 효율이 잘 나오지 않는다. 따라서 공통적인 특징인 사각형임을 이용해서"
             " 허프 변환 검출을 해서 모든 사각형들을 검출해 저장한다. 이는 다음 단계에서 정확히 분류를 한다.")
    st.markdown("---")
    # subtitle
    st.markdown("# **5. Iterator II**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    st.image(score.debugging.images[3])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Iterator II<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.write("보표(큰 보표, 작은 보표)별로 음표가 어떤 보표에 속해있는지 분리하기 위해"
             " 탐색 범위를 검출한 오선의 최대, 최소 값으로 설정한다.")
    st.markdown("---")
    # subtitle
    st.markdown("# **6. Iterator 내부 범위의 Component 분류**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    st.image(score.debugging.images[4])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Inner Components in Iterator II<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.write("재설정한 탐색 범위내에 Component들은 무조건 해당 범위에 속하기 때문에 해당 보표에 해당되는 저장 공간에 저장한다.")
    st.markdown("---")
    # subtitle
    st.markdown("# **7. Iterator 외부 범위의 Component 분류**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    st.image(score.debugging.images[5])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Outer Components in Iterator II<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.write("탐색 범위 내의 Component들을 전체 Component들이 저장된 공간에서 제거한다. 그러면 남은 Component들은"
             " 외부에 있는 Component들인데 해당 Component의 중앙에서 위아래로 탐색 범위를 탐색하여 먼저 닿은"
             " 탐색 범위를 가진 보표에 해당되는 것이고 해당 보표의 저장공간에 저장한다.")
    st.markdown("---")
    # subtitle
    st.markdown("# **8. Iterator III**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    st.image(score.debugging.images[6])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Iterator III<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.write("보표들은 현재 각 보표에 해당되는 Component들이 저장되어있다. 음높이의 최대를 정하기"
             " 위해 탐색 범위를 보표별 Component들의 최대, 최소 높이로 재설정한다.")
    st.markdown("---")
    # subtitle
    st.markdown("# **9. Beam과 4분음표 머리부분 연결**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    st.image(score.debugging.images[7])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Connection Beam with 1/4 Note's Head<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.write("저장된 사각형 객체들은 불필요한 객체까지 포함되어있다. Beam을 먼저 선별한다. "
             "원리는 Beam은 4분음표만이 가질 수 있다. 따라서 가로(4분음표), 세로(해당 보표의 탐색 범위)의 "
             "범위를 정하고 BFS 알고리즘을 이용해서 흰색은 제외 검은색을 가진 픽셀로만 이동하도록 한다. "
             "4분음표의 중앙에서 출발하여 결과적으로 Beam의 중앙으로 도착하면 해당 4분음표는 8분음표가 된다")
    st.markdown("---")
    # subtitle
    st.markdown("# **10. 가상 선 생성**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    st.image(score.debugging.images[8])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Create Virtual Line<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.write("음높이를 출력하기 위해 실제 오선의 간격들을 구한 다음, 간격을 반으로 나눠 탐색 범위만큼 내부에 생성한다.")
    st.markdown("---")
    # subtitle
    st.markdown("# **11. 2분, 온음표 검출**")
    # empty space
    st.markdown(" ")
    st.markdown(" ")
    st.image(score.debugging.images[9])
    # figure image
    st.markdown("<h5 style='text-align: center;'>Fig. Detected Whole and Half Rests<h5>", unsafe_allow_html=True)
    st.markdown(" ")
    st.write("2분쉼표와 온음표는 각각 2번, 3번줄에만 위치한다. 2번, 3번줄에서 BFS 알고리즘을 이용해서 사각형 객체에 도달한다면 해당 사각형 객체는 2분, 온쉼표이다.")

    with open('note.txt', 'w', encoding='utf-8') as file:
        file.write(notes)

    # st.markdown(f'```f{score.notes}```')
