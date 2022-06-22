import tkinter
import cv2
import PIL.Image,PIL.ImageTk
from functools import partial
import threading
import imutils
import time
stream=cv2.VideoCapture("clip.mp4")
flag=True
def play(speed):
    global flag
    print(f"your speed is {speed}")
    frame1=stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES,frame1+speed)
    grabbed,frame=stream.read()
    if not grabbed:
        exit()
    frame=imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134,26,text="decision pending",font="Times 26 bold",fill="black")
    flag=not flag
def pending(decision):
    # 1. Display decision pending image
    frame=cv2.cvtColor(cv2.imread("decisionpending.jpg"),cv2.COLOR_BGR2RGB)
    frame=imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)
    # 2. Wait for 1 second
    time.sleep(1)
    # 3. Display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsors.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    # 4. Wait for 1.5 second
    time.sleep(1.5)
    # 5. Display out/notout image
    if decision=="out":
        decisionimg="out.jpg"
    else:
        decisionimg="not out.jpg"
    frame = cv2.cvtColor(cv2.imread(decisionimg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
def out():
    thread=threading.Thread(target=pending,args=("out",))
    thread.daemon=1
    thread.start()
    print("player is out")
def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("player is not out")
SET_WIDTH=654
SET_HEIGHT=368
window=tkinter.Tk()
window.title("DRS BY SARTHAK CHAUDHARY")
cv_img=cv2.cvtColor(cv2.imread("welcome.jpg"),cv2.COLOR_BGR2RGB)
canvas=tkinter.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT)
photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas=canvas.create_image(0,0,ancho=tkinter.NW,image=photo)
canvas.pack()
#buttons to control playback
btn=tkinter.Button(window,text="<< Previous (fast)",width=50,command=partial(play,-25))
btn.pack()
btn=tkinter.Button(window,text="<< Previous (slow)",width=50,command=partial(play,-2))
btn.pack()
btn=tkinter.Button(window,text="Next (fast) >>",width=50,command=partial(play,2))
btn.pack()
btn=tkinter.Button(window,text="Next (slow) >>",width=50,command=partial(play,25))
btn.pack()
btn=tkinter.Button(window,text="Give Out",width=50,command=out)
btn.pack()
btn=tkinter.Button(window,text="Give Not Out",width=50,command=not_out)
btn.pack()
window.mainloop()
