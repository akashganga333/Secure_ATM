from tkinter import *



class dashboarddisplay():
    def display(self):
        root = Tk()
        root.minsize(height=500,width=900)
        label1 = Label(root,text=f"Welcome",font=('Times_New_Roman',25))
        label1.pack()
        root.mainloop()
if __name__=="__main__":
    w=dashboarddisplay()
    w.display()
   
