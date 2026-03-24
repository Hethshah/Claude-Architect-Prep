from dotenv import load_dotenv
load_dotenv(override=True)

from anthropic import Anthropic


client = Anthropic()
model = "claude-sonnet-4-0"


def chat(messages, system=None, stop_sequences=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages
    }

    if system:
        params["system"] = system

    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    message = client.messages.create(**params)
    return message.content[0].text


def add_user_message(message, text):
    user_message = {"role": "user", "content": text}
    message.append(user_message)

def add_assistant_message(message, text):
    assistant_message = {"role": "assistant", "content": text}
    message.append(assistant_message)


messages = []

prompt = """
Generate three sample AWS CLI commands. Each should be very short
"""
add_user_message(messages, prompt)
add_assistant_message(messages, "Here are all three command in single block\n ```bash")

text = chat(messages, stop_sequences=["```"])
# text = chat(messages)
print(text)
