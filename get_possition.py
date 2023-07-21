import cv2
import numpy as np
from os.path import splitext

drawing = False
ix, iy = -1, -1
position_list = []

def get_positions(event, x, y, flags, param):
    global drawing, ix, iy, position_list, image, temp_image
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            image = temp_image.copy()
            cv2.rectangle(image, (ix, iy), (x, y), (0, 255, 0), 2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        color = image[y+4][x+4]
        temp_image = cv2.rectangle(temp_image, (ix, iy), (x, y), color=(int(color[0]), int(color[1]), int(color[2])), thickness=-1)
        image = temp_image.copy()
        print([[ix, iy], [x, y]])
        position_list.append([[ix, iy], [x, y]])

if __name__ == '__main__':
    path = 'sample/10.png'
    image = cv2.imread(path)
    temp_image = image.copy()
    cv2.namedWindow('get possition')
    cv2.setMouseCallback('get possition', get_positions)
    while(True):
        cv2.imshow('get possition', image)
        if cv2.waitKey(20) & 0xFF == ord('d'):
            print(position_list)
            path_and_name, suffix = splitext(path)
            image_rename = path_and_name + '_whiteout' + '.png'
            with open(path_and_name + '_positions.txt', 'w') as position_file:
                position_file.write(str(position_list))
            cv2.imwrite(image_rename, image)
        elif cv2.waitKey(20) & 0xFF == ord('x'):
            break
    cv2.destroyAllWindows()