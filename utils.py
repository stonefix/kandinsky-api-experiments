import base64
from io import BytesIO

import qrcode
from PIL import Image, ImageDraw
from qrcode.compat.pil import Image as pil_Image
from qrcode.image.pil import PilImage
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles import colormasks
from qrcode.image.styles.colormasks import ImageColorMask
from qrcode.image.styles.moduledrawers import (RoundedModuleDrawer,
                                               SquareModuleDrawer)


def save_base64_to_file(base64_string: str, file: str):
    binary_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(binary_data))
    image.save(file)

def save_base64_to_buffer(base64_string: str) -> BytesIO:
    binary_data = base64.b64decode(base64_string)
    image_buffer = BytesIO(binary_data)
    return image_buffer

def generate_qr_code_for_str(data: str) -> BytesIO:
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True) # qrcode.image.pil.PilImage
    qr_image = qr.make_image(fill_color="black", back_color="white") # qrcode.image.pil.PilImage
    print(type(qr_image))
    image_buffer = BytesIO()
    qr_image.save(image_buffer, "PNG")
    image_buffer.seek(0)
    return image_buffer

def create_circle_qr_code_for_input(qr_img):
    qr_img_copy = qr_img.copy()
    draw = ImageDraw.Draw(qr_img_copy)
    draw.ellipse(
        (30, 30, qr_img_copy.size[1]-30, qr_img_copy.size[1]-30),
        fill = None,
        outline ='black',
        width=30
    )
    width, height = qr_img_copy.size
    left = 0
    top = height // 3
    right = width
    bottom = 2 * height//3
    cropped_section = qr_img_copy.crop((left, top, right, bottom))
    rotated_crop = cropped_section.copy()
    rotated_crop = rotated_crop.rotate(90, expand=True)
    qr_img_copy.paste(cropped_section, (0, -cropped_section.size[1]//2 + 20 ))
    qr_img_copy.paste(cropped_section, (0, qr_img_copy.size[1] - cropped_section.size[1]//2 -20 ))
    qr_img_copy.paste(rotated_crop, (-rotated_crop.size[0]//2 + 20, 0))
    qr_img_copy.paste(rotated_crop, (qr_img_copy.size[0] - rotated_crop.size[0]//2 - 20, 0))
    raw = ImageDraw.Draw(qr_img_copy)
    '''
    draw.ellipse(
        (30, 30, qr_img_copy.size[1]-30, qr_img_copy.size[1]-30),
        fill = None,
        outline ='black',
        width=30
    )
    '''
    '''
    draw.ellipse(
        (-rotated_crop.size[0],
        -cropped_section.size[1],
        qr_img_copy.size[1] + rotated_crop.size[0],
        qr_img_copy.size[1] + cropped_section.size[1]
        ),
        fill = None,
        outline ='white',
        width=340
    )
    '''
    qr_img_copy.save('test777.png')





#if not hasattr(Image, 'Resampling'):
#  Image.Resampling = Image

#qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=6)
#qr.add_data('https://s00.yaplakal.com/pics/pics_preview/3/2/8/17751823.jpg')
#qr_img = qr.make_image(image_factory=StyledPilImage, color_mask=ImageColorMask(color_mask_path='result.png'))
#qr_img = qr.make_image(fill_color="black", back_color="white")
#qr_img.save('image2.png')

#qr_img.save('my-colormask-qrcode.png')
