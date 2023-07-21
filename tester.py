import create_img_data
import cv2
from PIL import Image
import numpy as np
import create_content
import ast

def load_position(txt_path: str):
    with open(txt_path, 'r') as txt_file:
        positions_str = txt_file.read()
        list_of_positions = ast.literal_eval(positions_str)
        return list_of_positions

amount = 20
size =  25
save_to = 'sample/autocreate/'
auto_name = '1'
image = create_img_data.read_image('sample/1_whiteout.png')
list_of_positions = load_position('sample/1_positions.txt')
content = create_content.create_content(3, 6)
text = [
        content['name'], 
        content['gender'],
        content['id_card'],
        str(np.random.randint(0,120)),
        content['roc_year'],
        content['month'],
        content['day'],
        '',
        content['address'],
        create_content.get_random_year(),
        create_content.get_random_month(),
        create_content.get_random_day(),
        str(np.random.randint(0,10)),
        content['dept'],
        create_content.get_random_year(),
        create_content.get_random_month(),
        create_content.get_random_day(),
        content['doc_num'],
        content['disease'],
        content['advise']
]

print('-'*10+'creating first image'+'-'*10)
result_image, size = create_img_data.first_auto_fill(list_of_positions, image, size, text)
rgb_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
pillow_image = Image.fromarray(rgb_image)
pillow_image.show()
check = input('input "Y" if the first image seems fine: ')
if check == "Y":
    cv2.imwrite(save_to+auto_name+'_1.png', result_image)
    for i in range(2, amount+1):
        content = create_content.create_content(2, 6)
        text = [
                content['name'], 
                content['gender'],
                content['id_card'],
                str(np.random.randint(0,120)),
                content['roc_year'],
                content['month'],
                content['day'],
                '',
                content['address'],
                create_content.get_random_year(),
                create_content.get_random_month(),
                create_content.get_random_day(),
                str(np.random.randint(0,10)),
                content['dept'],
                create_content.get_random_year(),
                create_content.get_random_month(),
                create_content.get_random_day(),
                content['doc_num'],
                content['disease'],
                content['advise']
        ]
        image_name = save_to+auto_name+'_'+str(i)+'.png'
        print('-'*10+'creating '+image_name+'-'*10)
        result_image = create_img_data.auto_fill(list_of_positions, image, size, text)
        cv2.imwrite(image_name, result_image)

