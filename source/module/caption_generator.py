from openai import OpenAI

def get_caption(base64_image, client):
    """
    Generate a caption for the given base64 encoded image using OpenAI GPT.
    """
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
