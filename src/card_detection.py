import cv2
import sys
import os
from pathlib import Path

# custom class
# from package(folder).module(file) import Class
from grab_screen import GrabScreen




class CardDetection(object):
	def __init__(self):
		pass


	def matchImage(self, img, match_img, show=True):
		# match
		match_result = cv2.matchTemplate(img, match_img, cv2.TM_CCOEFF_NORMED)
		# draw box
		self.drawBox(img, match_img, match_result)	
		# show with box
		if show:
			cv2.imshow('detected', img)
			cv2.waitKey()
		return img

		
	def drawBox(self, img, match_img, match_result):
		# get the best match position
		_, max_val, _, max_loc = cv2.minMaxLoc(match_result) # only interested in whitest pixel given method TTM_CCOEFF_NORMEDM
		# print("best match from top left pos: {} \nWith confidence: {}".format(max_loc,max_val))

		# draw rectangle
		top_left = max_loc
		bottom_right = (top_left[0]+match_img.shape[1], top_left[1]+match_img.shape[0])
		cv2.rectangle(img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_4)



def main():
	GS = GrabScreen()

	# grap images
	img = GS.grabImage('bj_table.jpg',False)
	match_img = GS.grabImage('AceSpades.jpg',False)	

	# detection
	CD = CardDetection()
	result = CD.matchImage(img, match_img, True)

	# save image
	GS.saveImage(result, 'detection_AS', 'jpg')





if __name__ == '__main__':
	
	main()
