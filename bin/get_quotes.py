#!/usr/bin/env python3
import sys
import os
from openai import OpenAI

source_file = sys.argv[1]


if os.path.exists(source_file):
    with open(source_file, 'r') as file:
        content = file.read() + "\n"

OpenAI.api_key = os.environ["OPENAI_API_KEY"]

#client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
client = OpenAI()

completion = client.chat.completions.create(
#  model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf", 
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "Based on the user input generate a Yaml file with a key called summary and a key called quotes. The value of the summary key must be an essential of what the text is about (maximum 200 chars long) without mentioning people names or introduction like 'the text is about...' just write what's about. The value of the quotes key must be an array of 4 different quotes extracted from the text. Quotes should be about the most interesting and inspiring parts, must reflect the original text as much as possible, but you can remove unnecessary words or parts of the text. Each quote should be a string of maximum 140 characters."},
    {"role": "user", "content": content}
  ],
  temperature=0.7,
)

print(completion.choices[0].message.content)