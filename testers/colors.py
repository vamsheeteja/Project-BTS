# from tkinter import *

# root = Tk()

# root.geometry("500x500+200+200")
# root.title("Epilepsy Giver")
# root.resizable(width = FALSE, height = FALSE)

# def get_colour():
#     colours = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'violet']
#     while True:
#         for c in colours:
#             yield c
# def start():
#     root.configure(background=next(colour_getter)) # set the colour to the next colour generated
#     root.after(1000, start) # run this function again after 1000ms

# colour_getter = get_colour()
# startButton = Button(root,text="START",command=start)
# startButton.pack()

# root.mainloop()

from tkinter import *
from tkinter import ttk
#Create an instance of tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
#Create an Entry Widget
entry= ttk.Entry(win,font=('Century 22'),width=40)
entry.pack(pady= 30)
win.mainloop()