from dotenv import load_dotenv
load_dotenv(override=True)

from anthropic import Anthropic


client = Anthropic()
model = "claude-sonnet-4-0"


def chat(messages):
    response  = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages
    )
    return response.content[0].text



def add_user_message(message, text):
    user_message = {"role": "user", "content": text}
    message.append(user_message)

def add_assistant_message(message, text):
    assistant_message = {"role": "assistant", "content": text}
    message.append(assistant_message)

chat_message = []

while True:
    inp = input("> ")
    add_user_message(chat_message, inp)
    assistant_reply = chat(chat_message)
    print("*"*120)
    print(assistant_reply)
    print("*"*120)
    add_assistant_message(chat_message, assistant_reply)




