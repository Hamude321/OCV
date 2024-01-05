import tkinter as tk
from tkinter import *
from tkinter import filedialog
#from tkinter import ttk
import ttkbootstrap as ttk
import pyautogui
from windowcapture import WindowCapture
from core import Running
import cv2 as cv
from PIL import Image, ImageTk
from detection import Detection
from time import sleep
import threading
import numpy as np

    
def main():
    window = ttk.Window(themename='darkly')
    window1 = User_Interface(window,'Detection Bot', '1920x1080')
    return None
    

class User_Interface:

    #variables
    is_running = False
    core = None
    t1 = None
    recorded_coords = np.zeros((2,2), dtype=int)
    is_showing = False
    selected_item=None
    i=0
    
    #initialize window
    def __init__(self, window, title, geometry):

        self.window = window
        self.window.title(title)
        self.window.geometry(geometry)

        #frame
        input_frame = ttk.Frame(master=self.window, borderwidth=2, relief=tk.RIDGE)
        input_frame.pack(side='bottom')

        button_frame_1 = ttk.Frame(master=input_frame)
        button_frame_1.pack(side='right')

        button_frame_2 = ttk.Frame(master=input_frame)
        button_frame_2.pack(side='right', padx=10)

        #label
        self.title_label = ttk.Label(master=self.window, text = 'Test')
        self.title_label.pack(side='top')

        self.threshold_string= tk.StringVar()
        threshold_label = ttk.Label(master=input_frame, textvariable=self.threshold_string)
        threshold_label.pack()

        #button
        self.button_start = ttk.Button(master=button_frame_1, text='Start', state=DISABLED)
        self.button_start.pack(side ='right', padx=5)

        self.button_stop = ttk.Button(master = button_frame_1, text='Stop', state= DISABLED)
        self.button_stop.pack(side='right')

        self.button_load_img = ttk.Button(master = button_frame_2, text='Load Image', state=DISABLED)
        self.button_load_img.pack(side='right', padx=5)

        self.button_show = ttk.Button(master=button_frame_1, text='Show', state=DISABLED)
        self.button_show.pack()

        button_window_selection = ttk.Button(master =button_frame_2, text='Select Frame')
        button_window_selection.pack(side='right', padx=5)

        #scale
        self.threshold_scale = ttk.Scale(master=input_frame, value=30, from_=30, to=100, length=500)
        self.threshold_scale.pack()

        #output
        output_string = tk.StringVar()
        output_label = ttk.Label(master=input_frame, text='Output', font = 'Calibri 24 bold', textvariable=output_string)
        output_label.pack()

        self.x1y1_string = tk.StringVar()
        x1y1_label = ttk.Label(master =button_frame_2,textvariable=self.x1y1_string)
        x1y1_label.pack(side='top')

        self.x2y2_string = tk.StringVar()
        x2y2_label = ttk.Label(master= button_frame_2, textvariable=self.x2y2_string)
        x2y2_label.pack(side='bottom')

        #list
        self.list = Listbox(master=input_frame, width=50, height=10)
        self.list.pack(side='left')
        titles = self.get_titles()
        for title in titles:
            self.list.insert(0, title)
            
        #events
        #self.button_start.bind('<ButtonRelease-1>', self.start_thread)
        #self.button_show.bind('<ButtonRelease-1>', self.show_video)
        #self.button_stop.bind('<ButtonRelease-1>', self.stop_bot)
        self.list.bind('<<ListboxSelect>>', self.onselect)   
        #self.button_load_img.bind('<ButtonRelease-1>', self.load_img)  
        self.threshold_scale.bind('<B1-Motion>', self.threshold)    
        button_window_selection.bind('<ButtonRelease-1>', self.start_selection)


       #input
        # entry_int = tk.IntVar(value=7)
        # entry = ttk.Entry(master=input_frame, textvariable=entry_int)
        # entry.pack(side ='left', padx=10)
        
        #run(always at the end)
        self.window.mainloop()



    #methods   
    def onselect(self, event):
        w = event.widget
        idx = int(w.curselection()[0])
        self.selected_item = w.get(idx)
        if not self.is_running:        
            self.button_start.config(state=NORMAL) 
            self.button_start.bind('<ButtonRelease-1>', self.start_thread) 
        print(self.selected_item)
        
    def stop_bot(self, event):
        self.recorded_coords = np.zeros((2,2), dtype=int)
        if self.is_running:
            self.core.close_window()
            self.is_running = False
        self.list.config(state=DISABLED)
        self.list.unbind('<<ListboxSelect>>')
        self.button_start.config(state=DISABLED)
        self.button_start.unbind('<ButtonRelease-1>')
        self.button_load_img.config(state=DISABLED)
        self.button_load_img.unbind('<ButtonRelease-1>')  
        self.button_show.config(state=DISABLED)
        self.button_show.unbind('<ButtonRelease-1>')
        self.list.config(state=NORMAL)
        self.list.bind('<<ListboxSelect>>', self.onselect)
        self.button_stop.config(state=DISABLED)
        self.button_stop.unbind('<ButtonRelease-1>')
        # sleep(1)

    def start_selection(self,event):
            #if x1,y1=0....else if else
            sleep(2)
            self.recorded_coords[0,0], self.recorded_coords[0,1] = pyautogui.position()
            top_left=self.recorded_coords[0,0], self.recorded_coords[0,1]
            self.x1y1_string.set(top_left)
            print(top_left)
            sleep(2)

            self.recorded_coords[1,0], self.recorded_coords[1,1] = pyautogui.position()
            bottom_right=self.recorded_coords[1,0], self.recorded_coords[1,1]
            self.x2y2_string.set(bottom_right)
            print(bottom_right)
    
    def start_thread(self, event):
        if self.is_running is False:
            self.core = Running(self.selected_item, self.recorded_coords)
            self.t1 = threading.Thread(target=self.core.runstuff)
            self.t1.start()
            sleep(1)
            self.is_running = True  
            self.list.selection_clear(0, END)
            self.list.config(state=DISABLED)
            self.list.unbind('<<ListboxSelect>>')  
            self.button_start.config(state=DISABLED)
            self.button_start.unbind('<ButtonRelease-1>')
            self.button_stop.config(state=NORMAL)
            self.button_stop.bind('<ButtonRelease-1>', self.stop_bot)
            self.button_load_img.config(state=NORMAL)     
            self.button_load_img.bind('<ButtonRelease-1>', self.load_img)
            if self.i <1:
                self.button_show.config(state=NORMAL)
                self.button_show.bind('<ButtonRelease-1>', self.show_video)
                self.i+=1

    def show_video(self, event):
        self.display()
        self.button_load_img.config(state=NORMAL)     
        self.button_load_img.bind('<ButtonRelease-1>', self.load_img)  
        self.button_show.config(state=DISABLED) 
        self.button_show.unbind('<ButtonRelease-1>')             

    def display(self):
        if not self.core.detection_img is None:
            img = self.core.get_detection_img()
            self.to_pil(img, self.title_label, 50, 20, 1830, 800)
            self.title_label.after(10, self.display)
        else:
            img = None

    def to_pil(self, img, label, x,y,w,h):
        img = cv.resize(img,(w,h))
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        pic = ImageTk.PhotoImage(image)
        label.configure(image = pic)
        label.image = pic
        label.place(x=x, y=y)

    def threshold(self, event):
        threshold=int((self.threshold_scale.get()))/100
        self.threshold_string.set(threshold) 
        if not self.core is None:
            self.core.detector.update_threshold(threshold)

    def load_img(self,event):
        file = filedialog.askopenfilename(initialdir= "assets\\", filetypes= [("Image file", (".jpg"))])
        if len(file)>0:
            self.core.vision.update_needle_img_path(file)
            


    def get_titles(self):
        titles = []
        for x in pyautogui.getAllWindows():  
            if len(x.title)>0:
                titles.append(x.title)
        print(titles)
        return titles


main()


# light

#     cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti
# dark

#     cyborg - darkly - solar - superhero