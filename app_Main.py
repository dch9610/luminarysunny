import streamlit as st
from streamlit_lottie import st_lottie

import json
import sys
import os

from fnSideBar import *

# utils.py가 있는 경로를 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

# JSON을 읽어 들이는 함수
def loadJSON(path):
    f = open(path, 'r', encoding='utf-8')
    res = json.load(f)
    f.close()
    return res

# 로고 Lottie와 타이틀 출력
col1, col2 = st.columns([1,2])
with col1:
    lottie = loadJSON('./resource/json/sunny.json')
    st_lottie(lottie, speed=5, loop=True, width=150, height=150)
with col2:
    ''
    ''
    st.title('Title_')

fnSidebar()