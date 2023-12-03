from io import BytesIO

import qrcode
from PIL import Image


def generate_qr_code_for_link(data: str, name_of_file: str, size=768):
    qr = qrcode.QRCode(version=4, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image = qr_image.resize((size, size))
    
    image_buffer = BytesIO()
    qr_image.save(image_buffer, "PNG")
    image_buffer.seek(0)
    image = Image.open(image_buffer)
    image.save(name_of_file)
    #return image_buffer