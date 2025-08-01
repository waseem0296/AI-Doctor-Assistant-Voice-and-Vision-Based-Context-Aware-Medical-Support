#ffmpeg,portAudio
import logging
from dotenv import load_dotenv
from pydub import AudioSegment
import os
import speech_recognition as sr
from io import BytesIO

load_dotenv()
logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")
file_path="testing_patient_voice.mp3"
def voice_recorder(file_path,timeout=20,phrase_time_limit=None):
    recognizer=sr.Recognizer()
    try:    
        with sr.Microphone() as source:
            logging.info("Adjusting for the Ambient noise..")
            recognizer.adjust_for_ambient_noise(source,duration=1)
            logging.info("Start speeking now...")
            user_audio=recognizer.listen(source,timeout=timeout,phrase_time_limit=phrase_time_limit)
            logging.info("Audio has been completed...")
            wav_data=user_audio.get_wav_data()
            audio_segment=AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path,format="mp3",bitrate="128k")
            logging.info(f"Audio saved successfully to {file_path}")
    except Exception as e:
        logging.error(f"An arror occurred :{e}")
        
# voice_recorder(file_path)       
# Transcription of voice by groq from speech to speech
from groq import Groq
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
def transcription_from_voice_text(file_path):
    client=Groq(api_key=GROQ_API_KEY)
    audio_file=open(file_path, "rb")
    transcription=client.audio.transcriptions.create(
        model='whisper-large-v3',
        file=audio_file,
        language='en'
    )

    return transcription.text