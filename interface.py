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
    # mile_input = entry_int.get()
    # print(output_string.set(mile_input))
    # print(list_string)
    display()

def onselect(event):
    global is_running
    global mainf
    global t1
    if is_running is False:
        w = event.widget
        idx = int(w.curselection()[0])
        value = w.get(idx)
        mainf = Running(value)
        t1 = threading.Thread(target=mainf.runstuff)
        t1.start()
        #mainf.wincap.update(value)
        #mainf.run()
        #display(mainf.detection_img)
        is_running = True
    
def stop_bot(event):
    global is_running
    global mainf
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

    


#window
window = ttk.Window(themename='darkly')
window.title('Detection Bot')
window.geometry('1920x1080')

#frame
input_frame = ttk.Frame(master=window)
input_frame.pack(side='bottom')

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
button_show = ttk.Button(master=input_frame, text='Show', command=show_video)
button_show.pack(side ='right', padx=5)

button_stop = ttk.Button(master = input_frame, text='Stop')
button_stop.pack(side='right')

button_load_img = ttk.Button(master = input_frame, text='Load Image')
button_load_img.pack(side='right', padx=5)

#scale
threshold_scale = ttk.Scale(master=input_frame, value=30, from_=30, to=100, length=500)
threshold_scale.pack()

#output
output_string = tk.StringVar()
output_label = ttk.Label(master=input_frame, text='Output', font = 'Calibri 24 bold', textvariable=output_string)
output_label.pack()

#list
list_string = tk.StringVar()
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
threshold_scale.bind('<B1-Motion>',threshold )
button_load_img.bind('<ButtonRelease-1>', load_img)

#run(always at the end)
window.mainloop()





# light

#     cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti
# dark

#     cyborg - darkly - solar - superhero