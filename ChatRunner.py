import ollama
from yapper import Yapper, PiperSpeaker, PiperVoiceUK

messages = []

def chat_loop():
    yapper = initialize_speech_to_text()
    while True:
        user_input=get_user_input()
        if user_input.lower() == "exit":
            break
        append_messages("user", user_input)

        response_string = chat()
        print()
        yapper.yap(response_string, plain=True)
        append_messages("assistant", response_string)


def initialize_speech_to_text():
    return Yapper(
        speaker = PiperSpeaker(
            voice = PiperVoiceUK.ALBA
        )
    )

def get_user_input():
    return input("You: ")

def chat():
    stream = ollama.chat(
        model="marah",
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
