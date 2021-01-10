import cv2
import numpy as np
from pathlib import Path
import os

root_dir = Path(__file__).parent.parent
SUB_DIR = 'data'
SUB_DIR2 = 'raw_data'
FILE_NAME = 'singles1.jpg'
image_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2, FILE_NAME)

print(image_path)

img = cv2.imread(image_path)

cv2.imshow('originan', img)

# define corner points
left_top = (559,741)
right_top = (596,763)
left_bot = (483,778)
right_bot = (521,801)
ref_points = np.float32( [left_top, right_top, left_bot, right_bot] ) 


l = 483
r = 596
t = 801
b = 741



# wh_s, wh_l = 0.640, 0.716



w,h = 75, 100
target_points = np.float32( [[0,0], [w,0], [0,h], [w,h]] )


perspective_T = cv2.getPerspectiveTransform(
	ref_points, target_points)
warped_img = cv2.warpPerspective(img, perspective_T, (w,h))

print(perspective_T)



left_top = [559-l,741-b]
right_top = [596-l,763-b]
left_bot = [483-l,778-b]
right_bot = [521-l,801-b]
ref_points = np.float32( [left_top, right_top, left_bot, right_bot] ) 
in_map = cv2.getPerspectiveTransform(target_points, ref_points)
returned_img = cv2.warpPerspective(warped_img, in_map, (w+40,h-40), cv2.WARP_INVERSE_MAP)

cv2.imshow('warped card', warped_img)
cv2.imshow('returned card', returned_img)
cv2.waitKey(0)
