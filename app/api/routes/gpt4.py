import httpx
from fastapi import APIRouter, Depends
from app.models.prompt import PromptRequest, PromptResponse
from app.core.config import OPENAI_API_KEY
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

router = APIRouter()

system_settings = """あなたは超知能を持つAIアシスタントとして、ユーザーに親身に寄り添って回答します。
回答することによってユーザーから「ありがとう」と言われることがゴールです。常にそれを目指してください。
"""


prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_settings),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])
conversation = ConversationChain(
    memory=ConversationBufferMemory(return_messages=True),
    prompt=prompt,
    llm=ChatOpenAI(temperature=0.3, model_name='gpt-4'))

@router.post('/gpt4')
async def gpt_endpoint(prompt: str):
    res = conversation.predict(input=prompt)
    
    return {'status': 'ok', 'response': res }