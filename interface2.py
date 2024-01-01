import tkinter as tk
from tkinter import *
#from tkinter import ttk
import ttkbootstrap as ttk
import pyautogui
from windowcapture import WindowCapture
from main import Running

#main = Running(None)
test2 = False
main = None

def get_titles():
    titles = []
    for x in pyautogui.getAllWindows():  
        if len(x.title)>0:
            titles.append(x.title)
    print(titles)
    return titles

#functions here i guess
def convert():
    mile_input = entry_int.get()
    print(output_string.set(mile_input))
    print(list_string)
    

def onselect(event):
    global test2
    w = event.widget
    idx = int(w.curselection()[0])
    value = w.get(idx)
    print(test2)
    if test2:
        main.close_window()
    if test2 is False:
        main = Running(value)
        main.wincap = WindowCapture(value)
        main.runstuff()
        test = True
    
def stop_bot(event):
    global test2
    if test2:
        main.close_window()
        test2 = False
    


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




#events
button.bind('<Alt-KeyPress-a>', lambda event: print('an event'))
test = list.bind('<<ListboxSelect>>', onselect)
button_stop.bind('<ButtonRelease-1>', stop_bot)

#run(always at the end)
window.mainloop()





# light

#     cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti
# dark

#     cyborg - darkly - solar - superhero