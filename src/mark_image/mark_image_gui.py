import tkinter as tk

from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import filedialog, ttk, messagebox

from PIL import Image, ImageTk
from pathlib import Path
import os
import cv2
import numpy as np

 


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
            self.img = self.cach_imgs[-1].copy()
            self.cach_imgs.pop()
            self.pixel_list.pop()
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
        9. button: save info to file?  

        7. button: Next image in list
        8. button: previous image in list
    '''
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # variables
        self.corner_coordinates = tk.StringVar()
        self.image_path = tk.StringVar(value="C:/Users/Jasper/Desktop/counting_cards/data/backgrounds/bj_green_dark.jpg")
        self.files_in_dir = []# ["C:/Users/Jasper/Desktop/counting_cards/data/backgrounds/bj_green_dark.jpg"]

        self.save_dir = tk.StringVar(value="C:/Users/Jasper/Desktop/counting_cards/data/backgrounds")
        self.save_dir_options = self._listFoldersInDir("C:/Users/Jasper/Desktop/counting_cards/data")
        self.save_file_name = tk.StringVar(value='not yet generated')
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
        # positions entry and label
        coordinate_text = tk.Label(self.master, text="table position")
        coordinate_text.place(relx=col4, rely=row2, relwidth=bw, relheight=bh)
        self.label_text = tk.Text(self.master, bg='white', yscrollcommand=True)
        self.label_text.place(relx=col4, rely=row2+bh, relwidth=bw, relheight=row3- row2-2*bh)

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
        save_file_but = tk.Button(self.master, text="Save cards", command=self.saveFiles)
        save_file_but.place(relx=col4, rely=row3, relwidth=bw, relheight=bh)


    def setImagePath(self):
        self.image_path.set(askopenfilename(parent=root, 
            initialdir=Path(__file__).parent.parent.parent, title='Choose an image.'))
        # get list of file paths from same directory and update in self.files
        self.files_in_dir = self._listFilePathsInDir(Path(self.image_path.get()).parent)

    def setSaveDirectory(self):
        self.save_dir.set(askdirectory(parent=root, 
            initialdir=Path(__file__).parent.parent.parent, title='Choose save directory.'))

    def openImage(self):
        if not self.combo_file_path.get():
            messagebox.showerror("Error","Please select a file path")
            return 0
        if not os.path.isfile(self.combo_file_path.get()):
            messagebox.showerror("Error","Please select a correct file path")
            return 0

        # update paths in combobox such that all other files show in dropdown menue
        self.files_in_dir = self.updatePaths()

        # open the image using cv that allows drawing of points
        GPFI = GetPixelsFromImage(self.combo_file_path.get())
        GPFI.openImage()
        print(GPFI.pixel_list)
        # pathsOfAllFilesInDir(self.image_path)

        # create coordinate string and insert in text window
        text = ""
        for i, (x,y) in enumerate(GPFI.pixel_list,0):
            if i%4 ==0 and i!=0:
                text += '\n'
            pixel_str = "({},{}), ".format(x,y)
            text += pixel_str
        self.coordinate_text.insert(tk.INSERT,text) 

    def _listFoldersInDir(self, top_dir):
        return [Dir[0] for Dir in os.walk(top_dir)]

    def saveFiles(self):
        # Create function
        print('save files')

    def _listFilePathsInDir(self, dir_path):
        return [os.path.join(dir_path,file) for file in os.listdir(dir_path)]

    def _imagePathCB(self,*args):
        print(self.image_path.get())

    def _saveDirCB(self,*args):
        print(self.save_dir.get())

    def _saveFileNameCB(self,*args):
        print(self.save_file_name.get())


def setDictionair(pixel_list, labels, player_positions, image_path):
    length = len(pixel_list)
    card_corners = 4
    assert length%card_corners == 0

    n = 0
    coordinate_cards = [] # 2D list (x cards, 4 pixel tuples)
    # slice list after 4 pixels
    for i, pixel in enumerate(pixel_list,1):
        if i%card_corners == 0: # i is multiple of 4 
            coordinate_cards.append(pixel_list[n:i]) # slice list and create 2D list
            n+=card_corners

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
            'new_name': createName(label,pos,source_image_name)}
        info_cards.append(info_card.copy())

    print(info_cards)




if __name__ == "__main__":

    # # setDictionair Function
    # pixel_list = [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8)]
    # labels = ['As','7c']
    # image_path = 'image_path/ik.jpg'
    # player_positions = [1, 6]
    # setDictionair(pixel_list, labels, player_positions, image_path)

    root = tk.Tk()
    GUI = MarkImagesGui(master=root)
    GUI.mainloop()

    # launch app
        # select folder + image
        # open image
            # clickclcik
            # close image
        # Fill in card labels
        # save pixels, card label
            # store in dict with info
        # open next image



    # GPFI = GetPixelsFromImage()
    # GPFI.GetPixelsFromImage()

    # print(GPFI.pixel_list)


