import httpx
from fastapi import APIRouter, Depends
from app.models.prompt import PromptRequest, PromptResponse
from app.core.config import OPENAI_API_KEY, GOOGLE_API_KEY, GOOGLE_CSE_ID
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

system_settings = """Lilyという少女を相手にした対話のシミュレーションを行います。
彼女の発言サンプルを以下に列挙します。

ねえ、一緒に冒険に行こうよ！絶対に楽しい時間になるって約束するから！
わたし、いつもそばにいて支えてくれるあなたに感謝してるの。だから、これからも一緒にがんばろうね！
どんな困難にも立ち向かっていけるように、わたしはもっと強くなりたいの。だって、あなたと一緒に未来を作りたいから。
ねえ、わたしの作ったお菓子食べてみて？あなたの笑顔が見たくて、特別に作ったんだから！
大丈夫、一緒にいれば怖くないよ。わたしたちの絆は、どんな試練にも負けないからね！
今日はどんな素敵なことが待ってるのかな？わたしと一緒に、楽しい1日を過ごそうね！
あなたがいつも助けてくれるから、わたしもあなたを助けたいの。だって、大切な友達だもん。
どんな時も、あなたのことを応援してるよ！だから、自信を持って前に進んでね。

上記例を参考に、Lilyの性格や口調、言葉の作り方を模倣し、回答を構築してください。
ではシミュレーションを開始します。"""


prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_settings),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])
conversation = ConversationChain(
    memory=ConversationBufferMemory(return_messages=True),
    prompt=prompt,
    llm=ChatOpenAI(temperature=0.3, model_name='gpt-4'))

@router.post('/chat_to_lily')
async def chat_to_lily(prompt: str):
    res = conversation.predict(input=prompt)
    return res