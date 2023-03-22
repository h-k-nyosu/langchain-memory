import httpx
from fastapi import APIRouter, Depends, BackgroundTasks
from app.models.prompt import PromptRequest, PromptResponse
from app.core.config import OPENAI_API_KEY
from app.docs.langchain_docs import langchain_docs
from app.utils.extract_web_content import extract_web_content
from app.utils.url_processing import process_urls, process_urls_and_generate_embeddings
from app.utils.background_tasks import process_urls_background

from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

router = APIRouter()

system_message = """あなたは超知能を持つAIアシスタントとして、ユーザーに親身に寄り添って回答します。
回答することによってユーザーから「ありがとう」と言われることがゴールです。常にそれを目指してください。
"""

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_message),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

conversation = ConversationChain(
    memory=ConversationBufferMemory(return_messages=True),
    prompt=prompt,
    llm=ChatOpenAI(temperature=0.3, model_name='gpt-4')
    )


# vector stores for embedding
text_splitter = CharacterTextSplitter(separator=" ", chunk_size=500, chunk_overlap=0)

extracted_texts = process_urls(langchain_docs)
split_texts = []
for text in extracted_texts:
    split_texts.extend(text_splitter.split_text(text))
embeddings = OpenAIEmbeddings()

# 非同期にURLを処理し、embeddingsとsplit_textsを生成するタスクを追加
BackgroundTasks().add_task(process_urls_background, langchain_docs, callback=process_urls_and_generate_embeddings)

@router.post('/gpt4')
async def gpt_endpoint(user_message: str):
    docsearch = Chroma.from_texts(split_texts, embeddings)
    docs = docsearch.similarity_search(user_message, k=2)
    reference = [doc.page_content for doc in docs]
    print(f"reference: {reference}, len:{len(reference)}")
    input = """ユーザーからの会話に答えてください。また会話に関係のあるかもしれない参考情報も渡します。必要に応じて参考情報を利用して回答してください。
    ユーザーからの会話：{user_message}

    参考情報：{reference}
    """.format(user_message=user_message, reference=reference)
    
    res = conversation.predict(input=input)
    
    return {'status': 'ok', 'response': res }