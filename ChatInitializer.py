from yapper import Yapper, PiperSpeaker, PiperVoiceUK, PiperVoiceUS

def initialize_speech_to_text_voice():
    voices: list[PiperVoiceUK | PiperVoiceUS] = [*PiperVoiceUK, *PiperVoiceUS]

    for (index, voice) in enumerate(voices):
        print((index + 1), voice)
    voice_number = int(input("Input a number to select Piper voice: "))

    return Yapper(
        speaker = PiperSpeaker(
            voice = voices[voice_number - 1]
        )
    )

def initialize_llm_model():
    return str(input("Input LLM model name: "))

class ChatInitializer:
    def __init__(self):
        self.yapper = initialize_speech_to_text_voice()
        self.model = initialize_llm_model()

    def get_yapper(self):
        return self.yapper

    def get_model(self):
        return self.model
