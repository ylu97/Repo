import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor


class Character(BaseModel):
    name: str
    fact: List[str] = Field(..., description="A list of facts about the subject")


client = Groq(
    api_key=os.environ.get('GROQ_API_KEY'),
)

client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

resp = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[
        {
            "role": "user",
            "content": "Tell me about the company Google",
        }
    ],
    response_model=Character,
)
print(resp.model_dump_json(indent=2))
"""
{
  "name": "Tesla",
  "fact": [
    "electric vehicle manufacturer",
    "solar panel producer",
    "based in Palo Alto, California",
    "founded in 2003 by Elon Musk"
  ]
}
"""
