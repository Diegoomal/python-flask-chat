from PyPDF2 import PdfReader                                                    # type: ignore

def pypdf2_get_text_from_pdf(file_path: str):
    reader = PdfReader( file_path )
    document = ''.join(page.extract_text() for page in reader.pages)
    return document


import pdfplumber                                                               # type: ignore

def pdfplumber_get_text_from_pdf(file_path: str):
    with pdfplumber.open(file_path) as pdf:
        documents = ''.join([page.extract_text() for page in pdf.pages])
    return documents


from pdf2image import convert_from_path                                         # type: ignore

def pdf2img_get_image_from_pdf(file_path: str):
    images = convert_from_path(file_path)
    return images


import cv2                                                                      # type: ignore
import numpy as np                                                              # type: ignore
from PIL import ImageEnhance, ImageOps, Image                                   # type: ignore

def enhance_contrast(image, level=5.0):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(level)

def binarize_image(image, threshold=128):
    gray_image = image.convert('L')
    return gray_image.point(lambda x: 0 if x < threshold else 255, '1')

def dilate_image(image, kernel_size=(2, 2), iterations=1):
    open_cv_image = np.array(image).astype(np.uint8)
    kernel = np.ones(kernel_size, np.uint8)
    dilated_image = cv2.dilate(open_cv_image, kernel, iterations=iterations)
    return Image.fromarray(dilated_image)

# def process_image(image):
#     enhanced_image = enhance_contrast(image)
#     binarized_image = binarize_image(enhanced_image)
#     final_image = dilate_image(binarized_image)
#     return final_image

def process_image(images):
    processed_images = []
    for image in images:
        img = enhance_contrast(image)
        img = binarize_image(img)
        # img = dilate_image(img)
        processed_images.append(img)
    return processed_images


import pytesseract # type: ignore

def extract_text_with_OCR(image):
    return pytesseract.image_to_string(image)


import base64
from io import BytesIO

def get_imgs_b64(images, filter_data: bool = True):

    images_base64 = []
    for image in images:
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        images_base64.append(img_str)

    if(filter_data):
        images_base64 = [
            str(file).replace('data:image/jpeg;base64,', '') 
            for file in images_base64
        ]

    return images_base64


from IPython.display import display, Image                                      # type: ignore

def show_image(image_base64):
    display( Image(data=base64.b64decode( image_base64 ), format='png') )


from llm import ILLM, Ollama, LLMBuilder                                        # type: ignore

def get_ollama_instance(model_name: str = 'phi3:instruct', temperature: float = 0) -> Ollama:
    illm: ILLM = LLMBuilder( llm_type='ollama', model_name=model_name, temperature=temperature )
    ollm: Ollama = illm.get_instance()
    return ollm

def get_llm_vision_models():
    vision_models = [ 'llava', 'phi3:instruct', 'bakllava', 'llava-llama3', 'moondream' ]
    return vision_models

def get_llm_models():
    models = [ 'llama3', 'llama3.2:1b', 'phi3:mini-128k' ]
    return models
