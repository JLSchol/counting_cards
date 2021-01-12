import tkinter as tk

from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import filedialog, ttk, messagebox

from PIL import Image, ImageTk
from pathlib import Path
from functools import partial
import os
import cv2
import numpy as np
import json
import ast

 


class GetPixelsFromImage():
    def __init__(self, file_path=False):
        # Picture path
        if file_path == False:
            root_dir = Path(__file__).parent.parent.parent
            SUB_DIR = 'data'
            SUB_DIR2 = 'raw_data'
            self.file_name = 'singles1.jpg'
            file_path = os.path.join(root_dir, SUB_DIR, SUB_DIR2, self.file_name)
        else:
            # self.image_path = file_path
            self.file_name = os.path.basename(file_path)


        self.img = cv2.imread(file_path)
        self.cach_imgs = [self.img.copy()]
        cv2.namedWindow(self.file_name) 

        
        self.pixel_list = []



    def drawPoint(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.cach_imgs.append(self.img.copy())
            self.pixel_list.append((x,y))

            cv2.circle(self.img, (x, y), 1, (0, 0, 255), thickness=2)
            cv2.putText(self.img, "%d,%d" % (x, y), (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (140, 15, 10), thickness=1)

        if event == cv2.EVENT_RBUTTONDOWN:
            if self.cach_imgs and self.pixel_list:
                self.img = self.cach_imgs[-1].copy()
                self.cach_imgs.pop()
                self.pixel_list.pop()
            else:
                pass
                
            # cv2.imshow(self.file_name, self.img)q

    def openImage(self):
        while(True):
            cv2.setMouseCallback(self.file_name, self.drawPoint)
            cv2.imshow(self.file_name, self.img)
            if (cv2.waitKey(10) & 0xFF == ord("q")):
                cv2.destroyAllWindows()
                break
            elif (cv2.getWindowProperty(self.file_name, 0) == -1):
                cv2.destroyAllWindows()
                break
        cv2.destroyAllWindows()


class MarkImagesGui(tk.Frame):
    '''  
        GUI USED TO OPEN AN IMAGE, MARK CARDS CORNERS, LABEL CARDS, CROP CARDS, SAVE CROPED CARDS

        widget functionalities:
        1. button: open file explorer to find image path
        2. combobox: display image path and other files in that directory
        3. button : open image in seperate window  
            3.1 left mouse click to set corner point
            3.2 right mouse click to remove corner point
            3.3 mark corners of cards in specific order (left top, right top, left bot, right bot, )
            3.4 can be used to mark multiple cards in one image
            3.5 Hit q or exit window to save coordinates

        4. text: display selected coordinates of card corners
        5. entry: label card values comma seperated (Ad, Kc, Qh, Js, 10h,..)
        6. entry: player position of card values (1, 2, 3, 4, 5, 6, 7, dealer)

        7. button: open file explorer to find save croped images
        8. combobox: display image path or enter manually
        9. button: save info to json file  

        7. button: Next image in list
        8. button: previous image in list

        Current issues:
        when image is open, the gui can not be filled in
        When the image is open, it doen not allow enlarging the image
    '''
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        root_dir = Path(__file__).parent.parent.parent
        SUB_DIR = 'data'
        SUB_DIR2 = 'raw_data'
        START_FILE = 'clutterd1.jpg'
        INITIAL_IMAGE = os.path.join(root_dir, SUB_DIR, SUB_DIR2, START_FILE)

        # variable with initial image path and directory list
        self.corner_coordinates = tk.IntVar()
        self.image_path = tk.StringVar(value=INITIAL_IMAGE)
        self.files_in_dir = self._listFilePathsInDir(Path(self.image_path.get()).parent)

        self.save_dir = tk.StringVar(value=Path(self.image_path.get()).parent)
        self.save_dir_options = self._listFoldersInDir(self.save_dir.get())


        self.save_file_name = tk.StringVar(value=self._getJsonFileName(self.image_path.get()))
        print(self.save_file_name.get())

        # self.new

        # self.coordinates = 

        # put gui variable here (that are traced)

        # initializeWindow
        self.initializeWindow()

    def initializeWindow(self):
        # frame
        (w,h) = (900,700)
        self.master.title("mark images")
        self.master["bg"]="black"
        self.master.geometry("900x700")  
        frame = tk.Frame(self.master, bg='#ff6666').place(relx=0.02,rely=0.02,relwidth=0.96,relheight=0.96)

        # layout params
        bw, bh = 0.15, 0.05
        row1, col1 = 0.05, 0.05
        row2, col2 = row1 + 2*bh, col1+bw
        row3, col3  = 0.8, 0.575
        row4, col4  = 0.9, 0.8

        ######## ROW 1 ########
        # open file manager
        set_image_path = tk.Button(self.master, text="select file", command=self.setImagePath)
        set_image_path.place(relx=col1, rely=row1, relwidth=bw, relheight=bh)
        # show path, find in related folder, change names
        self.combo_file_path = ttk.Combobox(self.master, values=self.files_in_dir, textvariable=self.image_path,
                            postcommand=lambda: self.combo_file_path.configure(values=self.files_in_dir)) 
        self.image_path.trace('w',self._imagePathCB)       
        self.combo_file_path.place(relx=col2, rely=row1, relwidth=col4-col1-bw, relheight=bh)
        # open image for given path in combo_file_path
        open_image = tk.Button(self.master, text="open image", command=self.openImage)
        open_image.place(relx=col4, rely=row1, relwidth=bw, relheight=bh)

        ######## ROW 2 ########
        # coordinated entry and label
        coordinate_label = tk.Label(self.master, text="card corner coordinates")
        coordinate_label.place(relx=col1, rely=row2, relwidth=col3 - col1 - bw/2, relheight=bh)
        self.coordinate_text = tk.Text(self.master, bg='white', yscrollcommand=True)
        self.coordinate_text.place(relx=col1, rely=row2+bh, relwidth=col3 - col1 - bw/2, relheight=row3- row2-2*bh)
        # label entry and label
        card_label = tk.Label(self.master, text="card label")
        card_label.place(relx=col3, rely=row2, relwidth=bw, relheight=bh)
        self.label_text = tk.Text(self.master, bg='white', yscrollcommand=True)
        self.label_text.place(relx=col3, rely=row2+bh, relwidth=bw, relheight=row3- row2-2*bh)
        # positions of card on table entry and label
        table_pos_label = tk.Label(self.master, text="table position")
        table_pos_label.place(relx=col4, rely=row2, relwidth=bw, relheight=bh)
        self.table_pos_text = tk.Text(self.master, bg='white', yscrollcommand=True)
        self.table_pos_text.place(relx=col4, rely=row2+bh, relwidth=bw, relheight=row3- row2-2*bh)

        ######## ROW 3 ########
        # open file manager
        set_save_dir_but = tk.Button(self.master, text="select folder", command=self.setSaveDirectory)
        set_save_dir_but.place(relx=col1, rely=row3, relwidth=bw, relheight=bh)
        # show path, find in related folder, change names
        self.save_dir_combo = ttk.Combobox(self.master, values=self.save_dir_options, textvariable=self.save_dir) 
        self.save_dir.trace('w',self._saveDirCB)       
        self.save_dir_combo.place(relx=col2, rely=row3, relwidth=col3-col2+bw/2, relheight=bh)
        # file name to be saved with card info
        entry_file_name = tk.Entry(self.master, bg='white', textvariable=self.save_file_name)
        self.save_file_name.trace('w', self._saveFileNameCB)
        entry_file_name.place(relx=col3+bw/2, rely=row3, relwidth=bw, relheight=bh)
        # save button
        save_file_but = tk.Button(self.master, text="save file", command=self.saveFile)
        save_file_but.place(relx=col4, rely=row3, relwidth=bw, relheight=bh)

        ######## ROW 4 ########
        # previous image
        previous_image_but = tk.Button(self.master, text="previous image", command=partial(self.newImageCB, arg='previous_image') )
        previous_image_but.place(relx=col1, rely=row4, relwidth=bw, relheight=bh)
        # next image
        next_image_but = tk.Button(self.master, text="next image", command=partial(self.newImageCB, arg='next_image'))
        next_image_but.place(relx=col4, rely=row4, relwidth=bw, relheight=bh)


    def setImagePath(self):
        self.image_path.set(askopenfilename(parent=root, 
            initialdir=Path(__file__).parent.parent.parent, title='Choose an image.'))
        # get list of file paths from same directory and update in self.files
        self.files_in_dir = self._listFilePathsInDir(Path(self.image_path.get()).parent)

    def openImage(self):
        if not self.combo_file_path.get():
            messagebox.showerror("Error","Please select a file path")
            return 0
        if not os.path.isfile(self.combo_file_path.get()):
            messagebox.showerror("Error","Please select a correct file path")
            return 0

        # update paths in combobox (dropdown menu), save file and save file directories
        self.files_in_dir = self._listFilePathsInDir(Path(self.image_path.get()).parent)
        # update save file.json 
        self.save_file_name.set( self._getJsonFileName(self.image_path.get()) )

        # open the image using cv that allows drawing of points
        GPFI = GetPixelsFromImage(self.combo_file_path.get())
        GPFI.openImage()
        # self.corner_coordinates = _getCornerCoordinates()

        # create coordinate string and insert in text window
        text = ""
        for i, (x,y) in enumerate(GPFI.pixel_list,0):
            if i%4 ==0 and i!=0:
                text += '\n'
            pixel_str = "({},{}), ".format(x,y)
            text += pixel_str

        self.coordinate_text.insert(tk.INSERT,text) 

    def setSaveDirectory(self):
        self.save_dir.set(askdirectory(parent=root, 
            initialdir=Path(__file__).parent.parent.parent, title='Choose save directory.'))

    def saveFile(self):
        # read lines of text boxes
        coordinates = self._read_coordinates(self.coordinate_text)
        labels = self._read_text_input(self.label_text)
        player_positions = self._read_text_input(self.table_pos_text)

        # construct dictionair
        dict_list = self._setDictionair(coordinates, labels, player_positions, self.image_path.get())
        # save to file
        self._writeToJsonFile( dict_list, os.path.join(self.save_dir.get(),self.save_file_name.get()) )

        # clear text widgets
        self._clearTextWidgets()

    def _clearTextWidgets(self):
        self.coordinate_text.delete('1.0',tk.END)
        self.label_text.delete('1.0',tk.END)
        self.table_pos_text.delete('1.0',tk.END)



    def newImageCB(self, arg):
        # update image_path
        current_image_path = os.path.abspath(self.image_path.get())
        # find next/previous position of current path index in directory
        i = self.files_in_dir.index(current_image_path)
        if arg=='next_image':
            i+=1
        elif arg=='previous_image':
            i-+1
        # set new image path
        self.image_path.set(self.files_in_dir[i])
        # open image
        self.openImage()



    def _read_text_input(self, text_widget):
        text = text_widget.get('1.0', tk.END).splitlines()

        return [line.replace(",", "") for line in text]


        # return [line.split('.')[0] for line in text]
        # return [line for line in text]

    def _read_coordinates(self, text_widget):
        text = text_widget.get('1.0', tk.END).splitlines()
        coordinate_2Dlist = []
        for text_line in text:
            # convert to literal string of an list of tuples
            list_of_tuples_txt = "["+text_line+"]"
            list_of_tuples = ast.literal_eval(list_of_tuples_txt)
            coordinate_2Dlist.append(list_of_tuples)
        return coordinate_2Dlist

    def _setDictionair(self, coordinate_cards, labels, player_positions, image_path):
        for card_i_coordinates in coordinate_cards:
            n_coordinates = len(card_i_coordinates)
            card_corners = 4
            assert n_coordinates%card_corners == 0

        source_image_name = os.path.basename(image_path)
        createName = lambda label, pos, name: label +'_'+str(pos)+'_'+name.split('.')[0]

        info_cards = []
        for cornerpoints, label, pos in zip(coordinate_cards, labels, player_positions):
            info_card = {'source_image_path': image_path,
                'source_image_name': source_image_name,
                'card': label,
                'left_top': cornerpoints[0],
                'right_top': cornerpoints[1],
                'left_bot': cornerpoints[2],
                'right_bot': cornerpoints[3],
                'card_position': pos,
                'card_name': createName(label,pos,source_image_name)}
            info_cards.append(info_card.copy())

        return info_cards

    def _writeToJsonFile(self, dict_list, file_path):
        try: 
            with open(file_path,'w') as out_file:
                json.dump(dict_list, out_file)
        except EnvironmentError:
            print("WHOOPS!\nOp een of andere duistere reden can er niet naar: \n{} geschreven worden"
                .format(file_path))

    def _getJsonFileName(self,image_path):
        image_file_name = os.path.basename(image_path)
        file_name = image_file_name.split('.')[0]
        json_file_name = file_name+'.json'
        return json_file_name

    def _listFoldersInDir(self, top_dir):
        return [os.path.abspath(Dir[0]) for Dir in os.walk(top_dir)]

    def _listFilePathsInDir(self, dir_path):
        return [os.path.join(dir_path,file) for file in os.listdir(dir_path)]

    def _imagePathCB(self,*args):
        print(self.image_path.get())

    def _saveDirCB(self,*args):
        print(self.save_dir.get())

    def _saveFileNameCB(self,*args):
        print(self.save_file_name.get())



if __name__ == "__main__":

    root = tk.Tk()
    GUI = MarkImagesGui(master=root)
    GUI.mainloop()
