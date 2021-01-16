# how to augment:
# scale: [Bad, not useful, potentially usefull, usefull, important, mandatory] 
# augment complete image
	# mirror 			(Bad)
		# hor/ver axis
	# crop				(mandatory, make sure to crop to a of 32 and that the table is in there)
	# rotate 	 		(Bad)
	# shear	 	 		(not usefull)
	# brightness 		( usefull )
	# exposure  	 	(potentially usefull)
	# blur		 		(potentially usefull)
	# noise(gaussioan)	(potentially usefull)
# augment bounding box (card)
	# overlap			(mandatory)
	# mirror			( not usefull)
		# hor/ver axis
	# rotations			( important)
	# scale				( potentially usefull)
	# crop				( not usefull)
	# shear 			( important )
	# warp 				( important )
	# Brightness 		( not usefull )
	# exposure			( not usefull)
	# blur				( not usefull )
	# noise				( )

import numpy as np

import cv2
# from scipy import ndimage
# from PIL import Image



class AugmentImage():
	def __init__(self):
		print('init')

	def rotateSCIPY(self, img, angle, flag='deg'):
		rotated = ndimage.rotate(image_to_rotate, 45)
		return rotated
	def rotateCV(self, img, angle, flag='deg'):
		rad2deg = lambda rad: 180/3.14159
		image_center = tuple(np.array(img.shape[1::-1]) / 2)
		rot_mat = cv2.getRotationMatrix2D(image_center, rad2deg(angle), 1.0)
		rotated = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
		return rotated
	def rotatePIL(self, img, angle, flag='deg'):
		cv2.rotate(img, rotateCode)




if __name__ == "__main__":
	img_path = "C:\\Users\\Jasper\\Desktop\\counting_cards\\data\\croped_cards\\warped\\2c_4_singles16.jpg"
	img = cv2.imread(img_path)

	Aug = AugmentImage()
	img_r = Aug.rotateCV(img, 30)



	cv2.imshow('img', img)
	cv2.imshow('img_r', img_r)
	cv2.waitKey(0)
	# cv2.destroyAllWindows()
