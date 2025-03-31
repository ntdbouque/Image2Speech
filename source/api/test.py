from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


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


image_path = '/workspace/competitions/Sly/Image2Speech/images/image.png'
caption = get_caption(encode_image(image_path))
print('Caption:', caption)