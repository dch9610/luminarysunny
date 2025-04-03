import streamlit as st
from dotenv import load_dotenv

from app_Main import go_to_page
from fnLLM import get_ai_response

def fnChatBot():
    load_dotenv()
    # 홈으로 돌아가기 버튼
    if st.button("홈으로 돌아가기",key="to_home"):
        go_to_page("Home")
        st.rerun() # 2번 클릭 방지

    if 'message_list' not in st.session_state:
        st.session_state.message_list = []

    for message in st.session_state.message_list:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if user_question := st.chat_input(placeholder="궁금한 내용 입력!"):
        with st.chat_message("user"):
            st.write(user_question)
        st.session_state.message_list.append({"role":"user", "content":user_question})

        with st.spinner("답변을 생성 중입니다."):
            ai_message = get_ai_response(user_question)
            #ai_message = "AI"
            with st.chat_message("ai"):
                st.write(ai_message)
            st.session_state.message_list.append({"role":"ai", "content":ai_message})
    print("ChatBot")