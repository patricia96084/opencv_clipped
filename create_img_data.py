import cv2
import numpy as np
import matplotlib.pyplot as plt
from os.path import splitext
from PIL import Image, ImageDraw, ImageFont

def auto_fill(list_of_positions: list, image: np.ndarray, size: int, list_of_text: list):
    result_image= image.copy()
    for index, positions in enumerate(list_of_positions):
        result_image = fill_text(positions, result_image, size, list_of_text[index])
    return result_image

def first_auto_fill(list_of_positions: list, image: np.ndarray, size: int, list_of_text: list):
    result_image = image.copy()
    proper_size = test_text_size(list_of_positions[0], result_image, size, list_of_text[0])
    return auto_fill(list_of_positions, result_image, proper_size, list_of_text), proper_size

def test_text_size(positions: list, image: np.ndarray, size: int, text: str):
    result_image = fill_text(positions, image, size, text)
    rgb_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
    pillow_image = Image.fromarray(rgb_image)
    pillow_image.show()
    control_size = input('if the text size is fine, input "Y", otherwise, input another text size')
    if control_size == 'Y':
        return size
    else:
        print(int(control_size))
        return test_text_size(positions, image, int(control_size), text)

def fill_text(positions: list, image: np.ndarray, size: int, text: str) -> np.ndarray:
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pillow_image = Image.fromarray(rgb_image)
    limit = positions[1][0] - positions[0][0]
    draw = ImageDraw.Draw(pillow_image)
    font = ImageFont.truetype('kaiu.ttf', size=size)
    font_height = font.getsize('國')[0]

    cliped_text = clip_words(text, font, limit)
    for line_count, sentence in enumerate(cliped_text):
        text_position = (positions[0][0], positions[0][1] + line_count*font_height)
        draw.text(text_position, sentence, fill=(40, 40, 40), font=font)
    rgb_image = np.asarray(pillow_image)
    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    return bgr_image


def clip_words(text: str, font: ImageFont, limit: int):
    width, height = font.getsize(text)
    result = []
    if limit >= width:
        result.append(text)
    else:
        width_per_word = font.getsize('你好')[0] - font.getsize('你')[0]
        word_per_line = limit // width_per_word
        word_count = 1
        line_count = 0
        result.append('')
        for char in text:
            if word_count > word_per_line:
                line_count += 1
                result.append(char)
                word_count = 1
            else:
                result[line_count] = result[line_count] + char
                word_count += 1
    return result

'''
position should be like: [upper_left_of_the_rectangle, bottom_right_of_the_retangle]
'''
##### not for chinese or any other non-ASCII
# def filled_text(list_of_positions: list, image: np.ndarray):
#     result_image = image.copy()
#     for positions in list_of_positions:
#         upper_left = positions[0]
#         bottom_right = positions[1]
#         bottom_left = (upper_left[0], bottom_right[1])
#         fill_with = input()
#         result_image = cv2.putText(result_image,
#                                    fill_with,
#                                    bottom_left, 
#                                    cv2.FONT_HERSHEY_SIMPLEX,
#                                    1,
#                                    (200, 200, 200),
#                                    2,
#                                    cv2.LINE_AA)
#     return result_image

def display_image(image: np.ndarray, gray=False):
    cmap = cmap_value(gray)
    plt.imshow(image,cmap=cmap)
    plt.show()

'''
list of images should be list of np.ndarry, which is output type of cv2.imread
subplot_structure 23 stands for 2 x 3
'''
def display_images(list_of_images: list, subplot_structure: int, gray=False):
    cmap = cmap_value(gray)
    plt.figure()
    for index, image in enumerate(list_of_images):
        plt.subplot(subplot_structure*10+index+1)
        plt.imshow(image, cmap)
    plt.show()

def cmap_value(gray: bool) -> str:
    if gray:
        cmap = 'gray'
    else:
        cmap = 'viridis'
    return cmap

def read_image(image_path: str) -> np.ndarray:
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_ANYCOLOR)
    return image

def save_image(image:np.ndarray, image_path: str) -> None:
    path_and_name, image_type = splitext(image_path)
    is_success, encode_image = cv2.imencode(image_type, image)
    if is_success:
        encode_image.tofile(image_path)
    else:
        raise IOError
