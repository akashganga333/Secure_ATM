from tkinter import *
import sys
sys.path.append("C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm")   
import database_con


def Dashview(mobileno):
    database_con.curr.execute('select name from users where mobileno = %s',mobileno)
    name = database_con.curr.fetchone()[0]
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

    background_img = PhotoImage(file = f"C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\ATM\\interface_img\\dashback.png")
    background = canvas.create_image(
        612.5, 358.5,
        image=background_img)

    canvas.create_text(
        625.0, 43.0,
        text = f"WELCOME {name}",
        fill = "#000000",
        font = ("Roboto-Bold", int(48.0)))

    window.resizable(False, False)
    window.after(10000,lambda:window.destroy())
    window.mainloop()
