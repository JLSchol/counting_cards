import os
from pathlib import Path
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from functools import partial
import ast
import json
# custom classes:
from mark_pixels import MarkImage



class AnnotateCardsGui(tk.Frame):
    '''  
        HOW TO USE GUI:
        1. Open an image such that card corners can be marked and extracted
            1.1 left mouse click to mark corner point
            1.2 right-clicking goes back to previous image (similar as in ctrl+z)
            1.3 right-dragging up/down zooms in/out
            1.3 mark corners of cards in specific order!!!left top, right top, left bot, right bot!!!
            1.4 can and should be used to mark multiple cards in one image (All that has no overlap)
            1.5 Hit q, Esc or exit window to save coordinates
        2. Allows for adding extra information to the marked card corners:
            - card type (e.g. Qh=Quen of hearths) Seperate each card by a new line
            - card position on the table (e.g. Dealer, 1, 2) seperate by new line
        3. Save labled cards to json format containing:
            - 'source_image_name'   = Path of source image
            - 'card'                = cart type
            - 'left_top'            = left top pixel value of the card
            - 'right_top'           = right top pixel value of the card
            - 'left_bot'            = left bot pixel value of the card
            - 'right_bot'           = right bot pixel value of the card
            - 'card_position'       = position of card on the table 1-7 + dealer
            - 'card_name'           = Unige name generated based on card information:(card_cardPosition_sourceImageName)

        widget functionalities by GUI name:
        1. select file: open file explorer to find image path
        2. Entry field top: display image path and other files in that directory can be changed in line
        3. open image : open image in seperate window  
        4. image display and pixel values: display image that was marked
        5. Entry field below image: Entry display of marked coordinates of card corners (fills automatically)
        6. card label: Entry field for card values comma seperated (Ad, Kc, Qh, Js, 10h,..)
        7. table position: Entry player position of card values (dealer, 1, 2, 3, 4, 5, 6, 7)
        8. select folder: open file explorer to find folder that stores .json
        9. Entry field bot left: display image path or enter manually
        9. Entry field bot right: entry field json file name
        10. save file: save json file in destination folder with info of identified cards
        12. previous image:  previous image in list
        11. next image: Next image in list
    '''
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # some foders names and basis file
        root_dir = Path(__file__).parent.parent.parent
        SUB_DIR = 'data'
        SUB_DIR2 = 'raw_data'
        SUB_DIR3 = 'image_info'
        START_FILE = 'clutterd1.jpg'
        INITIAL_IMAGE = os.path.join(root_dir, SUB_DIR, SUB_DIR2, START_FILE)
        # image path and files in that directory
        self.image_path = tk.StringVar(value=INITIAL_IMAGE)
        self.files_in_dir = self._listFilePathsInDir(Path(self.image_path.get()).parent)
        # save path and folders in that directory
        save_dir_path = os.path.join(Path(self.image_path.get()).parent, SUB_DIR3)
        self.save_dir = tk.StringVar(value=save_dir_path)
        self.save_dir_options = self._listFoldersInDir(self.save_dir.get())
        # name of the jason file that has labeld card info(coordinates, player pos, card, etc)
        self.save_file_name = tk.StringVar(value=self._getJsonFileName(self.image_path.get()))
        # save some time with entry of position of the card on the table
        self.initial_card_pos_sequency = "dealer\n1\n2\n3\n4\n5\n6\n7"
        # initializeWindow
        self.initializeWindow()


    def initializeWindow(self):
        # init frame
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

        ################################ ROW 1 ################################
        # open file manager
        set_image_path = tk.Button(self.master, text="select file", command=self.navigateToImage)
        set_image_path.place(relx=col1, rely=row1, relwidth=bw, relheight=bh)
        # show path, find in related folder, change names
        self.combo_file_path = ttk.Combobox(self.master, values=self.files_in_dir, textvariable=self.image_path,
                            postcommand=lambda: self.combo_file_path.configure(values=self.files_in_dir)) 
        self.image_path.trace('w',self._imagePathCB)       
        self.combo_file_path.place(relx=col2, rely=row1, relwidth=col4-col1-bw, relheight=bh)
        # open image for given path in combo_file_path
        open_image = tk.Button(self.master, text="open image", command=self.openImage)
        open_image.place(relx=col4, rely=row1, relwidth=bw, relheight=bh)

        ################################ ROW 2 ################################
        # coordinate label, image wid and tex
        coordinate_label = tk.Label(self.master, text="image display and pixel values")
        coordinate_label.place(relx=col1, rely=row2, relwidth=col3 - col1 - bw/2, relheight=bh)
        self.image_wid = tk.Label(self.master)
        self.image_wid.place(relx=col1, rely=row2+bh, relwidth=col3 - col1 - bw/2, relheight=row3- row2-3*bh)
        self.coordinate_text = tk.Text(self.master, bg='white', yscrollcommand=True)
        self.coordinate_text.place(relx=col1, rely=row3-2*bh, relwidth=col3 - col1 - bw/2, relheight=bh)
        # label entry and label
        card_label = tk.Label(self.master, text="card label")
        card_label.place(relx=col3, rely=row2, relwidth=bw, relheight=bh)
        self.label_text = tk.Text(self.master, bg='white', yscrollcommand=True)
        self.label_text.place(relx=col3, rely=row2+bh, relwidth=bw, relheight=row3- row2-2*bh)
        # positions of card on table entry and label
        table_pos_label = tk.Label(self.master, text="table position")
        table_pos_label.place(relx=col4, rely=row2, relwidth=bw, relheight=bh)
        self.table_pos_text = tk.Text(self.master, bg='white', yscrollcommand=True)
        self.table_pos_text.insert(tk.INSERT, self.initial_card_pos_sequency)
        self.table_pos_text.place(relx=col4, rely=row2+bh, relwidth=bw, relheight=row3- row2-2*bh)

        ################################ ROW 3 ################################
        # open file manager
        set_save_dir_but = tk.Button(self.master, text="select folder", command=self.navigateToSaveDir)
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

        ################################ ROW 4 ################################
        # previous image
        previous_image_but = tk.Button(self.master, text="previous image", command=partial(self.nextPrevImage, arg='previous_image') )
        previous_image_but.place(relx=col1, rely=row4, relwidth=bw, relheight=bh)
        # next image
        next_image_but = tk.Button(self.master, text="next image", command=partial(self.nextPrevImage, arg='next_image'))
        next_image_but.place(relx=col4, rely=row4, relwidth=bw, relheight=bh)

    def navigateToImage(self):
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

        # open the image in seperate window that allows drawing of points and zooming in/out
        MI = MarkImage(self.image_path.get())
        MI.openImage()

        # load image in image widget of gui
        w = self.image_wid.winfo_width()
        h = self.image_wid.winfo_height()
        imtk = MI.toTkImage(w, h)
        self.image_wid.image = imtk
        self.image_wid['image'] = imtk

        # create coordinate string and insert in text window
        text = ""
        for i, (x,y) in enumerate(MI.pixel_list,0):
            if i%4 ==0 and i!=0:
                text += '\n'
            pixel_str = "({},{}), ".format(x,y)
            text += pixel_str
        self.coordinate_text.insert(tk.INSERT,text) 

    def navigateToSaveDir(self):
        self.save_dir.set(askdirectory(parent=root, 
            initialdir=Path(__file__).parent.parent.parent, title='Choose save directory.'))

    def saveFile(self):
        # read lines of text boxes
        coordinates = self._read_coordinates(self.coordinate_text)
        labels = self._read_text_input(self.label_text)
        player_positions = self._read_text_input(self.table_pos_text)
        # construct dictionair
        dict_list = self.setDictionary(coordinates, labels, player_positions, self.image_path.get())
        # save to file
        self.writeToJsonFile( dict_list, os.path.join(self.save_dir.get(),self.save_file_name.get()) )
        # clear text widgets
        self._clearTextWidgets()

    def nextPrevImage(self, arg):
        # update image_path
        current_image_path = os.path.abspath(self.image_path.get())
        # find next/previous position of current path index in directory
        i = self.files_in_dir.index(current_image_path)
        if arg=='next_image':
            i+=1
        elif arg=='previous_image':
            i-=1
        # set new image path
        self.image_path.set(self.files_in_dir[i])
        # clear values
        self._clearTextWidgets()
        # open image
        self.openImage()

    def setDictionary(self, coordinate_cards, labels, player_positions, image_path):
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

    def writeToJsonFile(self, dict_list, file_path):
        try: 
            with open(file_path,'w') as out_file:
                json.dump(dict_list, out_file)
        except EnvironmentError:
            print("WHOOPS!\nOp een of andere duistere reden can er niet naar: \n{} geschreven worden"
                .format(file_path))

    def _listFilePathsInDir(self, dir_path):
        return [os.path.join(dir_path,file) for file in os.listdir(dir_path)]
    
    def _listFoldersInDir(self, top_dir):
        return [os.path.abspath(Dir[0]) for Dir in os.walk(top_dir)]

    def _read_text_input(self, text_widget):
        text = text_widget.get('1.0', tk.END).splitlines()
        return [line for line in text]
        # return [line.replace(",", "") for line in text]
    
    def _read_coordinates(self, text_widget):
        text = text_widget.get('1.0', tk.END).splitlines()
        coordinate_2Dlist = []
        for text_line in text:
            # convert to literal string of an list of tuples
            list_of_tuples_txt = "["+text_line+"]"
            list_of_tuples = ast.literal_eval(list_of_tuples_txt)
            coordinate_2Dlist.append(list_of_tuples)
        return coordinate_2Dlist

    def _getJsonFileName(self,image_path):
        image_file_name = os.path.basename(image_path)
        file_name = image_file_name.split('.')[0]
        json_file_name = file_name+'.json'
        return json_file_name
    
    def _clearTextWidgets(self):
        self.coordinate_text.delete('1.0',tk.END)
        self.label_text.delete('1.0',tk.END)
        # self.table_pos_text.delete('1.0',tk.END) # 
        self.image_wid.image=''

    # trace inputs using CB on entry/combobox to update variables instantaniously
    def _imagePathCB(self,*args):
        pass
        # print(self.image_path.get())
    def _saveDirCB(self,*args):
        pass
        # print(self.save_dir.get())
    def _saveFileNameCB(self,*args):
        pass
        # print(self.save_file_name.get())



if __name__ == "__main__":

    root = tk.Tk()
    GUI = AnnotateCardsGui(master=root)
    GUI.mainloop()
