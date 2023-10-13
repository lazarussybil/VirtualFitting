import requests
import numpy as np
import base64
from PIL import Image
import cv2
from skimage import data,filters
''' url method'''
# response = requests.post(
#     'https://api.remove.bg/v1.0/removebg',
#     data={
#         'image_url': 'https://www.remove.bg/example.jpg',   # the url of your target picture
#         'size': 'auto'
#     },
#     headers={'X-Api-Key': 'temzvkbZEcX1PmXoRmiB6bCk'},
# )
# if response.status_code == requests.codes.ok:
#     with open('no-bg.png', 'wb') as out:
#         out.write(response.content)
# else:
#     print("Error:", response.status_code, response.text)

def convt_img2mask(img_path):
    L_image=Image.open(img_path)

    out = L_image.convert("RGB")
    img_arr = np.array(out)

    img_size = list(img_arr.shape)

    for i in range(img_size[0]):
        for j in range(img_size[1]):
            if img_arr[i][j][0] == 255 and img_arr[i][j][1] == 255 and img_arr[i][j][2] == 255:
                img_arr[i][j][0] = 0
                img_arr[i][j][1] = 0
                img_arr[i][j][2] = 0
            else:
                img_arr[i][j][0] = 255
                img_arr[i][j][1] = 255
                img_arr[i][j][2] = 255

    mask = Image.fromarray(img_arr)
    return out, mask


''' local file method '''

import requests
def remove_inference(image_path):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(image_path, 'rb')},      # the position of your target picture
        data={'size': 'auto', 'bg_color':'white'},
        headers={'X-Api-Key': 'temzvkbZEcX1PmXoRmiB6bCk'},
    )
    if response.status_code == requests.codes.ok:
        with open('no-bg.png', 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)
    result, mask = convt_img2mask('no-bg.png')
    return result, mask


def remove_inference_opencv(image_path, morph_size = 10, algo='MOG2'):
    img = cv2.imread(image_path)
    
    # TODO: Add HSI option
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # otsu阈值
    (t,thresh) = cv2.threshold(gray_img,0,255,cv2.THRESH_TOZERO_INV+cv2.THRESH_OTSU)

    # 腐蚀优化
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(morph_size,morph_size))
    thresh = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel)

    # 颜色空间转换：BGR转RGB
    ret, mask = cv2.threshold(thresh, 1, 255, cv2.THRESH_BINARY)
    mask_invert = cv2.bitwise_not(mask)

    result = cv2.add(img, np.zeros(np.shape(img), dtype=img.dtype), mask=mask)
    result = cv2.cvtColor(result,cv2.COLOR_BGR2RGB)
    result = np.array(result)
    for y in range(result.shape[0]):
        for x in range(result.shape[1]):
            if mask_invert[y][x] != 0:
                result[y, x, :] = [255, 255, 255]
    return result, mask

def main():
    remove_inference_opencv("./Database/val/cloth/002337_1.jpg")

if  __name__ == '__main__':
    main()