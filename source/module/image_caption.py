from transformers import pipeline
from PIL import Image
import io
import base64

pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")

def get_caption(base64_image):
    """
    Convert a base64 encoded image to a caption.
    """
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))
    
    result = pipe(image, max_new_tokens=100, return_full_text=False)
    return result[0]['generated_text']
