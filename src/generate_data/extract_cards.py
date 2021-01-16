import cv2
import numpy as np
from pathlib import Path
import os
import json


class ReadCheckWriteData():
	def __init__(self):
		self.data = []

	def readAll(self, file_paths):
		data_list = []
		for file_path in file_paths:
			data = self._readJsonFile(file_path)
			if isinstance(data, list):
				data_list.extend(data)
			else:
				data_list.extend([data])
		self.data = data_list
		return data_list	

	def checkData(self, data_list):
		for data in data_list:
			if not self._isValidCard(data['card']):
				print("image {} has incorrect card label {}".
					format(data['source_image_name'],data['card']))

			elif not self._isValidCardPosition(data['card_position']):
				print("image {} has incorrect card position {}".
					format(data['source_image_name'],data['card_position']))
			elif not self._hasCoordinates(data):
				print("image {} has incorrect coordinates {}\n{}\n{}\n{}".
					format(data['source_image_name'],
						data['left_top'],data['right_top'],data['left_bot'],data['right_bot']))

	def _readJsonFile(self, file_path):
		try:
			with open(file_path) as file:
				data = json.load(file)
				return data
		except OSError:
			print("Could not read file from {}".format(file_path))

	def writeToJsonFile(self, dict_list, file_path):
		try: 
			with open(file_path,'w') as out_file:
				json.dump(dict_list, out_file)
		except EnvironmentError:
			print("WHOOPS!\nOp een of andere duistere reden can er niet naar: \n{} geschreven worden"
			.format(file_path))

	def _isValidCard(self, card):
		cards = ['As','Ac','Ah','Ad', 'Ks','Kc','Kh','Kd', 'Qs','Qc','Qh','Qd', 'Js','Jc','Jh','Jd',
		'10s','10c','10h','10d', '9s','9c','9h','9d', '8s','8c','8h','8d', '7s','7c','7h','7d',
		'6s','6c','6h','6d',    '5s','5c','5h','5d', '4s','4c','4h','4d', '3s','3c','3h','3d',
		'2s','2c','2h','2d']
		if card in cards:
			return True
		else:
			return False

	def _isValidCardPosition(self, card_position):
		card_positions = [0,'1','2','3','4','5','6','7']
		if card_position in card_positions:
			return True
		else:
			return False

	def _hasCoordinates(self, data):
		isList = lambda x: True if isinstance(x, list) else False
		for key in ['left_top','right_top','left_bot','right_bot']:
			if not isList(data[key]):
				return False
				for (x,y) in data[key]:
					if isinstance(x, int) == False or isinstance(y, int) == False:
						return False 
		return True


class ExtractCards():
	def __init__(self, info_dir_path=None, img_dir_path=None):


	def selectAndSetBg(self, img, contours, fill_color, mask_value=1):
		img_filled =img.copy()
		# our stencil - some `mask_value` contours on black (zeros) background, 
		# the image has same height and width as `img`, but only 1 color channel
		stencil  = np.zeros(img.shape[:-1]).astype(np.uint8)
		cv2.fillPoly(stencil, contours, mask_value) # gets  stencil is cutout with the contour
		select = stencil != mask_value  # select everything that is not mask_value
		img_filled[select] = fill_color            # and fill it with fill_color
		return img_filled

	def cropAlongContour(self, img, contour):
		[x_min, y_min], [x_max, y_max], [dx,dy] = self._minMaxDiff(contour)
		return img[y_min:y_max, x_min:x_max].copy()

	def warpToTargetAndBack(self, img, source_points, target_points, dx_target, dy_target):
		warped_img, persp_T = self.warpToTarget(img, source_points, target_points, dx_target, dy_target)
		cropped_img, inv_persp_T = self.warpBackFromTarget(warped_img, source_points, target_points)
		return warped_img, cropped_img, persp_T, inv_persp_T

	def warpBackFromTarget(self, img, source_points, target_points):
		"""" The source points might be pixel values anywhere in the image and should be translated
		to the zero position which is the top left of the original image. Next we transform
		from the target to the zero position using inverse mapping argument
		"""
		# find width and height and translation distance (_min)
		[x_min, y_min], _, [dx,dy] = self._minMaxDiff(source_points)
		# translate source points to zero points
		zero_points = self._translatePoints(source_points, x_min, y_min)

		# get inverse perspectaive matrix and warp back
		# note the inputs of the function and that the mapping is from target -> original 
		original_img, inv_persp_T = self.warpToTarget(img, target_points, zero_points, 
			dx, dy, cv2.WARP_INVERSE_MAP, cv2.BORDER_TRANSPARENT)
		return original_img, inv_persp_T

	def warpToTarget(self, img, source_points, target_points, dx_target, dy_target, dst=None, borderMode=None):
		
		persp_T = cv2.getPerspectiveTransform(source_points, target_points)
		warped_img = cv2.warpPerspective(img, persp_T, (int(dx_target), int(dy_target)), 
															dst=dst, borderMode=borderMode)
		return warped_img, persp_T

	def _translatePoints(self, source_points, x_dist, y_dist):
		translated_points = np.zeros((4,2),np.float32)
		translated_points[:,0] = source_points[:,0] - x_dist
		translated_points[:,1] = source_points[:,1] - y_dist
		return translated_points

	def _minMaxDiff(self, contour):
		# find width and height and translation distance (_min)
		xy_min = contour.min(axis=0)
		xy_max = contour.max(axis=0)
		d_xy = xy_max - xy_min
		return xy_min, xy_max, d_xy

	def getPerspectiveMats(self, source_points, target_points):
		persp_T = cv2.getPerspectiveTransform(source_points, target_points)
		Inv_persp_T = cv2.getPerspectiveTransform(target_points, source_points)
		return persp_T, Inv_persp_T


