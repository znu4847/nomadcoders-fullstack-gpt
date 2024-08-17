from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI

llm = OpenAI()
chat = ChatOpenAI()

a = llm.predict("How many planets are there?")
b = chat.predict("How many planets are there?")
