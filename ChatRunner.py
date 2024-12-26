import ollama

ollama.ps()

def chat_loop():
    messages = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        stream = ollama.chat(
            model="mistral",
            messages=messages,
            stream=True,
        )
        response_string = ""
        for chunk in stream:
            print(chunk["message"]["content"], end="", flush=True)
            response_string += chunk.message.content
        print()

        messages.append({"role": "assistant", "content": response_string})

if __name__ == "__main__":
    chat_loop()
