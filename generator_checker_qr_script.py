import glob
import os
import shutil
import sys

import cv2
import pandas as pd
import qrcode
import zxing
from PIL import Image
from pyzbar import pyzbar
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import ImageColorMask


def read_qr_code_with_cv2(file):
    try:
        detector = cv2.QRCodeDetector()
        img = cv2.imread(file)
        value = detector.detectAndDecode(img)[0]
        return value
    except:
        return

def read_qr_code_with_pyzbar(file):
    try:
        img = cv2.imread(file)
        value = pyzbar.decode(img)[0].data.decode()
        return value 
    except:
        return

def read_qr_code_with_zxing(file):
    try:
        detector = zxing.BarCodeReader()
        value = detector.decode(file).parsed
        return value
    except:
        return


dataset_df = pd.read_csv('dataset.csv');


FILE_NAME = 'unique-name-for-dataset'

BASE_FILE_NAME = 'QR'

for index, row in dataset_df.iterrows():
    data_value = row.iloc[0]
    if len(data_value) < 4000:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data_value)
        unique_name = f'{BASE_FILE_NAME}-{index}.png'
        try:
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save(f'dataset-qr/{unique_name}')
        except:
            continue



'''
result_text_cv = read_qr_code_with_cv2(FILE_NAME)
result_text_pyzbar = read_qr_code_with_pyzbar(FILE_NAME)
result_text_zxing = read_qr_code_with_zxing(FILE_NAME)

if (result_text_cv and result_text_pyzbar and result_text_zxing):
    print('ITs OKAY!!!')
'''


'''
if not hasattr(Image, 'Resampling'):
  Image.Resampling = Image
'''




'''
for file in glob.glob('./images/*.png'):
    cv2_code = read_qr_code_with_cv2(file)
    cv2_result = (cv2_code == text)
    cv2_color = PASS if cv2_result else FAIL

    pyzbar_code = read_qr_code_with_pyzbar(file)
    pyzbar_result = (pyzbar_code == text)
    pyzbar_color = PASS if pyzbar_result else FAIL

    zxing_code = read_qr_code_with_zxing(file)
    zxing_result = (zxing_code == text)
    zxing_color = PASS if zxing_result else FAIL

    print(f'[{cv2_color}cv2{RESET} {pyzbar_color}pyzbar{RESET} {zxing_color}zxing{RESET}] {file}')

    if (cv2_result and pyzbar_result and zxing_result):
        shutil.copy2(file, file.replace('/images/', '/valid/'))
'''