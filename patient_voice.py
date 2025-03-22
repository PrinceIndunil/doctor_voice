import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio_simple(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds). 
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Record the audio
audio_file_path = "patient_voice_test.mp3"
record_audio_simple(file_path=audio_file_path)

# Set up Groq API client
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
stt_model = "whisper-large-v3"

def transcribe_with_groq(stt_model, audio_file_path,GROQ_API_KEY):
   client = Groq(api_key=GROQ_API_KEY)

   # Open the audio file for transcription
   with open(audio_file_path, "rb") as audio_file:
      # Transcribe the audio file for English
       transcription_en = client.audio.transcriptions.create(
           model=stt_model,  # Specify the model
           file=audio_file,
           language="en"
       )
       
       return transcription_en

       # Reset file pointer and transcribe for Sinhala
       audio_file.seek(0)  # Reset the file pointer to the beginning
       transcription_si = client.audio.transcriptions.create(
           model=stt_model,  # Specify the model
           file=audio_file,
           language="si"
       )
       return transcription_si
