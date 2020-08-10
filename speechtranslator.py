from tkinter import *
import tkinter.font as font
from tkinter.filedialog import askopenfilename
import pytesseract
from googletrans import Translator
from PIL import *
from PIL import ImageTk, Image
import numpy as np
import pyttsx3
import imghdr
import cv2

root = Tk()
root.title("Translating Telugu Word Image to its Meaningful English Word as Speech")
root.geometry('600x400')
canv = Canvas(root, width=600, height=400, bg='white')
canv.grid(row=2, column=3)
img = ImageTk.PhotoImage(Image.open("backgrounds2.jpg"))  
canv.create_image(0, 0, anchor=NW, image=img)

translator = Translator()

def convert(location):
    global btn1
    global li_box
    global lb2
    try:
        lb1.destroy()
    except Exception as e:
        print(e)
    img = Image.open(location)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #cv2.imshow("Gray Scale", img)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    kernel = np.ones((5,5), np.uint8) 
    img = cv2.erode(img, kernel, iterations=1) 
    #cv2.imshow("eroded", img)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    img = cv2.dilate(img, kernel, iterations=1)
    #cv2.imshow("dilation", img)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    a = pytesseract.image_to_string(img, lang='tel')
    file = open("file.txt", "wb")
    print(a)
    file.write(a.encode("utf-8"))
    file.close()
    print(len(a))
    root.config(height=400, bg = "white")
    li_box = Text(root)
    li_box.place(x=80, y=160, height = 300, width = 500)
    li_box.delete(0.0, "end")
    with open('file.txt', 'rb') as f:
        data = f.read().decode("utf-8")
        s = translator.translate(data, dest='en')
        if len(s.text)==0:
            lb2=Label(text='Given Image does not contain any telugu word', font=('Arial', 10), bg='White', fg='Red')
            lb2.place(x=90, y=170)
        else:
            li_box.insert(0.0, s.text)
            engine = pyttsx3.init()
            engine.say(s.text)
            engine.runAndWait()

            btn1 = Button(root, text='Clear Text',bg='PaleGreen', command=lambda: li_box.delete(0.0, "end"))
            btn1.place(x=500, y=120)

def browse():
    global btn2
    global btn1
    global lb1
    global lb3
    try:
        btn1.destroy()
        li_box.destroy()
        btn2.destroy()
        lb2.destroy()
    except Exception as e:
        print(e)
        print('ignore error')
    finally:
        loc = askopenfilename(parent=root)
        if not loc:
            lb3=Label(text='Please select an image to translate', font=('Arial', 10), bg='White', fg='Red')
            lb3.place(x=200, y=80)
            lb3.after(3000, lambda: lb3.destroy())

        else:
            print(loc)
            val = loc.split('.')[-1]
            str=imghdr.what(loc,h=None)
            if str=='jpeg' or str=='png':
                lb1=Label(text='Image Uploaded Successfully, Please click on convert button to translate', font=('Arial', 10), bg='White', fg='Blue')
                lb1.place(x=130, y=80)
                btn2 = Button(text='Convert',bg='PaleGreen', command=lambda: convert(loc))
                btn2.place(x=300, y=120)
            else:
                lab = Label(text='file not supported',
                        fg='red', font=("Arial", 14))
                lab.place(x=200, y=200)
                lab.after(3000, lambda: lab.destroy())
                print('try to provide jpg or jpeg formated image.')

            
def start_gui():

    Label(text='SPEECH TRANSLATOR', font=font.Font(family='Arial', size=20, weight='bold'), bg='White', fg='OrangeRed').place(x=160, y=40)
    Button(text='Browse',bg='PaleGreen', command=browse).place(x=200, y=120)
    

start_gui()


mainloop()


