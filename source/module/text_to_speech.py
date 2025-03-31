import os
from openai import OpenAI
import base64

temp_file = '/workspace/competitions/Sly/Image2Speech/sample/sample_audio.mp3'

def caption2speech(caption, client):
    """
    Convert text caption to speech and save as an audio file.
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=caption,
    )
    response.stream_to_file(temp_file)

def convert_audio_to_base64():
    """
    Convert audio file to base64.
    """
    try:
        with open(temp_file, "rb") as f:
            audio_data = f.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        return audio_base64
    except Exception as e:
        raise Exception(f"Failed to process audio file: {str(e)}")
