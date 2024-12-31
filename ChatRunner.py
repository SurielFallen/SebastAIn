import ollama
import pyttsx3
from gtts import gTTS
from io import BytesIO
from yapper import Yapper, PiperSpeaker, PiperVoiceUK, PiperQuality

Marah = PiperSpeaker(
    voice=PiperVoiceUK.ALBA
)
yapper = Yapper(speaker=Marah)

def chat_loop():
    messages = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        stream = ollama.chat(
            model="marah",
            messages=messages,
            stream=True,
        )
        response_string = ""
        for chunk in stream:
            print(chunk["message"]["content"], end="", flush=True)
            response_string += chunk.message.content
        print()
        yapper.yap(response_string, plain=True)
        messages.append({"role": "assistant", "content": response_string})

if __name__ == "__main__":
    chat_loop()
