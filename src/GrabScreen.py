import numpy as np
import mss
import cv2
import sys
import ctypes




class GrabScreen(object):
	def __init__(self):
		self.title = "[MSS] FPS benchmark"

		user32 = ctypes.windll.user32
		screensize1 = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		screensize2 = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
		self.mon = {"top": 0, "left": 0, "width": screensize1[0], "height": screensize1[1]}


		# sys.exit()


	def record_screen(self):

		# initiate
		sct = mss.mss()
		


		while True:
			# grap raw pixel from screen and save to np array
			img = np.asarray(sct.grab(self.mon))

			# display picture using opencv
			cv2.imshow(self.title, img)


			if cv2.waitKey(25) & 0xFF == ord("q"):
				cv2.destroyAllWindows()
				break




def main():
	GS = GrabScreen()
	GS.record_screen()


if __name__ == '__main__':
	
	main()

