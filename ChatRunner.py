import ollama
from ChatInitializer import ChatInitializer
import subprocess
import speech_recognition as sr

#start ollama server and wait
subprocess.Popen(["ollama", "serve"]).wait(300)

messages = []
chat_initializer = ChatInitializer()
r = sr.Recognizer()

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


def get_user_input():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        print("Done listening")

        try:
            user_input = r.recognize_whisper(audio, language="english")
            print("Whisper thinks you said " + user_input)
        except sr.UnknownValueError:
            print("Whisper could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Whisper; {e}")
    return user_input


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
