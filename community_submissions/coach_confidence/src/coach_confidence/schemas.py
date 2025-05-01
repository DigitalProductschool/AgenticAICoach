from pydantic import BaseModel

class TextInput(BaseModel):
    user_text: str
