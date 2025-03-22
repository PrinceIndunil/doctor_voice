import os
import platform
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
import pygame  # For MP3 playback

# Get ElevenLabs API Key
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Function to play MP3 audio
def play_mp3(output_filepath):
    if not os.path.exists(output_filepath):
        print(f"Error: File {output_filepath} not found.")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(output_filepath)
        pygame.mixer.music.play()
        
        # Wait for the audio to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Function for gTTS (Google Text-to-Speech)
def text_to_speech_with_gtts(input_text, output_filepath, autoplay=False):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)
    
    if autoplay:
        play_mp3(output_filepath)

# Function for ElevenLabs TTS
def text_to_speech_with_elevenlabs(input_text, output_filepath, autoplay=False):
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY is not set in the environment variables.")

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    # Use MP3 format (Free-tier friendly)
    audio_generator = client.generate(
        text=input_text,
        voice="Roger",
        output_format="mp3_44100_32",  # Supported MP3 format
        model="eleven_turbo_v2"
    )
    
    # Save the MP3 file correctly
    with open(output_filepath, "wb") as f:
        for chunk in audio_generator:
            f.write(chunk)

    if autoplay:
        play_mp3(output_filepath)

# Example usage
#input_text = "Hi, I'm Doctor AI with autoplay"
#text_to_speech_with_gtts(input_text, output_filepath="gtts_testing.mp3", autoplay=True)

#input_text = "Hi, I'm Doctor AI using ElevenLabs with autoplay"
#text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing.mp3", autoplay=True)
