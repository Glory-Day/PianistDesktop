import streamlit as st
from PIL import Image


def main(resources):
    # main title
    st.markdown("<h1 style='text-align: center;'>Project Pianist<h1>", unsafe_allow_html=True)

    # logo image
    col1, col2, col3 = st.beta_columns([1.8, 6, 1])
    with col1:
        st.write("")
    with col2:
        st.image(resources[0].resize((400, 400), Image.ANTIALIAS))
    with col3:
        st.write("")

    st.markdown("---")

    # subtitle
    st.markdown("## **Abstract**")

    # content
    st.write('현재 대부분의 리듬게임 채보들은 사람의 노력으로 제작되고 있습니다.'
             ' 채보에서 중요한 것은 음악과 얼마나 어울리는가가 중요합니다. 박자나 위치 노트의 길이까지 세세하게 잘 맞아떨어지는 채보는 '
             '플레이어들에게 리듬게임을 하게하는 중요한 원동력입니다. 이번 프로젝트는 과연 "이 조화를 찾는 일을 기계가 할 수 있는가?"라는 '
             '질문에서 시작되었습니다.')
