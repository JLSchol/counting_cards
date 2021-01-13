import os
from PIL import Image, ImageTk
import cv2
import numpy as np

class MarkImage(object):
    """ - Opens an image in an OpenCV window. 
        - Registers a mouse listener so that:
            1. left-clicking marks the pixel and shows the value
            2. right-clicking goes back to previous image (similar as in ctrl+z)
            3. right-dragging up/down zooms in/out 
        - Allows to save image to tkinter image"""
    def __init__(self, IMAGE_PATH = None, WINDOW_NAME = 'mark image'):
        self.WINDOW_NAME = WINDOW_NAME
        self.IMAGE_PATH = IMAGE_PATH
        self.img = cv2.imread(self.IMAGE_PATH,cv2.IMREAD_ANYCOLOR)
        self.panAndZoomState = PanAndZoomState(self.img.shape, self)
        self.mButtonDownLoc = None
        self.cach_imgs = [self.img.copy()]
        self.pixel_list = []

        cv2.namedWindow(self.WINDOW_NAME, cv2.WINDOW_NORMAL)
        self.redrawImage()
        cv2.setMouseCallback(self.WINDOW_NAME, self.onMouse)

    def openImage(self):
        key = -1
        while key != ord('q') and key != 27: # 27 = escape key
            #the OpenCV window won't display until you call cv2.waitKey()
            if (cv2.getWindowProperty(self.WINDOW_NAME, 0) == -1):
                break
            key = cv2.waitKey(5) #User can press 'q' or ESC to exit.
        cv2.destroyAllWindows()

    def onMouse(self,event, x,y,_ignore1,_ignore2):
        """ Responds to mouse events within the window. 
        The x and y are pixel coordinates in the image currently being displayed.
        If the user has zoomed in, the image being displayed is a sub-region, so you'll need to
        add self.panAndZoomState.ul to get the coordinates in the full image."""
        if event == cv2.EVENT_MOUSEMOVE:
            return
        elif event == cv2.EVENT_RBUTTONDOWN:
            #record where the user started to right-drag
            self.mButtonDownLoc = np.array([y,x])
        elif event == cv2.EVENT_RBUTTONUP and self.mButtonDownLoc is not None:
            # the user just finished right-dragging of finished right click
            dy = y - self.mButtonDownLoc[0]
            pixelsPerDoubling = 0.2*self.panAndZoomState.shape[0] #lower = zoom more
            changeFactor = (1.0+abs(dy)/pixelsPerDoubling)
            changeFactor = min(max(1.0,changeFactor),5.0)
            if changeFactor < 1.05: #this was a click, not a draw. -> go to previous image.
                dy = 0 
                # go to previous image and remove coordinates
                if self.cach_imgs and self.pixel_list:
                    self.img = self.cach_imgs[-1]
                    self.pixel_list.pop()
                    self.cach_imgs.pop()
                    self.redrawImage()

            if dy > 0: #moved down, so zoom out.
                zoomInFactor = 1.0/changeFactor
            else:
                zoomInFactor = changeFactor
            self.panAndZoomState.zoom(self.mButtonDownLoc[0], self.mButtonDownLoc[1], zoomInFactor)
        elif event == cv2.EVENT_LBUTTONDOWN:
            #If the user pressed the left button draw circle and show pixel values
            coordsInDisplayedImage = np.array([y,x])
            if np.any(coordsInDisplayedImage < 0) or np.any(coordsInDisplayedImage > self.panAndZoomState.shape[:2]):
                print("you clicked outside the image area")
            else:
                coordsInFullImage = self.panAndZoomState.ul + coordsInDisplayedImage
                self.cach_imgs.append(self.img.copy())
                self.pixel_list.append((coordsInFullImage[1],coordsInFullImage[0])) # note the x,y swap!
                self.drawPoint(self.img,coordsInFullImage)

    def drawPoint(self, image, coord): 
        (y,x) = coord
        cv2.circle(image, (x,y), 1, (0,0,255), thickness=2)
        cv2.putText(image, "%d,%d" % (x, y), (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (140, 15, 10), thickness=1)
        self.redrawImage()

    def toTkImage(self, w, h):
        b,g,r = cv2.split(self.img)
        img = cv2.merge((r,g,b))
        imgtk = Image.fromarray(img)
        imgtk = imgtk.resize((w, h), Image.ANTIALIAS)        
        imgtk = ImageTk.PhotoImage(imgtk)
        return imgtk

    def redrawImage(self):
        pzs = self.panAndZoomState
        cv2.imshow(self.WINDOW_NAME, self.img[pzs.ul[0]:pzs.ul[0]+pzs.shape[0], pzs.ul[1]:pzs.ul[1]+pzs.shape[1]])

class PanAndZoomState(object):
    """ Tracks the currently-shown rectangle of the image.
    Does the math to adjust this rectangle to pan and zoom."""
    MIN_SHAPE = np.array([50,50])
    def __init__(self, imShape, parentWindow):
        self.ul = np.array([0,0]) #upper left of the zoomed rectangle (expressed as y,x)
        self.imShape = np.array(imShape[0:2])
        self.shape = self.imShape #current dimensions of rectangle
        self.parentWindow = parentWindow
    def zoom(self,relativeCy,relativeCx,zoomInFactor):
        self.shape = (self.shape.astype(np.float)/zoomInFactor).astype(np.int)
        #expands the view to a square shape if possible. (I don't know how to get the acqtual window aspect ratio)
        self.shape[:] = np.max(self.shape) 
        self.shape = np.maximum(PanAndZoomState.MIN_SHAPE,self.shape) #prevent zooming in too far
        c = self.ul+np.array([relativeCy,relativeCx])
        self.ul = (c-self.shape/2).astype(np.int)
        self._fixBoundsAndDraw()
    def _fixBoundsAndDraw(self):
        """ Ensures we didn't zoom outside the image. 
        Then draws the currently-shown rectangle of the image."""
        self.ul = np.maximum(0,np.minimum(self.ul, self.imShape-self.shape))
        self.shape = np.minimum(np.maximum(PanAndZoomState.MIN_SHAPE,self.shape), self.imShape-self.ul)
        self.parentWindow.redrawImage()


if __name__ == "__main__":
    infile = "C:\\Users\\Jasper\\Desktop\\counting_cards\\data\\raw_data\\singles1.jpg"
    MI = MarkImage(infile, "mark cards")
    MI.openImage()
    print(MI.pixel_list)










