import threading
import tkinter as tk
from tkinter import *
#from tkinter import ttk
import ttkbootstrap as ttk
import pyautogui
from windowcapture import WindowCapture
from main import Running
import cv2 as cv
from PIL import Image, ImageTk
from detection import Detection


#mainf = Running(None)
test2 = False
mainf = None

def get_titles():
    titles = []
    for x in pyautogui.getAllWindows():  
        if len(x.title)>0:
            titles.append(x.title)
    print(titles)
    return titles

#functions here i guess
def convert():
    nuts = True
    # mile_input = entry_int.get()
    # print(output_string.set(mile_input))
    # print(list_string)
    display()

def onselect(event):
    global test2
    global mainf
    w = event.widget
    idx = int(w.curselection()[0])
    value = w.get(idx)
    print(test2)
    # if test2:
    #     mainf.close_window()
    if test2 is False:
        mainf = Running(value)
        t1 = threading.Thread(target=mainf.runstuff)
        t1.start()
        #mainf.wincap = WindowCapture(value)
        #mainf.run()
        #display(mainf.detection_img)
        test2 = True
    
def stop_bot(event):
    global test2
    global mainf
    nuts = False
    if test2:
        #mainf._return = True
        mainf.close_window()
        test2 = False

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
    img = mainf.get_detection_img()
    to_pil(img, title_label, 10, 10, 1000, 1000)
    title_label.after(10, display)

def threshold(event):
    threshold=int((threshold_scale.get()))/100
    threshold_string.set(threshold) 
    if not mainf is None:
        mainf.detector.update_threshold(threshold)

    


#window
window = ttk.Window(themename='darkly')
window.title('Detection Bot')
window.geometry('1920x1080')

#title
title_label = ttk.Label(master=window, text = 'Test')
title_label.pack()

#input
input_frame = ttk.Frame(master=window)
entry_int = tk.IntVar(value=7)
entry = ttk.Entry(master=input_frame, textvariable=entry_int)
button = ttk.Button(master=input_frame, text='Convert', command=convert)
entry.pack(side ='left', padx=10)
button.pack(side ='left', pady=50)
input_frame.pack()

button_stop = ttk.Button(master = input_frame, text='Stop')
button_stop.pack()

threshold_scale =  ttk.Scale(window, value=30, from_=30, to=100, length=500)
threshold_scale.pack()

threshold_string= tk.StringVar()
threshold_label = ttk.Label(window, text='blablalbla', textvariable=threshold_string)
threshold_label.pack()

#output
output_string = tk.StringVar()
output_label = ttk.Label(master=window, text='Output', font = 'Calibri 24 bold', textvariable=output_string)
output_label.pack()

list_string = tk.StringVar()
list = Listbox(master=window, width=50, height=20)
list.pack()
titles = get_titles()
for title in titles:
    list.insert(0, title)
#list.selection_set(first=0)

# img = cv.imread('assets/bear.jpg')
# rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# to_pil(rgb, title_label, 10, 10, 200, 200)

#events
button.bind('<Alt-KeyPress-a>', lambda event: print('an event'))
test = list.bind('<<ListboxSelect>>', onselect)
button_stop.bind('<ButtonRelease-1>', stop_bot)
threshold_scale.bind('<B1-Motion>',threshold )

#run(always at the end)
window.mainloop()





# light

#     cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti
# dark

#     cyborg - darkly - solar - superhero