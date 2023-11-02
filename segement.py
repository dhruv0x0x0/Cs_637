import cv2
import numpy as np
import time
import os
directory_path = '/home/dhruv0x0x0/PycharmProjects/Cs637/Dataset/'
file_name = str("Test.mp4")
filename = directory_path+file_name
outputname = filename[:len(filename)-3]+"txt"
with open(outputname, 'w') as file:
            video_capture = cv2.VideoCapture(filename)
            frame_width = int(video_capture.get(3))
            frame_height = int(video_capture.get(4))
            timestamp = 0

            time.sleep(3)
            while (video_capture.isOpened()):
                ret, image = video_capture.read()
                if not ret:
                    break
                timestamp = timestamp + 1
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                lower = np.array([10, 50, 0])
                upper = np.array([50, 150, 255])
                mask_all = cv2.inRange(hsv, lower, upper)
                mask_all = cv2.morphologyEx(
                    mask_all, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
                mask_all = cv2.morphologyEx(
                    mask_all, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
                mask2 = cv2.bitwise_not(mask_all)

                min_x, min_y, max_x, max_y = float('inf'), float('inf'), 0, 0
                zero_indices = np.argwhere(mask2 == 0)
                if zero_indices.size > 0:
                    min_y, min_x = zero_indices.min(axis=0)
                    max_y, max_x = zero_indices.max(axis=0)

                if (min_x > 0 and min_x < frame_width and max_x < frame_width and min_y > 0 and min_y < frame_height and max_y < frame_height):
                    cv2.rectangle(image, (min_x, min_y),
                                  (max_x, max_y), (0, 0, 255), 2)
                    xx = (min_x+max_x)//2
                    yy = (min_y+max_y)//2
                    area = (max_x - min_x)*(max_y - min_y)
                    area = area**0.5
                    file.write(f"{timestamp}, {xx}, {yy}, {area}\n")

video_capture.release()
cv2.destroyAllWindows()