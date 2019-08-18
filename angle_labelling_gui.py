import PySimpleGUI as sg
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from PIL import ImageTk, Image,ImageFilter
import os
import math
import cv2
from os import listdir
from os.path import isfile, join
import numpy as np
from itertools import cycle
import json

def writeToJSONFile(path, fileName, data):
    filePathNameWExt =  path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

class GUI:
    def move(self,event):
        if event.char == "a":
            self.canvas.move(self.img_id, -10, 0)
        elif event.char == "d":
            self.canvas.move(self.img_id, 10, 0)
        elif event.char == "w":
            self.canvas.move(self.img_id, 0, -10)
        elif event.char == "s":
            self.canvas.move(self.img_id, 0, 10)

    def resetZoom(self):
        self.canvas_image = ImageTk.PhotoImage(self.curIt)
        self.moveIM = self.canvas.create_image(self.w/2, self.h/2-100, image=self.canvas_image, anchor="center")
        self.zoomed = False
        self.scale = 1
    def zoomOut(self):
        self.scale *= float(2)/3
        self.redraw(self.x, self.y)
    def zoomIn(self):
        self.scale *= 1.5
        self.redraw(self.x, self.y)

    def redraw(self, x=0, y=0):
        if self.img_id:
            self.canvas.delete(self.img_id)
        self.zX = x
        self.zY = y
        print(self.curIt.size)
        self.iw, self.ih = self.curIt.size
        size = int(self.iw * self.scale), int(self.ih * self.scale)
        self.initial_im = self.canvas_image
        self.canvas_image = ImageTk.PhotoImage(self.curIt.resize(size),Image.ANTIALIAS)
        print(size)
        self.canvas.delete(ALL)
        self.img_id = self.canvas.create_image(self.w/2, self.h/2-100, image=self.canvas_image, anchor = "center")
        self.zoomed = True
        self.canvas.old_coords = None

    def leftClick(self,event):
        self.x,self.y = event.x, event.y
        if self.canvas.old_coords:
            
            self.x1, self.y1 = self.canvas.old_coords
            self.canvas.create_line(self.x, self.y, self.x1, self.y1, width = 2)
            self.canvas.old_coords = None
            if self.x == self.x1:
                if self.y1 < self.y:
                    degree = 90
                else:
                    degree = 270
            elif self.y == self.y1:
                if self.x1 < self.x:
                    degree = 0
                else:
                    degree = 0
            else:
                slope = -(self.y1-self.y)/(self.x1-self.x)
                degree = math.degrees(math.atan(slope))
                degree = round(degree)
                if self.y < self.y1:
                    if degree < 0:
                        degree = 180 + degree
                else:
                    if degree < 0:
                        degree = 360 + degree
                    else:
                        degree = 180 + degree    
            if degree == 360:
                degree = 0
            
            
            self.angle = str(degree)
            self.label.config(text=self.angle)
            print(degree)
            
        else:
            self.canvas.old_coords = self.x, self.y
            #self.button2Click()
    

    def buttonClick(self):
        
        if (self.angle == None):
            answer  = messagebox.askyesnocancel("Skip the Image","Any angle has not chosen yet, do you want to skip the image?")
            if answer == True:
                self.curName=next(self.iteratorName)
                if self.data[self.curName] == False:
                    self.canvas.delete(ALL)
                    self.curIt = next(self.iterator)
                    self.canvas_image = ImageTk.PhotoImage(self.curIt)
                    self.moveIM = self.canvas.create_image(self.w/2, self.h/2-100, image=self.canvas_image, anchor="center")
                    self.zoomed = False
                    self.scale = 1
                    self.angle = None
                else:
                    messagebox.showinfo("Quit","No Image Left")
                    self.window.destroy()
        else:
            self.f.write(self.curName +","+ self.angle + "\n")
            self.angle = None
            self.label.config(text=self.angle)
            self.data[self.curName] = True
            writeToJSONFile(self.direc,'file-name',self.data)
            self.curName=next(self.iteratorName)
    
            
            if self.data[self.curName] == False:
                self.canvas.delete(ALL)
                self.curIt = next(self.iterator)
                self.canvas_image = ImageTk.PhotoImage(self.curIt)
                self.moveIM = self.canvas.create_image(self.w/2, self.h/2-100, image=self.canvas_image, anchor="center")
                self.zoomed = False
                self.scale = 1
                
                
            else:
                 messagebox.showinfo("Quit","No Image Left")
                 self.window.destroy()

    def __init__(self):
        
        self.window = Tk()
        self.window.withdraw()
        self.direc = simpledialog.askstring("Directory","Please enter the directory",initialvalue="C:/Users/cagri/OneDrive/Desktop/Yedek/py/all/set")
        
        self.window.title("Angle Calculator")
        self.w, self.h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d+0+0" % (self.w, self.h-70))
  
        self.window.configure(background='grey')
        self.initial_im = None
        self.zX = None
        self.zY = None
        self.zoomed = False
        self.iw = None
        self.ih = None
        self.scale = 1
        self.img_id = None
        self.img = None
        self.x = None
        self.y = None
        self.x1 = None
        self.y1 = None
        self.images = []
        self._drag_data1 = {"x": 0, "y": 0, "item1": None}
        try:
            r = open(self.direc + "/" + 'Name-Angle.txt',mode='r') 
            alltxt = r.read()
            r.close()
        except:
            alltxt = ""
        self.f = open(self.direc + "/" +'Name-Angle.txt', 'w')
        self.f.write(alltxt)
        dirs = os.listdir( self.direc )
        
        try:
            filePathNameWExt =  self.direc + '/' + 'file-name' + '.json'
            with open(filePathNameWExt, "r") as read_file:
                self.data = json.load(read_file)
        except:
            print("Not Found")
            self.data = {}
        
        print(self.data)
        # resize image
        names = []
        for file in dirs:  
            #st = file.find(".jpg" ) is not -1) or (file.find(".JPG" ) is not -1) or (file.find(".bmp" ) is not -1) or (file.find(".BMP" ) is not -1)
            #st = (file.find(".bmp" ) is not -1) or (file.find(".BMP" ) is not -1)# or (file.find(".j" ) is not -1) or (file.find(".BMP" ) is not -1)
            if (file.find(".bmp" ) is not -1) or (file.find(".BMP" ) is not -1):
                file = file.replace(".bmp","")
                file = file.replace(".BMP","")
                
                if (file in self.data):
                    if (self.data[file] == False):
                        im = cv2.cvtColor(cv2.imread(self.direc+"/"+file+".bmp"), cv2.COLOR_BGR2RGB)
                        im = Image.fromarray(im)                   
                        names.append(file)
                        self.images.append(im)
                else:  
                    im = cv2.imread(self.direc+"/"+file+".bmp")
                    im = Image.fromarray(im)
                    names.append(file)
                    self.images.append(im)
                    self.data[file] = False
            elif (file.find(".jpg" ) is not -1) or (file.find(".JPG" ) is not -1):
                file = file.replace(".jpg","")
                file = file.replace(".JPG","")
                print(self.direc+"/"+file+".jpg")
                if (file in self.data):
                    if (self.data[file] == False):
                        im = cv2.cvtColor(cv2.imread(self.direc+"/"+file+".jpg"), cv2.COLOR_BGR2RGB)
                        im = Image.fromarray(im)                   
                        names.append(file)
                        self.images.append(im)
                else:  
                    #im = cv2.imread("1.jpg")
                    im = cv2.imread(self.direc+"/"+file+".jpg")
                    print(type(im))
                    im = Image.fromarray(im)
                    names.append(file)
                    self.images.append(im)
                    self.data[file] = False
        self.iterator = cycle(self.images)
        self.iteratorName = cycle(names)
        
        try:
            self.curName = next(self.iteratorName)
        except:
            messagebox.showinfo("Quit","No JPG Image Found")
            self.window.quit()
        self.curIt = next(self.iterator)
        self.img = ImageTk.PhotoImage(self.curIt)
        self.canvas_image = self.img
        writeToJSONFile(self.direc,'file-name',self.data)
        Button(text="Next Image",command=self.buttonClick).pack(side = "bottom", fill = "both", expand = "no")
        Button(text="Zoom In",command=self.zoomIn).pack(side = "bottom", fill = "both", expand = "no")
        Button(text="Zoom Out",command=self.zoomOut).pack(side = "bottom", fill = "both", expand = "no")
        Button(text="Reset Zoom",command=self.resetZoom).pack(side = "bottom", fill = "both", expand = "no")
        self.angle = None
        self.label = Label(text = self.angle)
        self.label.pack(side = "bottom", fill = "both", expand = "no")

        self.canvas = Canvas(width=self.w, height=self.h)  
        self.canvas.pack(expand=YES, fill=BOTH)  
        self.canvas.old_coords = None
        self.canvas_image = self.img
        self.moveIM = self.canvas.create_image(self.w/2, self.h/2-100, image=self.img, anchor="center")
        self.canvas.bind("<Button-1>",self.leftClick)
        self.window.bind("<Key>", self.move)
        self.move_flag = False
        self.mouse_xpos = self.w/2
        self.mouse_ypos = self.h/2-100
        self.window.deiconify()
        self.window.mainloop()
def main():
    GUI()
if __name__ == "__main__":
     main()