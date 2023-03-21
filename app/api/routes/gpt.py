import httpx
from fastapi import APIRouter, Depends
from app.models.prompt import PromptRequest, PromptResponse
from app.core.config import OPENAI_API_KEY, GOOGLE_API_KEY, GOOGLE_CSE_ID
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import initialize_agent

router = APIRouter()

search = GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID)
tools = [
    Tool(
        name = 'Search',
        func=search.run,
        description='useful for when you need to answer questions about current events'
    )
]
memory = ConversationBufferMemory(memory_key='chat_history')
llm=OpenAI(model_name='gpt-4', max_tokens=6000)
agent_chain = initialize_agent(tools, llm, agent='chat-zero-shot-react-description', verbose=True, memory=memory)


@router.post('/gpt')
async def gpt_endpoint(prompt: str):
    res = agent_chain.run(input=prompt)
    return {'generated_text': res}

# healthcheck api
@router.get('/healthcheck')
def healthcheck():
    return {'status': 'ok'}