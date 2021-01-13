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
		card_positions = ['dealer','1','2','3','4','5','6','7']
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
	def __init__(img_dir_path, info_dir_path):
		self.img_dir_path = image_path
		self.info_dir_path = info_folder_path
		self.croped_cards = []
		self.warped_cards = []
		self.Trans_card_2_ref = []
		self.Trans_ref_2_card = []

	# def 

if __name__ == "__main__":
	# some handy folder and file names
	root_dir = Path(__file__).parent.parent.parent
	SUB_DIR = 'data'
	SUB_DIR2 = 'raw_data'
	IMAGE_NAME = 'clutterd1.jpg'
	SUB_DIR3 = 'image_info'
	INFO_NAME = 'clutterd1.json'

	# some handy folder and file paths
	info_dir_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2,SUB_DIR3)
	info_file_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2, SUB_DIR3, INFO_NAME)
	image_dir_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2)
	image_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2, IMAGE_NAME)

	# list files in a directory
	listFilePathsInDir = lambda dir_path: [os.path.join(dir_path,file) for file in os.listdir(dir_path)]

	# load and check data
	RAC = ReadAndCheckData()
	data = RAC.readAll(listFilePathsInDir(info_dir_path))
	# RAC.checkData(data)

	# read cards

	# crop cards
		# find center

	# warp cards

	# filter enhance?

	# 
    

# print(image_path)

# img = cv2.imread(image_path)

# cv2.imshow('originan', img)

# # define corner points
# left_top = (559,741)
# right_top = (596,763)
# left_bot = (483,778)
# right_bot = (521,801)
# ref_points = np.float32( [left_top, right_top, left_bot, right_bot] ) 


# l = 483
# r = 596
# t = 801
# b = 741



# # wh_s, wh_l = 0.640, 0.716



# w,h = 75, 100
# target_points = np.float32( [[0,0], [w,0], [0,h], [w,h]] )


# perspective_T = cv2.getPerspectiveTransform(
# 	ref_points, target_points)
# warped_img = cv2.warpPerspective(img, perspective_T, (w,h))

# print(perspective_T)



# left_top = [559-l,741-b]
# right_top = [596-l,763-b]
# left_bot = [483-l,778-b]
# right_bot = [521-l,801-b]
# ref_points = np.float32( [left_top, right_top, left_bot, right_bot] ) 
# in_map = cv2.getPerspectiveTransform(target_points, ref_points)
# returned_img = cv2.warpPerspective(warped_img, in_map, (w+40,h-40), cv2.WARP_INVERSE_MAP)

# cv2.imshow('warped card', warped_img)
# cv2.imshow('returned card', returned_img)
# cv2.waitKey(0)
