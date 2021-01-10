import numpy as np
import mss
import cv2
import sys
import ctypes
import os
import time
from pathlib import Path
from pywinauto import Desktop




class GrabScreen(object):
	def __init__(self):
		self.TITLE = "screen_capture"

		user32 = ctypes.windll.user32
		screensize1 = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		# screensize2 = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
		self.mon = {"top": 0, "left": 0, "width": screensize1[0], "height": screensize1[1]}
		# self.mon = {"top": 40, "left": 0, "width": 800, "height": 640}
		self.list_window_names()
		# names can look something like:
		# name = 'Play Live Blackjack online | Unibet Casino - Google Chrome'
		# name = 'Play Live Blackjack online | Unibet Casino: audio wordt afgespeeld - Google Chrome'
		# name = 'Play Live Blackjack online | Unibet Casino - Mozilla Firefox'

		

	def list_window_names(self):	
		windows = Desktop(backend="uia").windows()
		print([w.window_text() for w in windows])


	def recordScreen(self):
		sct = mss.mss()
		# loop_time = time.time()
		while True:
			# grap raw pixels from screen and save to np array
			img = np.asarray(sct.grab(self.mon))

			# display picture using opencv
			cv2.imshow(self.TITLE, img)

			# wacht 10 ms if keyboard 'q' quit window
			# else if 'X' pressed on window quit window
			if (cv2.waitKey(10) & 0xFF == ord("q")):
				cv2.destroyAllWindows()
				break
			elif (cv2.getWindowProperty(self.TITLE, 0) == -1):
				cv2.destroyAllWindows()
				break

			# # measure fps
			# print('fps {}'.format(1/(time.time() - loop_time)))
			# loop_time = time.time()


	def grabImage(self, image_file_name, show=True, method=cv2.IMREAD_UNCHANGED):
		# get path to files
		root_dir = Path(__file__).parent.parent
		SUB_DIR = 'docs'
		image_path = os.path.join(root_dir, SUB_DIR, image_file_name)
		print(image_path)
		img = cv2.imread(image_path, method)
		if show:
			cv2.imshow('detected', img)
			cv2.waitKey()
		return img
		

	def saveImage(self, img, name, ext, sub_dir = 'docs'):
		image_path = os.path.join( Path(__file__).parent.parent, sub_dir, name+'.'+ext )
		cv2.imwrite(image_path, img)





def main():
	GS = GrabScreen()

	# RECORD SCREEN
	GS.recordScreen()

	# Grab image from docs folder
	img = GS.grabImage('bj_table.jpg',True)




if __name__ == '__main__':
	
	main()
