from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from App.database_password.receive_password import ValPass

from App.front_end.mainwindow import SeaofBTCapp


class PassWin:

    def submit_btn(self):
        check = ValPass.receive(self.pass_entry.get())
        if check == 1:
            print("password matched")
            self.root.destroy()
            app = SeaofBTCapp()
            app.mainloop()

        else:
            messagebox.showerror('Error', 'Wrong Password')
            self.pass_entry.delete(0, END)

    def __init__(self):
        self.root = Tk()
        self.root.title("Password Wizard")
        self.root.geometry("750x550+"+str((self.root.winfo_screenwidth())//4)+"+"+str((self.root.winfo_screenheight())//8))
        self.root.minsize(750, 550)
        self.root.resizable(0, 0)
        self.frame = Frame(self.root)
        self.frame.pack(pady=69)

        # Image

        self.img_p = Image.open("..\\image\\pass.png")
        self.img_p = self.img_p.resize((150, 150), Image.ANTIALIAS)
        self.image_p = ImageTk.PhotoImage(self.img_p)
        self.pass_image = Label(self.frame, image=self.image_p)
        self.pass_image.config(width=160, height=160)
        self.pass_image.grid(row=0)

        # password

        self.pass_label = Label(self.frame, text="Protected Page", font="arial 20 bold")
        self.pass_label.grid(row=1)

        # Password Entry
        self.s = IntVar()
        self.pass_entry = Entry(self.frame, show='*', width=30)
        self.pass_entry.focus()
        self.pass_entry.grid(row=2)

        # Password submit button

        self.pass_button = Button(self.frame, width=25, text="Submit", bg="#127dcd", fg="white", bd=2,
                                  command=self.submit_btn)
        self.s.get()
        self.pass_button.grid(row=3, padx=10, pady=10)

        self.root.mainloop()


PassWin()
