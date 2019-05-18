from tkinter import *

root = Tk()

def callback(event):
    print ("clicked at", event.x, event.y)
def two(event):
    print('two at',event.x,event.y)
def three(event):
    print("three at",event.x,event.y)

frame = Frame(root, width=100, height=100)
frame.bind("<Button-1>", callback)
frame.pack()

button = Button(frame,text="btn",width=10,height =10)
button.bind('<Button-1>',two)
button.pack()

button2 = Button(frame,text="btn2",width = 20,height = 20)
button2.bind('<Button-1>',three)
button2.pack()

root.mainloop()
root.destroy()