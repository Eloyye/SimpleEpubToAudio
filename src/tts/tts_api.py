from TTS.api import TTS
import torch

class TextToSpeechClient:
    def __init__(self, language='en', speaker='Ana Florence', output_file="../output/res.wav"):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        self.language = language
        self.speaker= speaker
        self.output_file = output_file
    def save(self, text : str):
        self.tts.tts_to_file(text, speaker=self.speaker, language=self.language, file_path=self.output_file)

    def set_output_file(self, new_of):
        self.output_file = new_of

    def get_output_file(self):
        return self.output_file

    def speak(self, text):
        self.tts.tts(text=text, speaker=self.speaker, language= self.language)