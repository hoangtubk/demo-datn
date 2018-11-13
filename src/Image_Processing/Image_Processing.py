"""
* Created by PyCharm.
* User: tuhoangbk
* Date: 05/10/2018
* Time: 23:27
*Have a nice day　:*)　:*)
"""

import cv2

def draw_rectangle_on_image(image_path, boxes):
    img = cv2.imread(image_path, 4)
    lineThickness = 1
    for box in boxes:
        for i in range(-2, 6, 2):
            cv2.line(img, (box[i], box[i+1]), (box[i+2], box[i+3]), (0, 255, 0), lineThickness)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    draw_rectangle_on_image()
