
import streamlit as st
import sys
import os

from fnNews import *
from fnStock import *
from fnChatBot import *

# .py가 있는 경로를 추가
sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))


def fnSidebar():
    st.sidebar.markdown(f"## SideBar 항목")

    # 상태 초기화
    if "selected_folder" not in st.session_state:
        st.session_state["selected_folder"] = None
    if "selected_file" not in st.session_state:
        st.session_state["selected_file"] = None

    # 폴더와 파일 데이터 정의
    folders = {
        "News": {
            "경제": "https://www.mk.co.kr/rss/30100041/",
            "기업/경영": "https://www.mk.co.kr/rss/50100032/",
            "금융": "https://www.mk.co.kr/rss/50200011/",
            "부동산": "https://www.mk.co.kr/rss/50300009/",
            "문화/연예" : " https://www.mk.co.kr/rss/30000023/"
        },
        "주식": ["국내 주식", "파일 2-2", "파일 2-3"],
        "C": ["파일 3-1", "파일 3-2", "파일 3-3"],
    }
        
    # 부모 항목 (폴더) 선택
    selected_folder = st.sidebar.selectbox("폴더 선택", ["폴더를 선택하세요"] + list(folders.keys()))


    # 부모 항목 선택 시 하위 항목 표시
    if selected_folder != "폴더를 선택하세요":
        st.session_state["selected_folder"] = selected_folder
        selected_file = st.sidebar.radio(f"📁 {selected_folder} 하위 항목", folders[selected_folder])
        st.session_state["selected_file"] = selected_file
        print(selected_folder)
    

    if st.session_state["selected_file"]:
        if selected_folder == "News":
            st.write(f"**선택한 파일:** {st.session_state['selected_file']}")
            st.write(f"여기에 **{st.session_state['selected_file']}**의 내용을 표시합니다.")
            # 내용 표시
            st.write(f"### {st.session_state['selected_file']} News")
            print(folders["News"][st.session_state['selected_file']])
            rss_url = folders["News"][st.session_state['selected_file']]
            fnGetNews(rss_url)
        
        if selected_folder == "주식":
            st.write(f"**선택한 파일:** {st.session_state['selected_file']}")
            st.write(f"여기에 **{st.session_state['selected_file']}**의 내용을 표시합니다.")
            fnStock()
            print(st.session_state['selected_file'])
        
        if selected_folder == "C":
            st.write(f"**선택한 파일:** {st.session_state['selected_file']}")
            st.write(f"여기에 **{st.session_state['selected_file']}**의 내용을 표시합니다.")

