from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS, Chroma
from langchain.storage import LocalFileStore
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.memory import ConversationBufferMemory


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
)

## retriever

cache_dir = LocalFileStore("./.cache/")

splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n",
    chunk_size=600,
    chunk_overlap=100,
)

loader = TextLoader("./files/input_text.txt")

docs = loader.load_and_split(text_splitter=splitter)

embeddings = OpenAIEmbeddings()

cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)

vectorstore = FAISS.from_documents(docs, cached_embeddings)

retriever = vectorstore.as_retriever()


## memory

memory = ConversationBufferMemory(return_message=True, memory_key="chat_history")


def load_memory(_):
    return memory.load_memory_variables({})["chat_history"]


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Read documents, and answer the question. 
            If you don't know the answer, just say that you don't know. Don't try to make up an answer.
            ------
            {context}
            """,
        ),
        ("human", "{question}"),
    ]
)

# chain = retriever | prompt | llm

chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough(),
        "chat_history": load_memory,
    }
    | prompt
    | llm
)


def chain_invoke(question):
    result = chain.invoke(question)
    memory.save_context(
        {"input": question},
        {"output": result.content},
    )
    print(result)
    print("---")


chain_invoke("Is Aaronson guilty?")
chain_invoke("What message did he write in the table?")
chain_invoke("Who is Julia?")

print(load_memory(None))
print(len(load_memory(None)))

# result = chain.invoke("Is Aaronson guilty?")
# print(result.content)
