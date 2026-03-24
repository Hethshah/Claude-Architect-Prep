from dotenv import load_dotenv
load_dotenv(override=True)

from anthropic import Anthropic


client = Anthropic()
model = "claude-sonnet-4-0"


def chat(messages, system=None):

    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages
    }

    if system:
        params["system"] = system
    
    response = client.messages.create(**params)
    return response.content[0].text

messages = [{"role":"user", "content": "Write me a python code for finding duplicate entry in string"}]
# messages = ["Write me a python code for finding duplicate entry in string"]

system = """
you are python engineer who Write a consie code single best solution only 
"""
print(chat(messages, system=system))
