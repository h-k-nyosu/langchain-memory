from pydantic import BaseModel

class PromptRequest(BaseModel):
    text: str
    max_tokens: int = 100

class PromptResponse(BaseModel):
    generated_text: str
