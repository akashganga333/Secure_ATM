from tkinter import *
from tkinter import messagebox
from twilio.rest import Client
import random



def OTPcheck(num):
    mobileno = f"+91-{num}"
    print(mobileno)
    n = random.randint(100000,999999)
    client=Client("AC8dd33014dfbebc0ad11c5de0f286b83e","65c0e8c8e0410c6597511210d1e7488b")
    client.messages.create(to = mobileno,
                                  from_="+12344054235",
                                  body=n)
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

    background_img = PhotoImage(file = f"C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\ATM\\interface_img\\background1.png")
    background = canvas.create_image(
        625.0, 306.0,
        image=background_img)

    entry0_img = PhotoImage(file = f"C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\ATM\\interface_img\\img_textBox1.png")
    entry0_bg = canvas.create_image(
        658.0, 264.0,
        
        image = entry0_img)

    enteredOtp = Entry(
        bd = 0,
        bg = "#ffffff",
        font = ("Rubik-Regular", int(25.0)),
        highlightthickness = 0)

    enteredOtp.place(
        x = 506.0, y = 222,
        width = 304.0,
        height = 82)

    
    img0 = PhotoImage(file = f"C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\ATM\\interface_img\\img1.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command =lambda: validateOTP(window,n,int(enteredOtp.get()),num),
        relief = "flat")

    b0.place(
        x = 554, y = 369,
        width = 207,
        height = 71)

    window.resizable(False, False)
    window.mainloop()


def validateOTP(window,n,enteredOTP,num):
    if enteredOTP==n:
        messagebox.showinfo("showinfo","Login success")
        window.destroy()
        import Dashboard
        Dashboard.Dashview(num)
    else:
        messagebox.showinfo("showinfo","Wrong OTP")
        window.destroy()
        import ATM_interface
