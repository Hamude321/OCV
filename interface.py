import threading
import tkinter as tk
from tkinter import *
from tkinter import filedialog
#from tkinter import ttk
import ttkbootstrap as ttk
import pyautogui
from windowcapture import WindowCapture
from main import Running
import cv2 as cv
from PIL import Image, ImageTk
from detection import Detection
from time import sleep


#mainf = Running(None)
is_running = False
mainf = None

def get_titles():
    titles = []
    for x in pyautogui.getAllWindows():  
        if len(x.title)>0:
            titles.append(x.title)
    print(titles)
    return titles

#functions here i guess
def show_video():
    display()

def onselect(event):
    global is_running
    global mainf
    global t1
    if is_running is False:
        w = event.widget
        idx = int(w.curselection()[0])
        value = w.get(idx)
        mainf = Running(value, mouse_x1, mouse_x2,mouse_y1,mouse_y2)
        t1 = threading.Thread(target=mainf.runstuff)
        t1.start()
        #mainf.wincap.update(value)
        #mainf.run()
        #display(mainf.detection_img)
        is_running = True
    
def stop_bot(event):
    global is_running
    global mainf
    global mouse_x1, mouse_x2,mouse_y1,mouse_y2
    mouse_x1, mouse_x2,mouse_y1,mouse_y2 = 0
    print(is_running)
    if is_running:
        mainf.close_window()
        is_running = False
        

def to_pil(img, label, x,y,w,h):
    img = cv.resize(img,(w,h))
    #img = cv.flip(img,1)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    pic = ImageTk.PhotoImage(image)
    label.configure(image = pic)
    label.image = pic
    label.place(x=x, y=y)

def display():
    if not mainf.detection_img is None:
        img = mainf.get_detection_img()
        to_pil(img, title_label, 50, 20, 1830, 800)
        title_label.after(10, display)
    else:
        img = None

def threshold(event):
    threshold=int((threshold_scale.get()))/100
    threshold_string.set(threshold) 
    if not mainf is None:
        mainf.detector.update_threshold(threshold)

def load_img(event):
    file = filedialog.askopenfilename(initialdir= "assets/", filetypes= [("Image file", (".jpg"))])
    mainf.vision.update_needle_img_path(file)


def start_selection(event):
        # global x0,y0
        # eventorigin.x0 = eventorigin.x
        # eventorigin.y0 = eventorigin.y
        # print(x0, y0)
        global mouse_x1, mouse_y1
        global mouse_x2, mouse_y2
        sleep(2)
        mouse_x1, mouse_y1 = pyautogui.position()
        a=mouse_x1, mouse_y1
        x1y1_string.set(a)
        print(a)
        sleep(2)
        mouse_x2, mouse_y2 = pyautogui.position()
        b=mouse_x2, mouse_y2
        x2y2_string.set(b)
        print(b)
        #mainf.wincap.update(mouse_x1,mouse_y1,mouse_x2,mouse_y2)

    


#window
window = ttk.Window(themename='darkly')
window.title('Detection Bot')
window.geometry('1920x1080')

#frame
input_frame = ttk.Frame(master=window)
input_frame.pack(side='bottom')

button_frame_1 = ttk.Frame(master=input_frame)
button_frame_1.pack(side='right')

button_frame_2 = ttk.Frame(master=input_frame)
button_frame_2.pack(side='right', padx=10)

#label
title_label = ttk.Label(master=window, text = 'Test')
title_label.pack(side='top')

threshold_string= tk.StringVar()
threshold_label = ttk.Label(master=input_frame, textvariable=threshold_string)
threshold_label.pack()


#input
entry_int = tk.IntVar(value=7)
entry = ttk.Entry(master=input_frame, textvariable=entry_int)
#entry.pack(side ='left', padx=10)

#button
button_show = ttk.Button(master=button_frame_1, text='Show', command=show_video)
button_show.pack(side ='right', padx=5)

button_stop = ttk.Button(master = button_frame_1, text='Stop')
button_stop.pack(side='right')

button_load_img = ttk.Button(master = button_frame_2, text='Load Image')
button_load_img.pack(side='right', padx=5)

button_window_selection = ttk.Button(master =button_frame_2, text='Select Frame')
button_window_selection.pack(side='right', padx=5)

#scale
threshold_scale = ttk.Scale(master=input_frame, value=30, from_=30, to=100, length=500)
threshold_scale.pack()

#output
output_string = tk.StringVar()
output_label = ttk.Label(master=input_frame, text='Output', font = 'Calibri 24 bold', textvariable=output_string)
output_label.pack()

x1y1_string = tk.StringVar()
x1y1_label = ttk.Label(master =button_frame_2,textvariable=x1y1_string)
x1y1_label.pack(side='top')

x2y2_string = tk.StringVar()
x2y2_label = ttk.Label(master= button_frame_2, textvariable=x2y2_string)
x2y2_label.pack(side='bottom')

#list
list = Listbox(master=input_frame, width=50, height=10)
list.pack(side='left')
titles = get_titles()
for title in titles:
    list.insert(0, title)
#list.selection_set(first=0)

#events
button_show.bind('<Alt-KeyPress-a>', lambda event: print('an event'))
test = list.bind('<<ListboxSelect>>', onselect)
button_stop.bind('<ButtonRelease-1>', stop_bot)
threshold_scale.bind('<B1-Motion>',threshold)
button_load_img.bind('<ButtonRelease-1>', load_img)
button_window_selection.bind('<ButtonRelease-1>',start_selection)


#run(always at the end)
window.mainloop()





# light

#     cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti
# dark

#     cyborg - darkly - solar - superhero