import streamlit as st
from streamlit_lottie import st_lottie

import json
import sys
import os

# 초기 세션 상태 설정
if "page" not in st.session_state:
    st.session_state["page"] = "Home"
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "page_stack" not in st.session_state:
    st.session_state["page_stack"] = []

# utils.py가 있는 경로를 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

# JSON을 읽어 들이는 함수
def loadJSON(path):
    f = open(path, 'r', encoding='utf-8')
    res = json.load(f)
    f.close()
    return res

# 페이지 전환 함수
def go_to_page(page_name):
    st.session_state["page"] = page_name
    

# 홈 페이지
def Home():
        # 로고 Lottie와 타이틀 출력
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        lottie = loadJSON('./resource/json/lottie-full-movie-experience-including-music-news-video-weather-and-lots-of-entertainment.json')
        st_lottie(lottie, speed=5, loop=True, width=150, height=150)
    with col2:
        ''
        ''
        st.title('SPC')
    with col3:
        # 홈으로 돌아가기 버튼
        if st.button("Home",key="to_home"):
            go_to_page("Home")
            st.rerun() # 2번 클릭 방지

    if st.button("Chatbot",key="to_chat"):
        go_to_page("fnChatBot")
        st.rerun() # 2번 클릭 방지
        


if __name__ == "__main__":
    from fnSideBar import *
    #Home()
    # 페이지 라우팅
    if st.session_state["page"] == "Home":
        Home()
    elif st.session_state["page"] == "fnChatBot":
        fnChatBot()


    fnSidebar()

