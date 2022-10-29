from tkinter import *
from tkinter import messagebox
import sys
sys.path.append("C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm")   
import database_con
# from Face_Recognization import encode_faces
from Liveness_detection import encode_faces


def btn_clicked():
    if mobileno.get().isnumeric() and len(mobileno.get())==10:
        database_con.curr.execute('select accountno from users where mobileno = %s',mobileno.get())
        try:
            accno = database_con.curr.fetchone()[0]
        except:
            messagebox.showwarning("Invalid Mobile no","Mobile Number doesn't exist")
        mobno = mobileno.get()
        if encode_faces.getaccno(accno):
            from Liveness_detection import Liveness_demo
            label_name,name = Liveness_demo.scanFace() 
            
            if label_name!="fake" and name!="Unknown":
                window.destroy()
                import otp_interface
                #otp_interface.sendOTP(mobileno.get())
                otp_interface.OTPcheck(mobno)

    
        
    else:
        messagebox.showwarning("Invalid Mobile no","Please Enter Valid Mobile no ")



    
window = Tk()

window.geometry("1200x650")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 650,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

entry0_img = PhotoImage(file = "C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\ATM\\interface_img\\img_textBox0.png")
entry0_bg = canvas.create_image(
    920.5, 351.0,
    image = entry0_img)

mobileno = Entry(
    bd = 0,
    bg = "#ffffff",
    
    font = ("Rubik-Regular", int(25.0)),
    
    highlightthickness = 0)

mobileno.place(
    x = 761.0, y = 309,
    width = 319.0,
    height = 82)

img0 = PhotoImage(file = "C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\ATM\\interface_img\\img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 719, y = 435,
    width = 377,
    height = 124)

background_img = PhotoImage(file = "C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\ATM\\interface_img\\background.png")
background = canvas.create_image(
    560.5, 321.0,
    image=background_img)

window.resizable(False, False)
window.mainloop()
