import ollama
from ChatInitializer import ChatInitializer
import subprocess
import speech_recognition as sr
import time
from queue import Queue
from threading import Thread

#start ollama server and wait
#subprocess.Popen(["ollama", "serve"]).wait(300)

messages = []
chat_initializer = ChatInitializer()
r = sr.Recognizer()

def chat_loop():
    while True:
        user_input=get_user_input()
        if user_input.lower() == "exit":
            break
        append_messages("user", user_input)

        start_time = time.time()
        response_string = chat()
        end_time = time.time()

        latency = end_time - start_time
        print(f"Chat Latency: {latency} seconds")

        print()
        append_messages("assistant", response_string)


def get_user_input():
    # with sr.Microphone() as source:
    #     print("Say something!")
    #     audio = r.listen(source)
    #     print("Done listening")
    #
    #     try:
    #         user_input = r.recognize_whisper(audio, language="english")
    #         print("Whisper thinks you said " + user_input)
    #     except sr.UnknownValueError:
    #         print("Whisper could not understand audio")
    #     except sr.RequestError as e:
    #         print(f"Could not request results from Whisper; {e}")
    user_input = input("Ready for input :")
    return user_input


def chat():
    stream = ollama.chat(
        model=chat_initializer.get_model(),
        messages=messages,
        stream=True,
    )
    token_queue = Queue(maxsize=0)
    yapper = chat_initializer.get_yapper()
    response_string = ""

    Thread(target=speech_output, args=(yapper,token_queue)).start()
    Thread(target=process_stream_chunks, args=(stream,token_queue)).start()
    return response_string

def process_stream_chunks(stream,token_queue):
    while True:
        combined_chunk_string = ""
        chunk_start_time = time.time()
        for chunk in stream:
            chunk_string = chunk["message"]["content"]
            print(chunk_string, end="", flush=True)
            token_queue.put(chunk)
            combined_chunk_string += chunk_string
        chunk_end_time = time.time()
        latency = chunk_end_time - chunk_start_time
       # print(f"LLM Latency: {latency} seconds")

def speech_output(yapper,token_queue):
    while True:
        yapper_latency = 0
        start_time = time.time()
        yapper.yap(token_queue.get(), plain=True)
        end_time = time.time()
        yapper_latency += end_time - start_time

        #print(f"Yapper Latency: {yapper_latency} seconds")

def append_messages(role,message):
    messages.append({"role": role, "content": message})

if __name__ == "__main__":
    chat_loop()