if __name__ == "__main__":
	# some handy folder and file names
	root_dir = Path(__file__).parent.parent.parent
	SUB_DIR, SUB_DIR2, SUB_DIR3, SUB_DIR4 = 'data', 'raw_data', 'image_info', 'croped_cards'
	SUB_DIR5, SUB_DIR6 = 'cropped', 'warped'
	[IMAGE_NAME, INFO_NAME] = ['clutterd1.jpg', 'clutterd1.json']
	# some handy folder and file paths
	info_dir_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2,SUB_DIR3)
	# info_file_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2, SUB_DIR3, INFO_NAME)
	image_dir_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2)
	# image_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2, IMAGE_NAME)
	# list files in a directory

	# load and check data
	RAC = ReadCheckWriteData()
	listFilePathsInDir = lambda dir_path: [os.path.join(dir_path,file) for file in os.listdir(dir_path)]
	data = RAC.readAll(listFilePathsInDir(info_dir_path))
	# RAC.checkData(data)

	EC = ExtractCards()	
	w_card, h_card = 75, 100 # define dimensions of cards 
	target_coord = np.float32( [[0,0], [w_card,0], [0,h_card], (w_card, h_card)] ) # bbox of front of card
	new_data = []
	for i,card in enumerate(data): # opening, processing, writing for every loop makes it slow (whatevs)
		print('working on file: {} of {}'.format(i,len(data)))
		# # read image
		img_path = card['source_image_path']
		img = cv2.imread(img_path)
		
		########### warp image to zero position and back ###########
		# get card coordinates
		card_coords = np.float32( [card['left_top'], card['right_top'], card['left_bot'], card['right_bot']] )
		# warp to target and back providing both perspective matrices and cropping the image
		warped_img, warped_back_img, persp_T, inv_persp_T = EC.warpToTargetAndBack(img, 
																	card_coords, target_coord, w_card, h_card)

		########### crop image and set bg to black ###########
		contour = np.array([card['left_top'],card['right_top'],card['right_bot'],card['left_bot']], dtype=np.int32)
		bg_color = (0,0,0)
		img_black_bg = EC.selectAndSetBg(img, [contour], bg_color)
		croped_img = EC.cropAlongContour(img_black_bg, contour)


		########### Save cards and informatino to file ###########
		# create saved dir name
		name = card['card_name']+ '.jpg'
		croped_dir = os.path.join(root_dir, SUB_DIR, SUB_DIR4 ,SUB_DIR5)
		warped_dir = os.path.join(root_dir, SUB_DIR, SUB_DIR4 ,SUB_DIR6)
		croped_path = os.path.join(croped_dir, name)
		warped_path = os.path.join(warped_dir, name)
		# clear old files
		# try:
		# 	os.remove(croped_path)
		# 	os.remove(warped_path)
		# except OSError as error: 
		#     print(error) 
		#     print("File path can not be removed") 
		# write
		cv2.imwrite(croped_path, croped_img)
		cv2.imwrite(warped_path, warped_img)


		########### add info to dictionary and add to list ###########
		card['transform'] = persp_T.tolist()
		card['inv_transform'] = inv_persp_T.tolist()
		card['cropped_path'] = croped_path
		card['warped_path'] = warped_path
		new_data.append(card)

	# print(new_data)
	
	########### Save card info to file ###########
	RAC.writeToJsonFile(new_data, os.path.join(root_dir, SUB_DIR, SUB_DIR4, 'cards_info.json'))




	# cv2.imshow(card['source_image_name'], img)
	# cv2.imshow('warped_img', warped_img)
	# cv2.imshow('warped_back_img', warped_back_img)
	# cv2.imshow('croped_img', croped_img)

	# cv2.imwrite('warped.jpg', warped_img)
	# cv2.imwrite('warped_back.jpg', warped_back_img)
	# cv2.imwrite('croped_img.jpg', croped_img)

	# # compare crop and fore/backwarp
	# # check if back ground can be set transparant

	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
