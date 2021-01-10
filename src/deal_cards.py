import sys
import os
import shutil
from pathlib import Path
from datetime import datetime
from time import strftime


'''
This file should simulate the dealer dealing blackjack cards
The idea was/is to write all played cards to a file
Currently on hold as focus is now on card detection module
Current functionality clears a log directory and opens an outputfile
'''


class DealCards(object):
	def __init__(self):
		# create file
		self.date_time = datetime.now().strftime("%Y_%m_%d_%H_%M") # year_month_day_hour_minutes
		self.file_name = 'count_' + self.date_time
		root_dir = Path(__file__).parent.parent
		SUB_DIR = 'log'
		self.path_to_file = os.path.join(root_dir, SUB_DIR, self.file_name)

		self.clearLogDir(os.path.join(root_dir, SUB_DIR))
		self.initTextFile(self.path_to_file, self.date_time)


	def clearLogDir(self, path_to_folder):
		for filename in os.listdir(path_to_folder):
			file_path = os.path.join(path_to_folder, filename)
			try:
				if os.path.isfile(file_path) or os.path.islink(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				print('Failed to delete %s. Reason: %s' % (file_path, e))

	def initTextFile(self, path_to_file, first_line):
		try: 
			with open(path_to_file,'w') as out_file:
				out_file.write(first_line)
		except EnvironmentError:
			print("WHOOPS!\nOp een of andere duistere reden can er niet naar: \n{} geschreven worden"
				.format(path_to_file))

	def addLine(self):
		pass
		# try:
		# 	with open(file)


def main():
	DC = DealCards()
	# DC.addLine()
	




if __name__ == '__main__':
	
	main()
