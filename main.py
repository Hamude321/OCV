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
import win32gui, win32ui, win32con
import pygetwindow as gw
from pygame import mixer
import os

    
def main():
    window = ttk.Window(themename='darkly')
    window1 = User_Interface(window,'Detection', '1920x1080')
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
    mixer.init()
    current_path = os.path.dirname(os.path.abspath(__file__))
    sound = mixer.Sound(current_path+'\\'+'assets\\sound\\ding.mp3')
    
    #initialize window
    def __init__(self, window, title, geometry):

        self.window = window
        self.window.title(title)
        self.window.geometry(geometry)

        #frame
        self.video_frame=ttk.Frame(master=self.window, borderwidth=2, relief=tk.RIDGE)
        self.video_frame.place(x=0, y=0, relwidth=1, relheight=0.7)

        self.option_frame=ttk.Frame(master=self.window, borderwidth=2, relief=tk.RIDGE)
        self.option_frame.place(x=0, rely=0.7, relheight=0.3, relwidth=1)
        #ttk.Label(self.option_frame, background='yellow').pack(expand=True, fill='both')
        self.option_frame.columnconfigure((0,1), weight=1)

        self.input_frame = ttk.Frame(self.option_frame, borderwidth=2, relief=tk.RIDGE)
        #self.input_frame.place(x=0, rely=0.7, relheight=0.3, relwidth=0.6)
        #self.input_frame.pack(expand=True)
        self.input_frame.grid(column=0, sticky='nsew')
        self.input_frame.columnconfigure((0,1,2), weight=1)
        self.input_frame.rowconfigure((0,1,2,3,4,5,6), weight=1)
        self.toggle_frame=ttk.Frame(master=self.input_frame)
        # self.toggle_frame.grid(column=0, row=6)
        # ttk.Label(self.toggle_frame, background='yellow').pack(expand=True, fill='both')



        #label
        self.video_label = ttk.Label(master=self.video_frame)
        self.video_label.pack(side='top', expand=True, fill='both')

        self.threshold_string= tk.StringVar()
        threshold_label = ttk.Label(master=self.input_frame, font = 'Calibri 24 bold', textvariable=self.threshold_string)
        threshold_label.grid(column=2, row=3, sticky='nsw')

        self.core_fps_string = tk.StringVar()
        self.core_fps_string.set('Core: 0')
        self.core_fps_label = ttk.Label(master=self.input_frame, textvariable=self.core_fps_string)
        self.core_fps_label.grid(column=2, row=5, sticky='nse')

        self.detection_fps_string = tk.StringVar()
        self.detection_fps_string.set('Detection: 0')
        self.detection_fps_label = ttk.Label(master=self.input_frame, textvariable=self.detection_fps_string)
        self.detection_fps_label.grid(column=2, row=6, sticky='nse')

        self.x1y1_string = tk.StringVar()
        self.x1y1_string.set('x: y:')
        self.x1y1_label = ttk.Label(master =self.input_frame,textvariable=self.x1y1_string)
        self.x1y1_label.grid(column=1, row=5, sticky='nsw')

        self.x2y2_string = tk.StringVar()
        self.x2y2_string.set('x: y:')
        x2y2_label = ttk.Label(master= self.input_frame, textvariable=self.x2y2_string)
        x2y2_label.grid(column=1, row=6, sticky='nsw')

        #button
        self.button_start = ttk.Button(master=self.input_frame, text='Start', state=DISABLED)
        self.button_start.grid(column=1, row=0, pady=10, sticky='nsw', ipadx=20)

        self.button_stop = ttk.Button(master = self.input_frame, text='Stop', state= DISABLED)
        self.button_stop.grid(column=1, row=1, sticky='nsw', ipadx=20)

        self.button_load_img = ttk.Button(master = self.input_frame, text='Load Image', state=DISABLED)
        self.button_load_img.grid(column=1, row=3, sticky='nsw', pady=10)

        self.button_window_selection = ttk.Button(master = self.input_frame, text='Select Frame')
        self.button_window_selection.grid(column=1, row=4, sticky='nsw')

        self.button_refresh_list = ttk.Button(master = self.input_frame, text='Refresh')
        self.button_refresh_list.grid(column=0, row=6)

        #scale
        self.threshold_scale = ttk.Scale(master=self.input_frame, value=30, from_=30, to=100)
        self.threshold_scale.grid(column=2, row=2, sticky='nswe')

        #list
        self.list = Listbox(master=self.input_frame, width=50, height=10)
        self.list.grid(column=0, row=0, rowspan=6, sticky='nwes', padx=10, pady=10)
        self.titles = self.get_titles()
        for title in self.titles:
            self.list.insert(0, title)
            
        #events
        #self.button_start.bind('<ButtonRelease-1>', self.start_thread)
        #self.button_stop.bind('<ButtonRelease-1>', self.stop_bot)
        self.list.bind('<<ListboxSelect>>', self.onselect)   
        #self.button_load_img.bind('<ButtonRelease-1>', self.load_img)  
        self.threshold_scale.bind('<B1-Motion>', self.threshold)    
        self.button_window_selection.bind('<ButtonRelease-1>', self.start_selection)
        self.button_refresh_list.bind('<ButtonRelease-1>', self.refresh_list)


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

        #enable/disable widgets
        if not self.is_running:        
            self.button_start.config(state=NORMAL) 
            self.button_start.bind('<ButtonRelease-1>', self.start_thread) 
        
    def stop_bot(self, event):
        self.recorded_coords = np.zeros((2,2), dtype=int)
        self.x1y1_string.set('x: y:')
        self.x2y2_string.set('x: y:')
        if self.is_running:
            self.core.close_window()
            self.is_running = False

        #enable/disable widgets
        self.button_window_selection.config(state=NORMAL)
        self.button_window_selection.bind('<ButtonRelease-1>', self.start_selection)
        self.list.config(state=DISABLED)
        self.list.unbind('<<ListboxSelect>>')
        self.button_start.config(state=DISABLED)
        self.button_start.unbind('<ButtonRelease-1>')
        self.button_load_img.config(state=DISABLED)
        self.button_load_img.unbind('<ButtonRelease-1>')  
        self.list.config(state=NORMAL)
        self.list.bind('<<ListboxSelect>>', self.onselect)
        self.button_stop.config(state=DISABLED)
        self.button_stop.unbind('<ButtonRelease-1>')

    def start_selection(self,event):
            chosen_window = None
            if self.selected_item:
                chosen_window = gw.getWindowsWithTitle(self.selected_item)

            if chosen_window:
                chosen_window = chosen_window[0]
                chosen_window.activate()
                sleep(2)
                self.recorded_coords[0,0], self.recorded_coords[0,1] = pyautogui.position()
                top_left=self.recorded_coords[0,0], self.recorded_coords[0,1]
                self.x1y1_string.set('x: {} y: {}'.format(top_left[0], top_left[1]))
                self.sound.play()
                print(top_left)

                sleep(2)
                self.recorded_coords[1,0], self.recorded_coords[1,1] = pyautogui.position()
                bottom_right=self.recorded_coords[1,0], self.recorded_coords[1,1]
                self.x2y2_string.set('x: {} y: {}'.format(bottom_right[0], bottom_right[1]))
                self.sound.play()
                print(bottom_right)
                self.start_thread(self)
        
    def start_thread(self, event):
        if self.is_running is False:
            self.core = Running(self.selected_item, self.recorded_coords)
            self.t1 = threading.Thread(target=self.core.runstuff)
            self.t1.start()
            sleep(1)            
            self.is_running = True  
            if self.i <1:
                self.show_video()
                self.i+=1            

            #enable/disable widgets
            self.list.selection_clear(0, END)
            self.list.config(state=DISABLED)
            self.list.unbind('<<ListboxSelect>>')  
            self.button_start.config(state=DISABLED)
            self.button_start.unbind('<ButtonRelease-1>')
            self.button_stop.config(state=NORMAL)
            self.button_stop.bind('<ButtonRelease-1>', self.stop_bot)
            self.button_load_img.config(state=NORMAL)     
            self.button_load_img.bind('<ButtonRelease-1>', self.load_img)
            self.button_window_selection.config(state=DISABLED)
            self.button_window_selection.unbind('<ButtonRelease-1>')


    def show_video(self):
        self.display()
        
        #enable/disable widgets
        self.button_load_img.config(state=NORMAL)     
        self.button_load_img.bind('<ButtonRelease-1>', self.load_img)  
           

    def display(self):
        if not self.core.detection_img is None:
            img = self.core.get_detection_img()
            self.to_pil(img, self.video_label, 0, 0)
            self.core_fps_string.set('Core: {}'.format(self.core.get_core_fps()))
            self.detection_fps_string.set('Detection: {}'.format(self.core.detector.get_detection_fps()))
            self.video_label.after(10, self.display)
        else:
            img = None

    def to_pil(self, img, label, x,y):
        w = self.video_frame.winfo_width()- 2*x
        h = self.video_frame.winfo_height()- 2*y
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
        file = filedialog.askopenfilename(initialdir= "assets\\pics\\", filetypes= [("Image file", (".jpg"))])
        if len(file)>0:
            self.core.vision.update_needle_img_path(file)
            
    def get_titles(self):
        self.titles = []
        for x in pyautogui.getAllWindows():  
            if len(x.title)>0:
                self.titles.append(x.title)
        print(self.titles)
        return self.titles
    
    def refresh_list(self, event):
        self.titles = []
        self.list.delete(0, END)
        for x in pyautogui.getAllWindows():  
            if len(x.title)>0:
                self.titles.append(x.title)
        for title in self.titles:
                    self.list.insert(0, title)           


main()


# light

#     cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti
# dark

#     cyborg - darkly - solar - superhero