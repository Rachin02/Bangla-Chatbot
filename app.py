
from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Langsmith tracking
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "Bangla Chatbot"
os.environ["LANGSMITH_TRACKING"] = "true"

# prompt
prompt = ChatPromptTemplate.from_messages(
  [
   ("system", "You are a helpful assistant. answer the following question simply"),
    ("user", "Question: {question}")
  ]
 )

# function to generate answer
def generate_answer(question, model, token):
    model = ChatOpenAI(model = model , max_tokens = token)
    parser = StrOutputParser()
    chain = prompt | model | parser

    response = chain.invoke({"question": question})
    return response

# Title of the web
st.title("Bangla Chatbot")

# sidebar for setting
model =  st.sidebar.selectbox("Select GPT model", ["gpt-4o-mini", "gpt-5-nano", "gpt-5.4-nano"])

# output token lenght define
token = st.sidebar.slider("Select output respons length in tokens", min_value= 30, max_value= 200, value = 100)

# inferface for user input
# st.write("Ask me anything...")
question = st.text_input("Ask me anything: ")
st.write(question)