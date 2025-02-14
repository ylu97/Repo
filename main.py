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

while True:
    user_input = input("Please enter a subject that you want to search (or type 'Quit' to exit): ")
    if user_input.strip().lower() == "quit":
        print("Exiting now...")
        break
    
    resp = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        response_model=Character,
    )
    print(resp.model_dump_json(indent=2))
