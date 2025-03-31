from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
import base64
import os
from openai import OpenAI
from flask_cors import CORS
load_dotenv(override=True)

app = Flask(__name__)
CORS(app)
temp_file = '/workspace/competitions/Sly/Image2Speech/temp/temp.mp3'

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_caption(base64_image):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Mô tả chi tiết bức ảnh (khoảng 100 từ)?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            ],
        }],
    )
    return response.choices[0].message.content

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
