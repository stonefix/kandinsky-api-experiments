import json
import time
from io import BytesIO
from os import environ

import qrcode
import requests
from dotenv import load_dotenv
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import ImageColorMask

from utils import (create_circle_qr_code_for_input, generate_qr_code_for_str,
                   save_base64_to_buffer, save_base64_to_file)

# https://fusionbrain.ai/docs/ru/doc/api-dokumentaciya/

class Request:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
                'model_id': (None, model),
                'params': (None, json.dumps(params), 'application/json')
            }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data

    def check_generation(self, request_id, attempts=10, delay=10):
        """
            Результат возращается в формате Base64
        """
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


if __name__ == '__main__':
    load_dotenv()
    url = environ.get('URL')
    api_key = environ.get('API_KEY')
    secret_key = environ.get('SECRET_KEY')

    TEXT = 'Dark Side Stop For Stop all this'
    RESULT_KANDINSKY = 'result_kandinsky.png'
    RESULT_KANDINSKY_BUFFER = BytesIO()

    request = Request(url, api_key, secret_key)
    model_id = request.get_model()['id']; 
    uuid = request.generate(TEXT, model_id)['uuid'];
    images = request.check_generation(uuid);
    
    RESULT_KANDINSKY_BUFFER = save_base64_to_buffer(images[0])
    if not hasattr(Image, 'Resampling'):
        Image.Resampling = Image
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(TEXT)
    qr.make(fit=True)

    # накладываем qr-код
    qr_img = qr.make_image(image_factory=StyledPilImage, color_mask=ImageColorMask(color_mask_path=RESULT_KANDINSKY_BUFFER))
    qr_img.save('my-colormask-qrcode-999.png')