from flask import Flask, request, jsonify
from flask_cors import CORS
from source.module.image_caption import get_caption
from source.module.text_to_speech import caption2speech, convert_audio_to_base64
from source.config.config import get_openai_client

app = Flask(__name__)
CORS(app)

@app.route('/image2speech', methods=['POST'])
def run():
    data = request.get_json()  
    client = get_openai_client()
    img_data = data.get('image')
    if not img_data:
        return jsonify({"error": "No image data provided"}), 400
    
    caption = get_caption(img_data)
    
    try:
        caption2speech(caption, client)
        audio_base64 = convert_audio_to_base64()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "caption": caption,
        "audio": audio_base64
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9190, debug=True)
