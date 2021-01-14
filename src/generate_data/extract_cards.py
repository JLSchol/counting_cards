import cv2
import numpy as np
from pathlib import Path
import os
import json


class ReadAndCheckData():
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
		self.img_dir_path = img_dir_path
		self.info_dir_path = info_dir_path
		self.croped_cards = []
		self.warped_cards = []
		self.card_2_zero_T = []
		self.zero_2_card_T = []

	def crop(self, img, contours):
		pass

	def warpCardToZeroAndCrop(self, card_points, w_card, h_card ):
		zero_position = np.float32( [[0,0], [w_card,0], [0,h_card], (w_card, h_card)] )
		warped_img, persp_T = self.warpToTarget(card_points, zero_position, w_card, h_card)

		# redefine card_points by getting relative positions
		# print(zero_position[:,0])
		x_min,x_max = card_points[:,0].min(), card_points[:,0].max()
		y_min,y_max = card_points[:,1].min(), card_points[:,1].max()

		new_position = np.zeros((4,2),np.float32)
		new_position[:,0] = card_points[:,0] - x_min
		new_position[:,1] = card_points[:,1] - y_min
		inv_persp_T = cv2.getPerspectiveTransform(zero_position, new_position)
		cropped_img = cv2.warpPerspective(warped_img, inv_persp_T, 
			(x_max-x_min, y_max-y_min), dst=cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_TRANSPARENT)

		return warped_img, cropped_img, persp_T


	def warpToTarget(self, card_points, target_points, w_card, h_card):
		persp_T = cv2.getPerspectiveTransform(card_points, target_points)
		warped_img = cv2.warpPerspective(img, persp_T, (w_card, h_card))
		# cv2.imshow('warped card', warped_img)
		return warped_img, persp_T

if __name__ == "__main__":
	# some handy folder and file names
	root_dir = Path(__file__).parent.parent.parent
	[SUB_DIR, SUB_DIR2, SUB_DIR3] = ['data', 'raw_data', 'image_info'] 
	[IMAGE_NAME, INFO_NAME] = ['clutterd1.jpg', 'clutterd1.json']
	# some handy folder and file paths
	info_dir_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2,SUB_DIR3)
	# info_file_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2, SUB_DIR3, INFO_NAME)
	image_dir_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2)
	# image_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2, IMAGE_NAME)
	# list files in a directory
	listFilePathsInDir = lambda dir_path: [os.path.join(dir_path,file) for file in os.listdir(dir_path)]

	# load and check data
	RAC = ReadAndCheckData()
	data = RAC.readAll(listFilePathsInDir(info_dir_path))
	# RAC.checkData(data)
	# print(data)

	# read cards
	

	d0 = data[1]
	print(d0)
	# get image path
	img_path = d0['source_image_path']
	img = cv2.imread(img_path)
	# cv2.imshow(d0['source_image_name'], img)

	# warp image to zero position
	EC = ExtractCards()	
	(w_card, h_card) = (75, 100)
	card_points = np.float32( [d0['left_top'], d0['right_top'], d0['left_bot'], d0['right_bot']] )

	print(img.shape)
	warped_img, croped_img, persp_trans = EC.warpCardToZeroAndCrop(card_points, w_card, h_card)

	cv2.imshow('warped', warped_img)
	cv2.imshow('croped', croped_img)
	# cv2.imshow('warped', warped_img)

	# # compare crop and fore/backwarp
	# # check if back ground can be set transparant

	# # crop process
	# [x1,y1] = d0['left_top']
	# [x2,y2] = d0['right_top']
	# [x3,y3] = d0['left_bot']
	# [x4,y4] = d0['right_bot']
	# widths = np.array([x1,x2,x3,x4])
	# heigts = np.array([y1,y2,y3,y4])
	# x_min, x_max = widths.min(),widths.max()
	# y_min, y_max = heigts.min(),heigts.max()
	# dx = x_max-x_min
	# dy = y_max-y_min
	# print('widths: {} x_min: {} x_max: {}'.format(widths, x_min, x_max))
	# print('heigts: {} y_min: {} y_max: {}'.format(heigts, y_min, y_max))
	# use copy such that the poython garbage collectory remoove the original image
	# croped = img[y_min:y_max, x_min:x_max].copy() 

	cv2.waitKey(0)
