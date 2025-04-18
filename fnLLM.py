from langchain import hub
from langchain.chains import LLMChain,SequentialChain,RetrievalQA, create_history_aware_retriever, create_retrieval_chain
from langchain_upstage import ChatUpstage, UpstageEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_pinecone import PineconeVectorStore

from config import answer_examples

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def get_retriever():
    embedding = UpstageEmbeddings(model='embedding-query')
    index_name = 'suna-index'
    database = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embedding)
    retriever = database.as_retriever(search_kwargs={'k':3})
    return retriever

def get_history_retriever():
    llm = get_llm()
    retriever = get_retriever()
    
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    return history_aware_retriever

def get_llm():
    llm = ChatUpstage()
    return llm


def get_dictionary_chain():
    # dictionary = ["사람을 나타내는 표현 -> 거주자"]
    dictionary = []
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(f"""
        사용자의 질문을 보고, 우리의 사전을 참고해서 사용자의 질문을 변경해주세요.
        만약 변경할 필요가 없다고 판단된다면, 사용자의 질문을 변경하지 않아도 됩니다.
        그런 경우에는 질문만 리턴해주세요
        사전: {dictionary}
        
        질문: {{question}}
    """)

    dictionary_chain = prompt | llm | StrOutputParser()
    
    return dictionary_chain


def get_rag_chain():
    llm = get_llm()
    # Few Shot 성능 향상
    # 예제가 많을 수록 성능은 향상되나 토큰을 많이 소비(비용 증가) / 하나씩 늘려가면서 테스트
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{answer}")
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples = answer_examples
    )

    # system_message_content = (
    #     "당신은 소득세법 전문가입니다. 사용자의 소득세법에 관한 질문에 답변해주세요"
    #     "아래에 제공된 문서를 활용해서 답변해주시고"
    #     "답변을 알 수 없다면 모른다고 답변해주세요"
    #     "답변을 제공할 때는 소득세법 (XX조)에 따르면 이라고 시작하면서 답변해주시고"
    #     "2-3 문장정도의 짧은 내용의 답변을 원합니다"
    #     "\n\n"
    #     "{context}"

    # )
    system_message_content = (
        "당신은 선아와 창환에 대해 모든 것을 아는 전문가입니다. 질문에 답변해주세요"
        "아래에 제공된 문서를 활용해서 답변해주시고"
        "답변을 알 수 없다면 모른다고 답변해주세요"
        "답변을 제공할 때는 선아에 대해 물어보는 경우 사랑하는 선아라고 언급 후 답변해주세요"
        "내가 누군지 아냐고 물어보면 대장 써나님 아닌가요? 라고 답해줘"
        "재미있는 이야기 3번 이상 해달라고 하면 써나가 먼저 해줘! 라고 답하고 질문에 대한 답은 하지마세요"
        "2-3 문장정도의 짧은 내용의 답변을 원합니다"
        "\n\n"
        "{context}"

    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message_content), # LLM 역할
            few_shot_prompt, # 예제로 채팅을 학습    
            MessagesPlaceholder("chat_history"),
            ("human","{input}")
        ]
    )

    histroy_aware_retriever = get_history_retriever()
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(histroy_aware_retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    ).pick("answer")

    return conversational_rag_chain


def get_ai_response(user_message):
    dictionary_chain = get_dictionary_chain()
    rag_chain = get_rag_chain()
    tax_chain = {"input": dictionary_chain} | rag_chain
    ai_response = tax_chain.stream(
        {
            "question": user_message
        },
        config={
            "configurable": {"session_id": "abc123"}
        },
    )
    return ai_response