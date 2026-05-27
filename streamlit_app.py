import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"] # for streamlit cloud deploy and work if you are running in local delete this line



# Store history
if "store" not in st.session_state:
    st.session_state.store = {}
store = st.session_state.store

# Chat UI messages store
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role":"assistant", "content":"Hi! how can i help you"}]


st.set_page_config(page_title="Bangla Chatbot", page_icon= "🌍")
st.title("Bangla Chatbot")

model_name = st.sidebar.selectbox("Choose GPT model",["gpt-4o-mini","gpt-5-nano"])
token_len = st.sidebar.slider("Select maximum output token length", min_value= 50, max_value= 300, value = 100)


llm_model = ChatOpenAI(model = model_name, max_completion_tokens= token_len, streaming = True)

prompt = ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistant. answer the following question simply. remember question will be in english, banglish and bangla language but you will always replay in bangla language. don't use word from any other language except Bangla"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user","Question : {question}")
])

chain = prompt | llm_model 

# session history function
def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="question", history_messages_key="chat_history")


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# clear chat with messages
if st.sidebar.button("Clear History"):
    st.session_state.store = {}
    st.session_state.messages = []
    st.rerun()

# user input
question = st.chat_input("Ask Anything")

if question:
    st.session_state.messages.append({"role":"user", "content":question})
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        answer = chain_with_history.stream(
            {"question": question},
            config = {
                "configurable":{"session_id":"user_1"}
            }
        )
        response = st.write_stream(answer)

    st.session_state.messages.append({"role":"assistant","content":response})



st.sidebar.markdown(
    """
        <div style = " background-color: #8dc6ff;
                       color : black;
                       padding : 7px;
                       border-radius: 10px;
                       text-align: center;
                       font-size:13px;
                       font-weight:200;"
        >Developed by Rachin
        </div>
    """,
    unsafe_allow_html= True
)