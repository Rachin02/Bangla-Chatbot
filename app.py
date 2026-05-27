from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
# from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Langsmith tracking
# os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")  #use these for local use 
# os.environ["LANGSMITH_PROJECT"] = "Bangla Chatbot"
# os.environ["LANGSMITH_TRACING"] = "true"

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]           #use this for streamlit cloude use
os.environ["LANGSMITH_API_KEY"] = st.secrets["LANGSMITH_API_KEY"]

# store history
# persistent store
if "store" not in st.session_state:
    st.session_state.store = {}

store = st.session_state.store

# session history get
def get_session_history(session_id:str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    return store[session_id]


# prompt
prompt = ChatPromptTemplate.from_messages(
  [
   ("system", "You are a helpful assistant. answer the following question simply. remember question will be in english, banglish and bangla language but you will always replay in bangla language. don't use word from any other language except Bangla"),
   MessagesPlaceholder(variable_name= "history"),
    ("user", "Question: {question}")
  ]
 )

# function to generate answer
def generate_answer(question, model, token):
    model = ChatOpenAI(model = model, max_completion_tokens= token)

    # parser = StrOutputParser()
    chain = prompt | model 

    # add memory
    chain_with_memory = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="question", history_messages_key= "history")

    return chain_with_memory.stream(
        {"question":question},
        config = {
            "configurable":{
                "session_id":"user_1"
            }
        })

# Title of the web
st.title("Bangla Chatbot")

# sidebar for setting
model =  st.sidebar.selectbox("Select GPT model", ["gpt-4o-mini", "gpt-4.1-nano", "gpt-5.4-nano"])

# output token lenght define
token = st.sidebar.slider("Select output response length in tokens", min_value= 30, max_value= 300, value = 100) 

# inferface for user input
question = st.text_input("Ask me anything: ")

# answer
if st.button("Ask"):
    if question:
        answer = generate_answer(question, model, token)
        st.write_stream(answer)
        # st.write(store["user_1"].messages)
    else:
        st.write("ask question")

    











