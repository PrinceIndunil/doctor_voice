import os
import gradio as gr

from doctor_brain import encode_image, analyze_image_with_query
from patient_voice import record_audio_simple, transcribe_with_groq
from doctor_voice import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

# Fixed grammar in system_prompt
system_prompt = """You have to act as a professional doctor. I know you are not, but this is for learning purposes. 
What's in this image? Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in your response. 
Your response should be in one long paragraph. Also, always answer as if you are speaking to a real person. 
Do not say 'In the image I see' but instead say 'With what I see, I think you have ....' 
Do not respond as an AI model. Your answer should mimic that of an actual doctor, not an AI bot. 
Keep your answer concise (max 2 sentences). No preamble; start your answer right away, please."""

def process_inputs(audio_file_path, image_filepath):
    # Ensure API key exists
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        return "Error: Missing GROQ API Key", "", ""

    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=groq_api_key,
        audio_file_path=audio_file_path,
        stt_model="whisper-large-v3"
    )

    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + " " + speech_to_text_output,  # Space added for separation
            encoded_image=encode_image(image_filepath),
            model="llama-3.2-90b-vision-preview"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    # Ensure consistent file naming
    output_audio_path = "final.mp3"
    voice_of_doctor = text_to_speech_with_elevenlabs(doctor_response, output_audio_path)

    return speech_to_text_output, doctor_response, voice_of_doctor

iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("final.mp3")  # Use correct file name
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)
