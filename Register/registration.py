from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import sys
sys.path.append("C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm")
import database_con

from imutils import face_utils
from imutils.video import VideoStream
import numpy as np
import imutils
import dlib
import cv2
import os

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def btn_clicked():

    isValid = True
    
    #name check
    if bool(re.match('[a-zA-Z\s]+$',name.get())) and len(name.get())>3 and name.get()!="":
        print("valid name")
    else:
        messagebox.showwarning("Invalid Name","Please Enter Valid Name ")
        isValid=False
        
    #mobile no check
    if mobileno.get().isnumeric() and len(mobileno.get())==10:
        print("valid mobile no")
    else:
        messagebox.showwarning("Invalid Mobile no","Please Enter Valid Mobile no ")
        isValid=False
        
    # email check
    if(re.fullmatch(regex, email.get()) and email.get()!="" ):
        print("Valid Email")
    else:
        messagebox.showwarning("Invalid Email Id","Please Enter Valid Email Id")
        isValid=False

    #accountno check
    if accountno.get().isnumeric() and len(accountno.get())==11:
        print("valid Account no")
    else:
        messagebox.showwarning("Invalid Account no","Please Enter Valid Account No")
        isValid=False
        
    # output/ store in databse
    print(name.get() , mobileno.get() , email.get() , accountno.get())
    
    if(isValid):
        if(captureFace()):
            previewData()

def captureFace():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    #load the input image, resize it, and convert it to grayscale
    os.makedirs(f'C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\users_face/{accountno.get()}')
    vs = VideoStream(0).start()
    img_counter = 0
    while True:
        frame = vs.read()
        image = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscale image
        rects = detector(gray, 1)
        
        
        path = f'C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\users_face/{accountno.get()}' 
        os.chdir(path)
        # loop over the face detections
        for (i, rect) in enumerate(rects):
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            # convert dlib's rectangle to a OpenCV-style bounding box
            # [i.e., (x, y, w, h)], then draw the face bounding box
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # show the face number
            cv2.putText(image, "Face Detected".format(i + 1), (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # loop over the (x, y)-coordinates for the facial landmarks
            # and draw them on the image
            for (x, y) in shape:
                cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
            
        # show the output image with the face detections + facial landmarks
        # show the output
        cv2.imshow('Frame', image)
        k = cv2.waitKey(1)
        if k%256 == 27:
                # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32: 
            print(img_counter)
            cv2.imwrite(f"{img_counter}.png", frame)
            print("{}/{} written!".format(path,img_counter))
            img_counter=img_counter+1
            

        if(img_counter==3):
            cv2.destroyAllWindows()
            vs.stop()
            return True
            
    # clean up
    cv2.destroyAllWindows()
    vs.stop()

def previewData():
    
    newWindow = Toplevel(window)
    # sets the title of the
    # Toplevel widget
    newWindow.title("Preview") 
    # sets the geometry of toplevel
    newWindow.geometry("300x400")
    # A Label widget to show in toplevel
    Label(newWindow,
          text ="Please check the Image and confirm").pack()
    # print(accountno.get())
    img= Image.open(f"C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\users_face\\{accountno.get()}\\0.png")
    #Resize the Image using resize method
    resized_image= img.resize((300,300), Image.ANTIALIAS)
    new_image= ImageTk.PhotoImage(resized_image)
    image1 = Label(newWindow, image=new_image)
    image1.image = new_image
    image1.place(x=0, y=0)
    
    b = Button(newWindow,text = "Confirm",bg="#11ffff",command=confirmData)
    b.place(x = 100,y = 350,width=100,height=30)

def confirmData():
    database_con.curr.execute("INSERT INTO `users` (name, mobileno, email, accountno) VALUES(%s, %s, %s, %s)", (str(name.get()), str(mobileno.get()), str(email.get()), str(accountno.get())))
    database_con.conn.commit()
    database_con.curr.close()
    database_con.conn.close()
    messagebox.showinfo("Registration Successful")
    name.delete(0,END)
    mobileno.delete(0,END)
    email.delete(0,END)
    accountno.delete(0,END)
    window.after(3500,lambda:window.destroy())


################################################################
window = Tk()

window.geometry("1250x650")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 650,
    width = 1250,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\Register\\ui_img\\background.png")
background = canvas.create_image(
    625.0, 314.0,
    image=background_img)

entry0_img = PhotoImage(file = f"C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\Register\\ui_img\\img_textBox0.png")
entry0_bg = canvas.create_image(
    600.5, 183.0,
    image = entry0_img)

name = Entry(
    bd = 0,
    bg = "#ffffff",
    
    highlightthickness = 0)

name.place(
    x = 434.0, y = 163,
    width = 333.0,
    height = 38)

entry1_img = PhotoImage(file = f"C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\Register\\ui_img\\img_textBox1.png")
entry1_bg = canvas.create_image(
    600.5, 399.0,
    image = entry1_img)

email = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

email.place(
    x = 434.0, y = 379,
    width = 333.0,
    height = 38)

entry2_img = PhotoImage(file = f"C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\Register\\ui_img\\img_textBox2.png")
entry2_bg = canvas.create_image(
    600.5, 507.0,
    image = entry2_img)

accountno = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

accountno.place(
    x = 434.0, y = 487,
    width = 333.0,
    height = 38)

entry3_img = PhotoImage(file = f"C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\Register\\ui_img\\img_textBox3.png")
entry3_bg = canvas.create_image(
    600.5, 291.0,
    image = entry3_img)

mobileno = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

mobileno.place(
    x = 434.0, y = 271,
    width = 333.0,
    height = 38)

img0 = PhotoImage(file = f"C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\Register\\ui_img\\img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 473, y = 540,
    width = 285,
    height = 73)

window.resizable(False, False)
window.mainloop()
