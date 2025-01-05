import ollama
from ChatInitializer import ChatInitializer
import subprocess

#start ollama server and wait
subprocess.Popen(["ollama", "serve"]).wait(300)

messages = []
chat_initializer = ChatInitializer()

def chat_loop():
    while True:
        user_input=get_user_input()
        if user_input.lower() == "exit":
            break
        append_messages("user", user_input)

        response_string = chat()
        print()
        chat_initializer.get_yapper().yap(response_string, plain=True)
        append_messages("assistant", response_string)

#speech input to be added
def get_user_input():
    return input("You: ")

def chat():
    stream = ollama.chat(
        model=chat_initializer.get_model(),
        messages=messages,
        stream=True,
    )
    response_string = ""
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)
        response_string += chunk.message.content
    return response_string

def append_messages(role,message):
    messages.append({"role": role, "content": message})

if __name__ == "__main__":
    chat_loop()
