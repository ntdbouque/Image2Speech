from dotenv import load_dotenv
from flask import Flask, request, jsonify
import base64
import os
from openai import OpenAI
from flask_cors import CORS
from transformers import pipeline
from PIL import Image
import io

load_dotenv(override=True)

app = Flask(__name__)
CORS(app)
temp_file = '/workspace/competitions/Sly/Image2Speech/sample/sample_audio.mp3'

os.environ["HF_HOME"] = "hf_model"
pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")

def get_caption(base64_image):
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))
    
    result = pipe(image, max_new_tokens=100, return_full_text=False)
    return result[0]['generated_text']

def caption2speech(caption):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=caption,
    )
    response.stream_to_file(temp_file)

@app.route('/image2speech', methods=['POST'])
def run():
    data = request.get_json()  
    img_data = data.get('image')
    if not img_data:
        return jsonify({"error": "No image data provided"}), 400
    
    caption = get_caption(img_data)
    
    caption2speech(caption)
    
    try:
        with open(temp_file, "rb") as f:
            audio_data = f.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    except Exception as e:
        return jsonify({"error": "Failed to process audio file", "details": str(e)}), 500

    return jsonify({
        "caption": caption,
        "audio": audio_base64
    })

if __name__ == '__main__':
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    app.run(host='0.0.0.0', port=9190, debug=True)