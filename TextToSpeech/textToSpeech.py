from gtts import gTTS
import os

def text_to_speech_from_file(file_path, filename='textToSpeech.mp3'):
    with open(file_path, 'r') as file:
        text = file.read()
    tts = gTTS(text=text, lang='en')  # 'en' for English
    tts.save(filename)
    os.system(f'start {filename}')  # Opens the audio file with the default audio player

file_path = "../SignToText/output.txt" 
text_to_speech_from_file(file_path)
