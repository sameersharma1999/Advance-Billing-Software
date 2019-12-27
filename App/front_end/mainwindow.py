import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from App.back_end.validations import Validate
from App.backend_database.database_connection import DBConnection
from App.backend_database.in_up_de import InDeUp
from tkinter.ttk import Combobox
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
import datetime
from App.back_end.frontend import InterBilling
from App.back_end.excel_pdf import ExcelToPdf

LARGE_FONT = ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.title("BILLING SYSTEM")
        # container.pack(side="top", fill="both", expand=True)
        container.pack()

        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (FirstWin, CustomerDetails, ItemDetails, CustomerEdit, ItemEdit, CreateBill):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstWin)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.text = None

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("arial", "8", "normal"))

        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


class FirstWin(tk.Frame):
    # root = Tk()
    # root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    # root.minsize(750, 550)
    # root.title("Billing System")
    # root.iconbitmap("..\\image\\icon.ico")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.frame = window
        # self.frame.pack(pady=30)
        # Resizing disable
        # self.root.resizable(0, 0)
        self.label_frame = LabelFrame(self, text="Choose from following options: ", font="arial 12")
        self.label_frame.pack(padx=10, pady=30)
        # ADD CUSTOMER

        self.add_c_image = Image.open("..\\image\\addcustomer.png")
        self.add_c_image = self.add_c_image.resize((190, 200), Image.ANTIALIAS)
        self.add_c_img = ImageTk.PhotoImage(self.add_c_image)
        self.add_customer = Button(self.label_frame, bd=2, image=self.add_c_img,
                                   command=lambda: controller.show_frame(CustomerDetails))
        self.add_customer.config(width=200, height=200, cursor="hand2")
        self.add_customer.grid(row=0, column=0)
        CreateToolTip(self.add_customer, text='Add a new customer')
        # label
        self.label_a_c = Label(self.label_frame, text="Add Customer", font="arial 12")
        self.label_a_c.grid(row=1, column=0)

        # ADD ITEM

        self.add_i_image = Image.open("..\\image\\itemadd.png")
        self.add_i_image = self.add_i_image.resize((190, 200), Image.ANTIALIAS)
        self.add_i_img = ImageTk.PhotoImage(self.add_i_image)
        self.add_item = Button(self.label_frame, bd=2, image=self.add_i_img,
                               command=lambda: controller.show_frame(ItemDetails))
        self.add_item.config(width=200, height=200, cursor="hand2")
        self.add_item.grid(row=0, column=1)
        CreateToolTip(self.add_item, text='Add a new item')
        # label
        self.label_a_i = Label(self.label_frame, text="Add Item", font="arial 12")
        self.label_a_i.grid(row=1, column=1)

        # BILL CREATION

        self.bill_c_image = Image.open("..\\image\\billcreate.png")
        self.bill_c_image = self.bill_c_image.resize((185, 200), Image.ANTIALIAS)
        self.bill_c_img = ImageTk.PhotoImage(self.bill_c_image)
        self.bill_create = Button(self.label_frame, bd=2, image=self.bill_c_img, padx=20,
                                  command=lambda: controller.show_frame(CreateBill))
        self.bill_create.config(width=200, height=200, cursor="hand2")
        self.bill_create.grid(row=0, column=2)
        CreateToolTip(self.bill_create, text='Create a new bill.')
        # label
        self.bill_create = Label(self.label_frame, text="Create Bill", font="arial 12")
        self.bill_create.grid(row=1, column=2)

        # CUSTOMER EDIT

        self.edit_c_image = Image.open("..\\image\\customeredit.png")
        self.edit_c_image = self.edit_c_image.resize((190, 200), Image.ANTIALIAS)
        self.edit_c_img = ImageTk.PhotoImage(self.edit_c_image)
        self.edit_customer = Button(self.label_frame, bd=2, image=self.edit_c_img,
                                    command=lambda: controller.show_frame(CustomerEdit))
        self.edit_customer.config(width=200, height=200, cursor="hand2")
        self.edit_customer.grid(row=2, column=0)
        CreateToolTip(self.edit_customer, text='Edit details of previous customer')
        # label
        self.label_e_c = Label(self.label_frame, text="Edit Customer", font="arial 12")
        self.label_e_c.grid(row=3, column=0)

        # ITEM EDIT

        self.edit_i_image = Image.open("..\\image\\itemedit.png")
        self.edit_i_image = self.edit_i_image.resize((180, 200), Image.ANTIALIAS)
        self.edit_i_img = ImageTk.PhotoImage(self.edit_i_image)
        self.edit_item = Button(self.label_frame, bd=2, image=self.edit_i_img,
                                command=lambda: controller.show_frame(ItemEdit))
        self.edit_item.config(width=200, height=200, cursor="hand2")
        self.edit_item.grid(row=2, column=1)
        CreateToolTip(self.edit_item, text='Edit previous item')
        # label
        self.label_e_i = Label(self.label_frame, text="Edit Item", font="arial 12")
        self.label_e_i.grid(row=3, column=1)

        # SHOW BILL

        self.show_b_image = Image.open("..\\image\\cancel.png")
        self.show_b_image = self.show_b_image.resize((170, 200), Image.ANTIALIAS)
        self.show_b_img = ImageTk.PhotoImage(self.show_b_image)
        self.show_bill = Button(self.label_frame, bd=2, image=self.show_b_img, command=FirstWin.exit_func)
        self.show_bill.config(width=200, height=200, cursor="hand2")
        self.show_bill.grid(row=2, column=2)
        CreateToolTip(self.show_bill, text='Close the application')
        # label
        self.label_s_b = Label(self.label_frame, text="Exit", font="arial 12")
        self.label_s_b.grid(row=3, column=2)

    @staticmethod
    def exit_func():
        sys.exit()
    # def cus_link(self):
    #     self.frame.pack_forget()
    #     CustomerDetails(self.root)
    #
    # def item_link(self):
    #     self.frame.pack_forget()
    #     ItemDetails(self.root)
    #
    # def cus_edit_link(self):
    #     self.frame.pack_forget()
    #     CustomerEdit(self.root)
    #
    # def bill_link(self):
    #     self.frame.pack_forget()
    #
    # def item_edit_link(self):
    #     self.frame.pack_forget()
    #     ItemEdit(self.root)
    #
    # def show_bill_link(self):
    #     self.frame.pack_forget()


class CustomerDetails(tk.Frame):
    control = None
    customer_dir = {}
    try:
        my_db = DBConnection.get_connection()
    except Exception:
        messagebox.showerror("Connection Error", 'Database in not connected')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # CustomerDetails.control = controller
        # self.window = window
        # self.window.title('CustomerDetails')
        # self.window.geometry('520x500+500+150')
        # self.window.configure(background='white')
        # self.window.wm_minsize(width=500, height=500)
        # self.window.wm_maxsize(width=500, height=500)
        # self.main_frame_outer = Frame(self)
        # self.main_frame_outer.pack(side=LEFT)
        self.states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujrat',
                       'Harayana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerla',
                       'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
                       'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                       'Uttarakhand', 'West Bengal']
        self.my_font = Font(family='Times New Roman', size=18)
        self.font2 = Font(family='Times New Roman', size=22, weight='bold')
        self.font3 = Font(family='Times New Roman', size=12)

        # self.main_menu = Menu(self)
        # self.config(menu=self.main_menu)
        # self.file_menu = Menu(self.main_menu)
        # self.main_menu.add_cascade(label='File', menu=self.file_menu)
        # self.file_menu.add_command(label='Save   Ctrl+S', command=self.save)
        # self.file_menu.add_command(label='Cancel   Ctrl+E', command=self.cancel)
        #
        # self.goto_menu = Menu(self)
        # self.main_menu.add_cascade(label='Goto', menu=self.goto_menu)
        # self.goto_menu.add_command(label='Home', command=lambda: controller.show_frame(FirstWin))      # make changes in command (redirect to home page)
        # self.inter_mediate_frame = Frame(self.main_frame_outer)
        self.outerframe = LabelFrame(self, background='white')
        self.name = Label(self.outerframe, text='Add Customer Details', font=self.font2, background='white')
        self.name.grid(row=0, column=0, padx=10, pady=10)

        # # TOOL BAR ON LEFT FUNCTION
        # self.toolbar = Frame(self.main_frame_outer, bg="blue")
        #
        # # ADD CUSTOMER
        #
        # self.add_c_image = Image.open("image\\addcustomer.png")
        # self.add_c_image = self.add_c_image.resize((40, 50), Image.ANTIALIAS)
        # self.add_c_img = ImageTk.PhotoImage(self.add_c_image)
        # self.add_customer = Button(self.toolbar, bd=2, image=self.add_c_img, command=lambda: controller.show_frame(CustomerDetails, 0))
        # self.add_customer.config(cursor="hand2")
        # self.add_customer.pack(side=TOP, padx=2, pady=2)
        # CreateToolTip(self.add_customer, text='Add a new customer')
        #
        # # ADD ITEM
        #
        # self.add_i_image = Image.open("image\\itemadd.png")
        # self.add_i_image = self.add_i_image.resize((40, 50), Image.ANTIALIAS)
        # self.add_i_img = ImageTk.PhotoImage(self.add_i_image)
        # self.add_item = Button(self.toolbar, bd=2, image=self.add_i_img,
        #                        command=lambda: controller.show_frame(ItemDetails, 0))
        # self.add_item.config(cursor="hand2")
        # self.add_item.pack(side=TOP, padx=2, pady=2)
        # CreateToolTip(self.add_item, text='Add a new item')
        # # # label
        # # self.label_a_i = Label(self.toolbar, text="Add Item", font="arial 12")
        # # self.label_a_i.grid(row=1, column=1)
        #
        # # BILL CREATION
        #
        # self.bill_c_image = Image.open("image\\billcreate.png")
        # self.bill_c_image = self.bill_c_image.resize((40, 50), Image.ANTIALIAS)
        # self.bill_c_img = ImageTk.PhotoImage(self.bill_c_image)
        # self.bill_create = Button(self.toolbar, bd=2, image=self.bill_c_img, padx=20,
        #                           command=lambda: controller.show_frame(CustomerDetails, 0))
        # self.bill_create.config(cursor="hand2")
        # self.bill_create.pack(side=TOP, padx=2, pady=2)
        # CreateToolTip(self.bill_create, text='Create a new bill.')
        # # # label
        # # self.bill_create = Label(self.toolbar, text="Create Bill", font="arial 12")
        # # self.bill_create.grid(row=1, column=2)
        #
        # # CUSTOMER EDIT
        #
        # self.edit_c_image = Image.open("image\\customeredit.png")
        # self.edit_c_image = self.edit_c_image.resize((40, 50), Image.ANTIALIAS)
        # self.edit_c_img = ImageTk.PhotoImage(self.edit_c_image)
        # self.edit_customer = Button(self.toolbar, bd=2, image=self.edit_c_img,
        #                             command=lambda: controller.show_frame(CustomerEdit, 0))
        # self.edit_customer.config(cursor="hand2")
        # self.edit_customer.pack(side=TOP, padx=2, pady=2)
        # CreateToolTip(self.edit_customer, text='Edit details of previous customer')
        # # # label
        # # self.label_e_c = Label(self.toolbar, text="Edit Customer", font="arial 12")
        # # self.label_e_c.grid(row=3, column=0)
        #
        # # ITEM EDIT
        #
        # self.edit_i_image = Image.open("image\\itemedit.png")
        # self.edit_i_image = self.edit_i_image.resize((40, 50), Image.ANTIALIAS)
        # self.edit_i_img = ImageTk.PhotoImage(self.edit_i_image)
        # self.edit_item = Button(self.toolbar, bd=2, image=self.edit_i_img,
        #                         command=lambda: controller.show_frame(ItemEdit, 0))
        # self.edit_item.config(cursor="hand2")
        # self.edit_item.pack(side=TOP, padx=2, pady=2)
        # CreateToolTip(self.edit_item, text='Edit previous item')
        # # # label
        # # self.label_e_i = Label(self.toolbar, text="Edit Item", font="arial 12")
        # # self.label_e_i.grid(row=3, column=1)
        #
        # # SHOW BILL
        #
        # self.show_b_image = Image.open("image\\showbill.png")
        # self.show_b_image = self.show_b_image.resize((40, 50), Image.ANTIALIAS)
        # self.show_b_img = ImageTk.PhotoImage(self.show_b_image)
        # self.show_bill = Button(self.toolbar, bd=2, image=self.show_b_img,
        #                         command=lambda: controller.show_frame(CustomerEdit, 0))
        # self.show_bill.config(cursor="hand2")
        # self.show_bill.pack(side=TOP, padx=2, pady=2)
        # CreateToolTip(self.show_bill, text='Show all existing bills')
        #
        # self.toolbar.place(x=0, y=(self.winfo_screenheight())//2)

        self.top_frame = Frame(self.outerframe, background='white')
        self.left_frame = Frame(self.top_frame, background='white')
        self.label_first_name = Label(self.left_frame, text='First Name: ', font=self.my_font, background='white').grid(
            row=0, column=0, stick=W, padx=10, pady=10)
        self.label_last_name = Label(self.left_frame, text='Last Name: ', font=self.my_font, background='white').grid(
            row=1, column=0, stick=W, padx=10, pady=10)
        self.address = Label(self.left_frame, text='Address: ', font=self.my_font, background='white').grid(row=2,
                                                                                                            column=0,
                                                                                                            stick=W,
                                                                                                            padx=10,
                                                                                                            pady=10)
        self.state = Label(self.left_frame, text='State: ', font=self.my_font, background='white').grid(row=3, column=0,
                                                                                                        stick=W,
                                                                                                        padx=10,
                                                                                                        pady=10)
        self.city = Label(self.left_frame, text='City: ', font=self.my_font, background='white').grid(row=4, column=0,
                                                                                                      stick=W, padx=10,
                                                                                                      pady=10)
        self.gst = Label(self.left_frame, text='GST Number: ', font=self.my_font, background='white').grid(row=5,
                                                                                                           column=0,
                                                                                                           stick=W,
                                                                                                           padx=10,
                                                                                                           pady=10)
        self.addhar = Label(self.left_frame, text='Addhar Card Number: ', font=self.my_font, background='white').grid(
            row=6, column=0, stick=W, padx=10, pady=10)
        self.pan = Label(self.left_frame, text='PAN Number: ', font=self.my_font, background='white').grid(row=7,
                                                                                                           column=0,
                                                                                                           stick=W,
                                                                                                           padx=10,
                                                                                                           pady=10)
        self.mobile = Label(self.left_frame, text='Mobile Number: ', font=self.my_font, background='white').grid(row=8,
                                                                                                                 column=0,
                                                                                                                 stick=W,
                                                                                                                 padx=10,
                                                                                                                 pady=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        self.f_n = StringVar()
        self.l_n = StringVar()
        self.add = StringVar()
        self.sta = StringVar()
        self.cit = StringVar()
        self.gs = StringVar()
        self.addh = StringVar()
        self.p = StringVar()
        self.mob = StringVar()
        self.right_frame = Frame(self.top_frame, background='white')
        self.efirst_name = ttk.Entry(self.right_frame, text='First Name: ', textvariable=self.f_n, font=self.my_font)
        self.efirst_name.grid(row=0, column=0, stick=W, padx=10, pady=10)
        self.elast_name = ttk.Entry(self.right_frame, text='Last Name: ', textvariable=self.l_n, font=self.my_font)
        self.elast_name.grid(row=1, column=0, stick=W, padx=10, pady=10)
        self.eaddress = ttk.Entry(self.right_frame, text='Address: ', textvariable=self.add, font=self.my_font)
        self.eaddress.grid(row=2, column=0, stick=W, padx=10, pady=10)
        self.estate = Combobox(self.right_frame, value=self.states, textvariable=self.sta, font=self.my_font)
        self.estate.set('Punjab')
        self.estate.grid(row=3, column=0, stick=W, padx=10, pady=10)
        self.ecity = ttk.Entry(self.right_frame, textvariable=self.cit, font=self.my_font)
        self.ecity.grid(row=4, column=0, stick=W, padx=10, pady=10)
        self.egst = ttk.Entry(self.right_frame, textvariable=self.gs, font=self.my_font)
        self.egst.grid(row=5, column=0, stick=W, padx=10, pady=10)
        self.eaddhar = ttk.Entry(self.right_frame, textvariable=self.addh, font=self.my_font)
        self.eaddhar.grid(row=6, column=0, stick=W, padx=10, pady=10)
        self.epan = ttk.Entry(self.right_frame, textvariable=self.p, font=self.my_font)
        self.epan.grid(row=7, column=0, stick=W, padx=10, pady=10)
        self.emobile = ttk.Entry(self.right_frame, textvariable=self.mob, font=self.my_font)
        self.emobile.grid(row=8, column=0, stick=W, padx=10, pady=10)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)
        self.top_frame.grid(row=1, column=0, padx=10, pady=10)

        self.bottom_frame = Frame(self.outerframe, pady=30, background='white')
        self.save_button = Button(self.bottom_frame, text="Save", command=self.save)
        self.save_button.config(width=10, height=0, bg='#0d02cc', fg='white', font=self.font3)
        self.save_button.grid(row=0, column=0, padx=10, pady=10)
        self.cancel_button = Button(self.bottom_frame, text="Cancel", command=lambda: self.clear_cus('c', controller))
        self.cancel_button.config(width=10, height=0, bg='#b8010f', fg='white', font=self.font3)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)
        self.bottom_frame.grid(row=2, column=0, padx=10, pady=10)
        self.outerframe.pack(padx=10, pady=30)
        self.efirst_name.focus()
        # print(self.f_n.get())
        # self.inter_mediate_frame.place(x=(self.winfo_screenwidth()//3), y=(self.winfo_screenheight()//6),
        #                                width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.bind('<Control-s>', self.save)
        self.bind('<Control-e>', lambda: self.clear_cus('c', controller))

    def clear_cus(self, temp, controller):
        if temp == 'c':
            if not self.mob.get() or (self.mob.get() == " "):
                ans = messagebox.askyesno('Leave this window?', 'Do you want to Leave? ')
                if ans:
                    controller.show_frame(FirstWin)
                else:
                    pass
            if self.mob.get() != "":
                ans = messagebox.askyesno('Leave this window?', 'Your data is not saved. Do you want to continue? ')
                if ans:
                    self.efirst_name.delete(first=0, last=100)
                    self.elast_name.delete(first=0, last=100)
                    self.eaddress.delete(first=0, last=100)
                    self.ecity.delete(first=0, last=100)
                    self.egst.delete(first=0, last=100)
                    self.eaddhar.delete(first=0, last=100)
                    self.emobile.delete(first=0, last=100)
                    self.epan.delete(first=0, last=100)
                    self.estate.set('Punjab')
                    controller.show_frame(FirstWin)

        else:
            self.efirst_name.delete(first=0, last=100)
            self.elast_name.delete(first=0, last=100)
            self.eaddress.delete(first=0, last=100)
            self.ecity.delete(first=0, last=100)
            self.egst.delete(first=0, last=100)
            self.eaddhar.delete(first=0, last=100)
            self.emobile.delete(first=0, last=100)
            self.epan.delete(first=0, last=100)
            self.estate.set('Punjab')

    def save(self, event=0):
        CustomerDetails.customer_dir.clear()
        CustomerDetails.customer_dir = {'first_name': self.f_n.get().lower(), "last_name": self.l_n.get().lower(),
                                        'address': self.add.get(), 'state': self.sta.get(),
                                        'city': self.cit.get().lower(),
                                        "gst_number": self.gs.get(), 'addhar_card_number': self.addh.get(),
                                        'pan_number': self.p.get(),
                                        'phone_number': self.mob.get()}
        k = CustomerDetails.customer_dir.values()
        check = Validate.basic_check(k)

        if check == "al":
            messagebox.showinfo("NO DATA", "Enter data before saving it.")
        elif check == "fi":
            messagebox.showinfo("MISSING DATA", "Enter first name of the customer.")
        elif check == "la":
            messagebox.showinfo("MISSING DATA", "Enter the last name of the customer")
        elif check == "ad" or check == "st":
            messagebox.showinfo("MISSING DATA", "Enter address or state of the customer.")
        elif check == "ci":
            messagebox.showinfo("MISSING DATA", "Enter the city from where the customer is.")
        elif check is -1:
            g = Validate.check(CustomerDetails.customer_dir)
            print(CustomerDetails.customer_dir)
            if g[0] == 'empty' and g[1] == 'empty' and g[2] == 'empty':
                messagebox.showinfo("MISSING DATA", "All three GST/PAN/Addhar cannot be empty")
            elif g[3] == 'empty':
                messagebox.showinfo("PHONE NUMBER", "Phone number is mandatory")
            elif 0 in g:
                messagebox.showerror("Error", 'GST/PAN/Addhar/Phone filled wrong')
            else:
                try:
                    # print(CustomerDetails.customer_dir)
                    InDeUp.upload_to_database_customer(CustomerDetails.customer_dir, CustomerDetails.my_db)
                    messagebox.showinfo("Uploaded", 'Data Saved Successfully')
                    self.clear_cus('s', None)
                except Exception as e:
                    messagebox.showwarning("Exists", 'Data already exists')
                    print(e)
        else:
            pass


    # def cancel(self, controller, event=0):
    #     ans = messagebox.askyesno('Leave this window?', 'Your data is not saved')
    #     if ans:
    #         lambda: controller.show_frame(FirstWin)
    #     else:
    #         pass

    # def redirect(self, event=0):
    #     pass


class ItemDetails(tk.Frame):
    item_dir = {}
    try:
        my_db = DBConnection.get_connection()
    except Exception:
        messagebox.showerror("Connection Error", 'Database in not connected')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  # print(window)
        # self.window = tk_r
        # window.title('EditDetails')
        # window.geometry('520x500+500+150')
        self.configure(background='white')
        # window.wm_minsize(width=500, height=500)
        # window.wm_maxsize(width=500, height=500)

        # self.save_pic = ImageTk.PhotoImage(Image.open('E:/Logos/save1.png'))
        self.gss = ['5', '12', '18', '28']
        self.my_font = Font(family='Times New Roman', size=18)
        self.font2 = Font(family='Times New Roman', size=22, weight='bold')
        self.font3 = Font(family='Times New Roman', size=12)

        # self.main_menu = Menu(self)
        # self.config(menu=self.main_menu)
        # self.file_menu = Menu(self.main_menu)
        # self.main_menu.add_cascade(label='File', menu=self.file_menu)
        # self.file_menu.add_command(label='Save   Ctrl+S', command=self.save)
        # self.file_menu.add_command(label='Cancel   Ctrl+E', command=self.cancel)
        #
        # self.goto_menu = Menu(self.main_menu)
        # self.main_menu.add_cascade(label='Goto', menu=self.goto_menu)
        # self.goto_menu.add_command(label='Home', command=self.redirect)     # make changes in command (redirect to home page)

        self.outerframe = LabelFrame(self, background='white')
        self.name = Label(self.outerframe, text='Add Items', font=self.font2, background='white')
        self.name.grid(row=0, column=0, padx=10, pady=10)

        self.top_frame = Frame(self.outerframe, background='white')
        self.left_frame = Frame(self.top_frame, background='white')
        self.item_id = Label(self.left_frame, text='Item Id: ', font=self.my_font, background='white').grid(row=0,
                                                                                                            column=0,
                                                                                                            stick=W,
                                                                                                            padx=10,
                                                                                                            pady=10)
        self.item_name = Label(self.left_frame, text='Item Name: ', font=self.my_font, background='white').grid(row=1,
                                                                                                                column=0,
                                                                                                                stick=W,
                                                                                                                padx=10,
                                                                                                                pady=10)
        self.price = Label(self.left_frame, text='Price ', font=self.my_font, background='white').grid(row=2, column=0,
                                                                                                       stick=W, padx=10,
                                                                                                       pady=10)
        self.gstp = Label(self.left_frame, text='GST(%): ', font=self.my_font, background='white').grid(row=3, column=0,
                                                                                                        stick=W,
                                                                                                        padx=10,
                                                                                                        pady=10)
        self.hsn = Label(self.left_frame, text='HSN code: (Optional)', font=self.my_font, background='white').grid(row=4,
                                                                                                         column=0,
                                                                                                         stick=W,
                                                                                                         padx=10,
                                                                                                         pady=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        self.i_d = StringVar()
        self.i_n = StringVar()
        self.p = StringVar()
        self.g = StringVar()
        self.h = StringVar()
        self.right_frame = Frame(self.top_frame, background='white')
        self.eitem_id = ttk.Entry(self.right_frame, textvariable=self.i_d, font=self.my_font)
        self.eitem_id.grid(row=0, column=0, stick=W, padx=10, pady=10)
        self.eitem_name = ttk.Entry(self.right_frame, textvariable=self.i_n, font=self.my_font)
        self.eitem_name.grid(row=1, column=0, stick=W, padx=10, pady=10)
        self.eprice = ttk.Entry(self.right_frame, textvariable=self.p, font=self.my_font)
        self.eprice.grid(row=2, column=0, stick=W, padx=10, pady=10)
        self.egstp = Combobox(self.right_frame, value=self.gss, textvariable=self.g, font=self.my_font)
        self.egstp.set('5')
        self.egstp.grid(row=3, column=0, stick=W, padx=10, pady=10)
        self.ehsn = ttk.Entry(self.right_frame, textvariable=self.h, font=self.my_font)
        self.ehsn.grid(row=4, column=0, stick=W, padx=10, pady=10)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)
        self.top_frame.grid(row=1, column=0, padx=10, pady=10)

        self.bottom_frame = Frame(self.outerframe, pady=30, background='white')
        self.save_button = Button(self.bottom_frame, text="Save", command=self.save)
        self.save_button.config(width=10, height=0, bg='#0d02cc', fg='white', font=self.font3)
        self.save_button.grid(row=0, column=0, padx=10, pady=10)
        self.cancel_button = Button(self.bottom_frame, text="Cancel", command=lambda: self.clear_item('c', controller))
        self.cancel_button.config(width=10, height=0, bg='#b8010f', fg='white', font=self.font3)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)
        self.bottom_frame.grid(row=2, column=0, padx=10, pady=10)
        self.outerframe.pack(padx=10, pady=30)

        self.bind('<Control-s>', self.save)
        self.bind('<Control-e>', lambda: self.clear_item('c', controller))
        # print(self.i_d.get())
        # self.window.mainloop()

    def clear_item(self, temp, controller):
        if temp == 'c':
            if not self.i_d.get() or (self.i_d.get() == " "):
                ans = messagebox.askyesno('Leave this window?', 'Do you want to Leave? ')
                if ans:
                    controller.show_frame(FirstWin)
                else:
                    pass
            if self.i_d.get() != "":
                ans = messagebox.askyesno('Leave this window?', 'Your data is not saved. Do you want to continue? ')
                if ans:
                    self.egstp.set('5')
                    self.eitem_id.delete(first=0, last=END)
                    self.eitem_name.delete(first=0, last=END)
                    self.eprice.delete(first=0, last=END)
                    self.ehsn.delete(first=0, last=END)
                    controller.show_frame(FirstWin)
        else:
            self.egstp.set('5')
            self.eitem_id.delete(first=0, last=END)
            self.eitem_name.delete(first=0, last=END)
            self.eprice.delete(first=0, last=END)
            self.ehsn.delete(first=0, last=END)

    def save(self, event=0):
        ItemDetails.item_dir = {'item_id': self.i_d.get().strip(), "item_name": self.i_n.get().strip(),
                                'price': self.p.get().strip(), 'gst_per': self.g.get(),
                                'hsn_code': self.h.get().strip()}
        print(ItemDetails.item_dir)
        k = ItemDetails.item_dir.values()
        check = Validate.basic_check(k)
        if check == "al":
            messagebox.showinfo("NO DATA", "Enter data before saving it.")
        elif check == "fi":
            messagebox.showinfo("MISSING DATA", "Enter item ID of the Item.")
        elif check == "la":
            messagebox.showinfo("MISSING DATA", "Enter the Item name of the Item.")
        elif check == "ad":
            messagebox.showinfo("MISSING DATA", "Enter price of the Item.")
        elif check == "st":
            messagebox.showinfo("MISSING DATA", "Enter the gst percent of the Item.")
        else:
            try:
                InDeUp.upload_to_database_items(ItemDetails.item_dir, ItemDetails.my_db)
                messagebox.showinfo("Uploaded", 'Data Saved Successfully')
                # SeaofBTCapp.show_frame(FirstWin, 0)
                self.clear_item('s', None)
            except Exception:
                messagebox.showwarning("Exists", 'Data already exists')

    # def cancel(self, event=0):
    #     ans = messagebox.askyesno('Leave this window?', 'Your data is not saved')
    #     if ans:
    #         self.outerframe.pack_forget()
    #         self.config(menu="")
    #     else:
    #         pass

    # def redirect(self, event=0):
    #     self.outerframe.pack_forget()
    #     self.config(menu="")

    # @staticmethod
    # def initialize():
    #     root = Tk()
    #     ItemDetails(root)
    #     root.mainloop()
    @staticmethod
    def fun():
        pass


class CustomerEdit(tk.Frame):
    customer_dir = {}
    try:
        my_db = DBConnection.get_connection()
    except Exception:
        messagebox.showerror("Connection Error", 'Database in not connected')

    def clear_search_data(self):
        self.efirst_name.delete(0, END)
        self.elast_name.delete(0, END)
        self.eaddress.delete(0, END)
        # self.estate.delete(0, get_data[4])
        self.ecity.delete(0, END)
        self.egst.delete(0, END)
        self.eaddhar.delete(0, END)
        self.eaddhar.delete(0, END)
        self.emobile.delete(0, END)

    def search_details(self):
        if self.search_data.get() == "" or self.search_data.get() == " ":
            messagebox.showinfo("EMPTY", "No mobile number entered:")
        # clear entry box
        else:
            get_data = InDeUp.search_data_customer(self.search_data.get(), CustomerEdit.my_db)
            self.clear_search_data()

            # insert in entry box
            try:
                self.efirst_name.insert(0, get_data[1])
                self.elast_name.insert(0, get_data[2])
                self.eaddress.insert(0, get_data[3])
                # self.estate.insert(0, get_data[4])
                self.ecity.insert(0, get_data[5])
                self.egst.insert(0, get_data[6])
                self.eaddhar.insert(0, get_data[7])
                self.epan.insert(0, get_data[8])
                self.emobile.insert(0, get_data[9])
            except Exception:
                messagebox.showerror("Unable to fetch data", "Check Phone number")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.window = window
        # window.title('CustomerEdit')
        # window.geometry('700x1000')
        # window.configure(background='white')
        # window.wm_minsize(width=700, height=1000)
        # # window.wm_maxsize(width=500, height=500)

        # self.save_pic = ImageTk.PhotoImage(Image.open('E:/Logos/save1.png'))
        self.states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujrat',
                       'Harayana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerla',
                       'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
                       'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                       'Uttarakhand', 'West Bengal']
        self.my_font = Font(family='Times New Roman', size=18)
        self.font2 = Font(family='Times New Roman', size=22, weight='bold')
        self.font3 = Font(family='Times New Roman', size=12)

        # self.main_menu = Menu(self)
        # self.config(menu=self.main_menu)
        # self.file_menu = Menu(self.main_menu)
        # self.main_menu.add_cascade(label='File', menu=self.file_menu)
        # self.file_menu.add_command(label='Save   Ctrl+S', command=self.save)
        # self.file_menu.add_command(label='Cancel   Ctrl+E', command=self.cancel)
        #
        # self.goto_menu = Menu(self.main_menu)
        # self.main_menu.add_cascade(label='Goto', menu=self.goto_menu)
        # self.goto_menu.add_command(label='Home', command=self.redirect)      # make changes in command (redirect to home page)

        self.outerframe = LabelFrame(self, background='white')
        self.name = Label(self.outerframe, text='Edit Customer Details', font=self.font2, background='white')
        self.name.grid(row=0, column=0, padx=10, pady=30)

        self.top_frame = Frame(self.outerframe, background='white')
        self.search_lb_frame = LabelFrame(self.outerframe, background='white')

        # Search bar for the editing details of customer
        self.search_data = StringVar()
        self.search_label = Label(self.search_lb_frame, background='white', text='Search using Mobile No.',
                                  font=self.my_font).grid(row=0, column=0, stick=W, padx=10, pady=10)
        self.search_entry = ttk.Entry(self.search_lb_frame, textvariable=self.search_data, font=self.my_font)
        self.search_entry.grid(row=0, column=1, stick=W, padx=10, pady=10)
        self.search_lb_frame.grid(row=1, padx=10)
        self.img_search = Image.open("..\\image\\search.png")
        self.img_search = self.img_search.resize((25, 25), Image.ANTIALIAS)
        self.image_search = ImageTk.PhotoImage(self.img_search)
        self.image_button = Button(self.search_lb_frame, bd=2, image=self.image_search, command=self.search_details)
        self.image_button.config(cursor="hand2")
        self.image_button.grid(row=0, column=2)

        # # line as a separator
        # self.canvas_line = Canvas(self.top_frame)
        # self.canvas_line.create_line(0,0,200,50)

        self.left_frame = Frame(self.top_frame, background='white')
        self.label_first_name = Label(self.left_frame, text='First Name: ', font=self.my_font, background='white').grid(
            row=0, column=0, stick=W, padx=10, pady=10)
        self.label_last_name = Label(self.left_frame, text='Last Name: ', font=self.my_font, background='white').grid(
            row=1, column=0, stick=W, padx=10, pady=10)
        self.address = Label(self.left_frame, text='Address: ', font=self.my_font, background='white').grid(row=2,
                                                                                                            column=0,
                                                                                                            stick=W,
                                                                                                            padx=10,
                                                                                                            pady=10)
        self.state = Label(self.left_frame, text='State: ', font=self.my_font, background='white').grid(row=3, column=0,
                                                                                                        stick=W,
                                                                                                        padx=10,
                                                                                                        pady=10)
        self.city = Label(self.left_frame, text='City: ', font=self.my_font, background='white').grid(row=4, column=0,
                                                                                                      stick=W, padx=10,
                                                                                                      pady=10)
        self.gst = Label(self.left_frame, text='GST Number: ', font=self.my_font, background='white').grid(row=5,
                                                                                                           column=0,
                                                                                                           stick=W,
                                                                                                           padx=10,
                                                                                                           pady=10)
        self.addhar = Label(self.left_frame, text='Addhar Card Number: ', font=self.my_font, background='white').grid(
            row=6, column=0, stick=W, padx=10, pady=10)
        self.pan = Label(self.left_frame, text='PAN Number: ', font=self.my_font, background='white').grid(row=7,
                                                                                                           column=0,
                                                                                                           stick=W,
                                                                                                           padx=10,
                                                                                                           pady=10)
        self.mobile = Label(self.left_frame, text='Mobile Number: ', font=self.my_font, background='white').grid(row=8,
                                                                                                                 column=0,
                                                                                                                 stick=W,
                                                                                                                 padx=10,
                                                                                                                 pady=10)
        self.left_frame.grid(row=1, column=0, padx=10, pady=10)

        self.f_n = StringVar()
        self.l_n = StringVar()
        self.add = StringVar()
        self.sta = StringVar()
        self.cit = StringVar()
        self.gs = StringVar()
        self.addh = StringVar()
        self.p = StringVar()
        self.mob = StringVar()
        self.right_frame = Frame(self.top_frame, background='white')
        self.efirst_name = ttk.Entry(self.right_frame, text='First Name: ', textvariable=self.f_n, font=self.my_font)
        self.efirst_name.grid(row=0, column=0, padx=10, pady=10, stick=W)
        self.elast_name = ttk.Entry(self.right_frame, text='Last Name: ', textvariable=self.l_n, font=self.my_font)
        self.elast_name.grid(row=1, column=0, stick=W, padx=10, pady=10)
        self.eaddress = ttk.Entry(self.right_frame, text='Address: ', textvariable=self.add, font=self.my_font)
        self.eaddress.grid(row=2, column=0, stick=W, padx=10, pady=10)
        self.estate = Combobox(self.right_frame, value=self.states, textvariable=self.sta, font=self.my_font)
        self.right_frame.option_add("*TCombobox*Listbox*Font", self.my_font)
        self.estate.set('Punjab')
        self.estate.grid(row=3, column=0, stick=W, padx=10, pady=10)
        self.ecity = ttk.Entry(self.right_frame, textvariable=self.cit, font=self.my_font)
        self.ecity.grid(row=4, column=0, stick=W, padx=10, pady=10)
        self.egst = ttk.Entry(self.right_frame, textvariable=self.gs, font=self.my_font)
        self.egst.grid(row=5, column=0, stick=W, padx=10, pady=10)
        self.eaddhar = ttk.Entry(self.right_frame, textvariable=self.addh, font=self.my_font)
        self.eaddhar.grid(row=6, column=0, stick=W, padx=10, pady=10)
        self.epan = ttk.Entry(self.right_frame, textvariable=self.p, font=self.my_font)
        self.epan.grid(row=7, column=0, stick=W, padx=10, pady=10)
        self.emobile = ttk.Entry(self.right_frame, textvariable=self.mob, font=self.my_font)
        self.emobile.grid(row=8, column=0, stick=W, padx=10, pady=10)
        self.right_frame.grid(row=1, column=1, padx=10, pady=10)
        self.top_frame.grid(row=2, column=0, padx=10, pady=10)

        self.bottom_frame = Frame(self.outerframe, background='white')
        self.save_button = Button(self.bottom_frame, text="Save", command=self.save)
        self.save_button.config(width=10, height=0, bg='#0d02cc', fg='white', font=self.font3)
        self.save_button.grid(row=0, column=0)
        self.cancel_button = Button(self.bottom_frame, text="Cancel", command=lambda: self.clear_cus('c', controller))
        self.cancel_button.config(width=10, height=0, bg='#b8010f', fg='white', font=self.font3)
        self.cancel_button.grid(row=0, column=1, padx=10)
        self.bottom_frame.grid(row=3, column=0, padx=10, pady=10)
        self.outerframe.pack(padx=10, pady=10)

        self.bind('<Control-s>', self.save)
        self.bind('<Control-e>', lambda: self.clear_cus('c', controller))

    def clear_cus(self, temp, controller):
        if temp == 'c':
            if not self.mob.get() or (self.mob.get() == " "):
                ans = messagebox.askyesno('Leave this window?', 'Do you want to Leave? ')
                if ans:
                    controller.show_frame(FirstWin)
                else:
                    pass
            if self.mob.get() != "":
                ans = messagebox.askyesno('Leave this window?', 'Your data is not saved. Do you want to continue? ')
                if ans:
                    self.search_entry.delete(first=0, last=0)
                    self.efirst_name.delete(first=0, last=100)
                    self.elast_name.delete(first=0, last=100)
                    self.eaddress.delete(first=0, last=100)
                    self.ecity.delete(first=0, last=100)
                    self.egst.delete(first=0, last=100)
                    self.eaddhar.delete(first=0, last=100)
                    self.emobile.delete(first=0, last=100)
                    self.epan.delete(first=0, last=100)
                    self.estate.set('Punjab')
                    controller.show_frame(FirstWin)

        else:
            self.search_entry.delete(first=0, last=100)
            self.efirst_name.delete(first=0, last=100)
            self.elast_name.delete(first=0, last=100)
            self.eaddress.delete(first=0, last=100)
            self.ecity.delete(first=0, last=100)
            self.egst.delete(first=0, last=100)
            self.eaddhar.delete(first=0, last=100)
            self.emobile.delete(first=0, last=100)
            self.epan.delete(first=0, last=100)
            self.estate.set('Punjab')

    def save(self, event=0):
        CustomerEdit.customer_dir = {'first_name': self.f_n.get().lower(), "last_name": self.l_n.get().lower(),
                                     'address': self.add.get(), 'state': self.sta.get(),
                                     'city': self.cit.get().lower(),
                                     "gst_number": self.gs.get(), 'addhar_card_number': self.addh.get(),
                                     'pan_number': self.p.get(),
                                     'phone_number': self.mob.get()}
        k = CustomerEdit.customer_dir.values()
        check = Validate.basic_check(k)

        if check == "al":
            messagebox.showinfo("NO DATA", "Enter data before saving it.")
        elif check == "fi":
            messagebox.showinfo("MISSING DATA", "Enter first name of the customer.")
        elif check == "la":
            messagebox.showinfo("MISSING DATA", "Enter the last name of the customer")
        elif check == "ad" or check == "st":
            messagebox.showinfo("MISSING DATA", "Enter address or state of the customer.")
        elif check == "ci":
            messagebox.showinfo("MISSING DATA", "Enter the city from where the customer is.")
        else:
            g = Validate.check(CustomerEdit.customer_dir)
            if 0 in g:
                messagebox.showerror("Error", 'GST/PAN/Addhar/Phone filled wrong')
            else:
                try:
                    InDeUp.update_to_database_customer(CustomerEdit.customer_dir, CustomerEdit.my_db,
                                                       self.search_data.get())
                    messagebox.showinfo("Uploaded", 'Data Saved Successfully')
                    self.clear_search_data()
                    self.clear_cus('s', None)
                    # SeaofBTCapp.show_frame(FirstWin, 0)
                except Exception:
                    messagebox.showwarning("Exists", 'Data already exists')

    # def cancel(self, event=0):
    #     ans = messagebox.askyesno('Leave this window?', 'Your data is not saved')
    #     if ans:
    #         pass
    #     else:
    #         pass

    # def redirect(self, event=0):
    #     self.outerframe.pack_forget()
    #     self.window.config(menu="")


class ItemEdit(tk.Frame):
    item_dir = {}
    try:
        my_db = DBConnection.get_connection()
    except Exception:
        messagebox.showerror("Connection Error", 'Database in not connected')

    def clear_search_data(self):
        self.eitem_id.delete(0, END)
        self.eitem_name.delete(0, END)
        self.eprice.delete(0, END)
        self.egstp.delete(0, END)
        self.ehsn.delete(0, END)

    def search_details(self):
        if self.search_data.get() == "" or self.search_data.get() == " ":
            messagebox.showinfo("EMPTY", "No mobile number entered:")
        # clear entry box
        else:
            get_data = InDeUp.search_data_item(self.search_data.get(), ItemEdit.my_db)

            # clear search box
            self.clear_search_data()

            try:
                self.eitem_id.insert(0, get_data[0])
                self.eitem_name.insert(0, get_data[1])
                self.eprice.insert(0, get_data[2])
                self.egstp.insert(0, get_data[3])
                self.ehsn.insert(0, get_data[4])
            except Exception:
                messagebox.showerror("Error", "Check Item id")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.window = window
        # self.window.title('EditDetails')
        # self.window.geometry("{0}x{1}+0+0".format(self.window.winfo_screenwidth(), root.winfo_screenheight()))
        # self.window.configure(background='white')

        self.gss = ['5', '12', '18', '28']
        self.my_font = Font(family='Times New Roman', size=18)
        self.font2 = Font(family='Times New Roman', size=22, weight='bold')
        self.font3 = Font(family='Times New Roman', size=12)

        # self.main_menu = Menu(self)
        # self.config(menu=self.main_menu)
        # self.file_menu = Menu(self.main_menu)
        # self.main_menu.add_cascade(label='File', menu=self.file_menu)
        # self.file_menu.add_command(label='Save   Ctrl+S', command=self.save)
        # self.file_menu.add_command(label='Cancel   Ctrl+E', command=self.cancel)
        #
        # self.goto_menu = Menu(self.main_menu)
        # self.main_menu.add_cascade(label='Goto', menu=self.goto_menu)
        # self.goto_menu.add_command(label='Home', command=self.redirect)      # make changes in command (redirect to home page)

        self.outerframe = LabelFrame(self, background='white')
        self.name = Label(self.outerframe, text='Edit Items Details', font=self.font2, background='white')
        self.name.grid(row=0, column=0, padx=10, pady=30)

        self.top_frame = Frame(self.outerframe, background='white')
        self.left_frame = Frame(self.top_frame, background='white')
        self.search_lb_frame = LabelFrame(self.outerframe, background='white')
        # Search bar for the editing details of customer
        self.search_data = StringVar()
        self.search_label = Label(self.search_lb_frame, background='white', text='Search using Item No.',
                                  font=self.my_font).grid(row=0, column=0, stick=W, padx=10, pady=10)
        self.search_entry = ttk.Entry(self.search_lb_frame, textvariable=self.search_data, font=self.my_font)
        self.search_entry.grid(row=0, column=1, stick=W, padx=10, pady=10)
        self.search_lb_frame.grid(row=1, padx=10)
        self.img_search = Image.open("..\\image\\search.png")
        self.img_search = self.img_search.resize((25, 25), Image.ANTIALIAS)
        self.image_search = ImageTk.PhotoImage(self.img_search)
        self.image_button = Button(self.search_lb_frame, bd=2, command=self.search_details, image=self.image_search)
        self.image_button.config(width=25, height=25, cursor="hand2")
        self.image_button.grid(row=0, column=2, padx=10, pady=10)
        self.image_button.bind()
        self.item_id = Label(self.left_frame, text='Item Id: ', font=self.my_font, background='white').grid(row=0,
                                                                                                            column=0,
                                                                                                            stick=W,
                                                                                                            padx=10,
                                                                                                            pady=10)
        self.item_name = Label(self.left_frame, text='Item Name: ', font=self.my_font, background='white').grid(row=1,
                                                                                                                column=0,
                                                                                                                stick=W,
                                                                                                                padx=10,
                                                                                                                pady=10)
        self.price = Label(self.left_frame, text='Price ', font=self.my_font, background='white').grid(row=2, column=0,
                                                                                                       stick=W, padx=10,
                                                                                                       pady=10)
        self.gstp = Label(self.left_frame, text='GST(%): ', font=self.my_font, background='white').grid(row=3, column=0,
                                                                                                        stick=W,
                                                                                                        padx=10,
                                                                                                        pady=10)
        self.hsn = Label(self.left_frame, text='HSN code: ', font=self.my_font, background='white').grid(row=4,
                                                                                                         column=0,
                                                                                                         stick=W,
                                                                                                         padx=10,
                                                                                                         pady=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        self.i_d = StringVar()
        self.i_n = StringVar()
        self.p = StringVar()
        self.g = StringVar()
        self.h = StringVar()
        self.right_frame = Frame(self.top_frame, background='white')
        self.eitem_id = ttk.Entry(self.right_frame, textvariable=self.i_d, font=self.my_font)
        self.eitem_id.grid(row=0, column=0, stick=W, padx=10, pady=10)
        self.eitem_name = ttk.Entry(self.right_frame, textvariable=self.i_n, font=self.my_font)
        self.eitem_name.grid(row=1, column=0, stick=W, padx=10, pady=10)
        self.eprice = ttk.Entry(self.right_frame, textvariable=self.p, font=self.my_font)
        self.eprice.grid(row=2, column=0, stick=W, padx=10, pady=10)
        self.egstp = Combobox(self.right_frame, value=self.gss, textvariable=self.g, font=self.my_font)
        self.right_frame.option_add("*TCombobox*Listbox*Font", self.my_font)
        self.egstp.set('5')
        self.egstp.grid(row=3, column=0, stick=W, padx=10, pady=10)
        self.ehsn = ttk.Entry(self.right_frame, textvariable=self.h, font=self.my_font)
        self.ehsn.grid(row=4, column=0, stick=W, padx=10, pady=10)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)
        self.top_frame.grid(row=2, column=0, padx=10, pady=10)

        self.bottom_frame = Frame(self.outerframe, pady=30, background='white')
        self.save_button = Button(self.bottom_frame, text="Save", command=self.save)
        self.save_button.config(width=10, height=0, bg='#0d02cc', fg='white', font=self.font3)
        self.save_button.grid(row=0, column=0, padx=10, pady=10)
        self.cancel_button = Button(self.bottom_frame, text="Cancel", command=lambda: controller.show_frame(FirstWin))
        self.cancel_button.config(width=10, height=0, bg='#b8010f', fg='white', font=self.font3)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)
        self.bottom_frame.grid(row=3, column=0, padx=10, pady=10)
        self.outerframe.pack(padx=10, pady=10)

        self.bind('<Control-s>', self.save)
        self.bind('<Control-e>', lambda: controller.show_frame(FirstWin))

    def clear_item(self, temp, controller):
        if temp == 'c':
            if not self.i_d.get() or (self.i_d.get() == " "):
                ans = messagebox.askyesno('Leave this window?', 'Do you want to Leave? ')
                if ans:
                    controller.show_frame(FirstWin)
                else:
                    pass
            if self.i_d.get() != "":
                ans = messagebox.askyesno('Leave this window?', 'Your data is not saved. Do you want to continue? ')
                if ans:
                    self.search_entry.delete(first=0, last=END)
                    self.egstp.set('5')
                    self.eitem_id.delete(first=0, last=END)
                    self.eitem_name.delete(first=0, last=END)
                    self.eprice.delete(first=0, last=END)
                    self.ehsn.delete(first=0, last=END)
                    controller.show_frame(FirstWin)

        else:
            self.search_entry.delete(first=0, last=END)
            self.egstp.set('5')
            self.eitem_id.delete(first=0, last=END)
            self.eitem_name.delete(first=0, last=END)
            self.eprice.delete(first=0, last=END)
            self.ehsn.delete(first=0, last=END)

    def save(self, event=0):
        ItemEdit.item_dir = {'item_id': self.i_d.get().strip(), "item_name": self.i_n.get().strip(),
                             'price': self.p.get().strip(), 'gst_per': self.g.get(),
                             'hsn_code': self.h.get().strip()}
        k = ItemEdit.item_dir.values()
        check = Validate.basic_check(k)
        if check == "al":
            messagebox.showinfo("NO DATA", "Enter data before saving it.")
        elif check == "fi":
            messagebox.showinfo("MISSING DATA", "Enter item ID of the Item.")
        elif check == "la":
            messagebox.showinfo("MISSING DATA", "Enter the Item name of the Item.")
        elif check == "ad":
            messagebox.showinfo("MISSING DATA", "Enter price of the Item.")
        elif check == "st":
            messagebox.showinfo("MISSING DATA", "Enter the gst percent of the Item.")
        else:
            try:
                InDeUp.update_to_database_item(ItemEdit.item_dir, ItemEdit.my_db, self.search_entry.get())
                messagebox.showinfo("Uploaded", 'Data Saved Successfully')
                self.clear_item('s', None)
                # SeaofBTCapp.show_frame(FirstWin, 0)
                # messagebox.askyesno("New Customer Updation", "")
            except Exception:
                messagebox.showwarning("Exists", 'Data already exists')


class CreateBill(tk.Frame):
    j = 0
    transport_detail_dict = []
    main_list = []
    customer_list = []
    price_list = []
    total_price = 0
    discount_price = 0
    total_sgst = 0
    total_cgst = 0
    total_igst = 0
    grand_total = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.i = 0
        # Frame for Interface
        self.frame = LabelFrame(self, width=950, height=800)

        # Invoice Label
        self.inv = Label(self.frame, text="Invoice No.", font=("Arial", 10))
        self.inv.place(x=20, y=10)

        # Invoice Number
        self.invno = Label(self.frame, text="1 ", font=("Arial", 10))
        self.invno.place(x=90, y=10)

        # Date
        self.add_date = Label(self.frame, text="Date : ", font=("Arial", 10))
        self.add_date.place(x=800, y=10)
        self.date = datetime.date.today()
        self.da = StringVar()
        self.get_date = Label(self.frame, text=self.date, font=("Arial", 10))
        self.get_date.place(x=850, y=10)

        # mobile number

        self.mobile_first_label = Label(self.frame, text="Mobile No.", font=("Arial", 10))
        self.mobile_first_label.place(x=20, y=55)
        self.first_mobile_entrybox = Entry(self.frame, bd=2)
        self.first_mobile_entrybox.place(x=95, y=55)

        # State
        self.state_label = Label(self.frame, text="State ", font=("Arial", 10))
        self.state_label.place(x=345, y=55)
        self.state_label_entrybox = Entry(self.frame, bd=2)
        self.state_label_entrybox.place(x=395, y=55)
        self.first_cutomerLabel = Label(self.frame, text="Customer Name : ", font=("Arial", 10))
        self.first_cutomerLabel.place(x=20, y=85)
        self.get_cutomername = Label(self.frame, text=" ", font=("Arial", 10))
        self.get_cutomername.place(x=130, y=85)
        # Shipment
        self.check_checkbutton1 = BooleanVar()
        self.check_checkbutton1.set(True)
        self.chk = Checkbutton(self.frame, text=" Same Shipment Address ", variable=self.check_checkbutton1,
                               font=("Arial", 10), command=self.check)
        self.chk.place(x=20, y=110)
        self.mobile_second_label = Label(self.frame, text="Mobile Number ", font=("Arial", 10), bd=2)
        self.mobile_second_label.place(x=30, y=140)
        self.get_second_mobile = Entry(self.frame, state='disabled')
        self.get_second_mobile.place(x=140, y=140)

        # Customer Label
        self.first_cutomerLabel = Label(self.frame, text="Customer Name : ", font=("Arial", 10))
        self.first_cutomerLabel.place(x=30, y=165)
        self.second_customername = Label(self.frame, text=" ", font=("Arial", 10))
        self.second_customername.place(x=150, y=165)

        # Address Label
        self.customer_address = Label(self.frame, text="Address : ", font=("Arial", 10))
        self.customer_address.place(x=30, y=188)
        self.first_cutomerLabel_add = Label(self.frame, text=" ", font=("Arial", 10))
        self.first_cutomerLabel_add.place(x=120, y=188)

        # Canvas1  Input Item code and rest details and add it to the another canvas
        self.it = StringVar()
        self.qt = StringVar()
        self.unitprice_labelp = StringVar()
        self.discount_labels = StringVar()
        self.sgst_labelg = StringVar()
        self.cgst_labelg = StringVar()
        self.igst_labelg = StringVar()
        self.totalprice_labelp = StringVar()
        self.product_labelo = StringVar()
        self.hsn_no = StringVar()
        # Canvas1
        self.canvas2vas1 = Canvas(self.frame, height=120, width=900)
        self.canvas2vas1.place(x=10, y=210)
        # Creating Rectangle
        self.canvas2vas1.create_rectangle(3, 3, 900, 75, fill="light grey")

        # ItemCode Label
        self.item_label = Label(self.canvas2vas1, text="Item Code", bg="light grey", font=("Arial", 10))
        self.item_label.place(x=10, y=15)
        # ItemCode Entry Box
        self.item_entrybox = Entry(self.canvas2vas1, width=10, bd="2", textvariable=self.it)
        self.item_entrybox.place(x=11, y=43)

        # Quantity Label
        self.quantity = Label(self.canvas2vas1, text="Qty", bg="light grey", font=("Arial", 10))
        self.quantity.place(x=110, y=15)
        # Quantity Entry Box
        self.quantity_entrybox = Entry(self.canvas2vas1, width=10, bd="2", textvariable=self.qt)
        self.quantity_entrybox.place(x=90, y=43)

        # UnitPrice Label
        self.unitprice_label = Label(self.canvas2vas1, text="Unit Price", bg="light grey", font=("Arial", 10))
        self.unitprice_label.place(x=190, y=15)
        # UnitPrice Entry BOx
        self.unitprice_entrybox = Entry(self.canvas2vas1, width=15, bd="2", textvariable=self.unitprice_labelp)
        self.unitprice_entrybox.place(x=170, y=43)

        # Discount Label
        self.discount_label = Label(self.canvas2vas1, text="Discount %", bg="light grey", font=("Arial", 10))
        self.discount_label.place(x=290, y=15)
        # Discount Entry BOx
        self.discount_entrybox = Entry(self.canvas2vas1, width=15, bd="2", textvariable=self.discount_labels)
        self.discount_entrybox.place(x=280, y=43)

        # Tab key on Quantity Entry BOx
        self.item_entrybox.bind("<Tab>", self.item_pass)
        # Tab key on Total Price BOx
        self.discount_entrybox.bind("<Tab>", self.Discount)
        self.first_mobile_entrybox.bind("<Tab>", self.mobile_pass)
        self.get_second_mobile.bind("<Tab>", self.shipment_mobile)

        # SGST Label
        self.sgst_label = Label(self.canvas2vas1, text="SGST", bg="light grey", font=("Arial", 10))
        self.sgst_label.place(x=400, y=15)
        # SGST Entry BOx
        self.sgst_entrybox = Entry(self.canvas2vas1, width=10, bd="2", textvariable=self.sgst_labelg)
        self.sgst_entrybox.place(x=390, y=43)

        # CGST Label
        self.cgst_label = Label(self.canvas2vas1, text="CGST", bg="light grey", font=("Arial", 10))
        self.cgst_label.place(x=480, y=15)
        # CGST Entry Box
        self.cgst_entrybox = Entry(self.canvas2vas1, width=10, bd="2", textvariable=self.cgst_labelg)
        self.cgst_entrybox.place(x=470, y=43)

        # IGST Label
        self.igst_label = Label(self.canvas2vas1, text="IGST", bg="light grey", font=("Arial", 10))
        self.igst_label.place(x=560, y=15)
        # IGST Entry BOx
        self.igst_entrybox = Entry(self.canvas2vas1, width=10, bd="2", textvariable=self.igst_labelg)
        self.igst_entrybox.place(x=550, y=43)

        # TotalPrice Label
        self.totalprice_label = Label(self.canvas2vas1, text="T Price ", bg="light grey", font=("Arial", 10))
        self.totalprice_label.place(x=640, y=15)
        # TotalPrice Entry Box
        self.totalprice_entrybox = Entry(self.canvas2vas1, width=10, bd="2", textvariable=self.totalprice_labelp)
        self.totalprice_entrybox.place(x=630, y=43)

        # Product Label
        self.product_label = Label(self.canvas2vas1, text="Product Name", bg="light grey", font=("Arial", 10))
        self.product_label.place(x=715, y=15)
        # Product Entry box
        self.product_entrybox = Entry(self.canvas2vas1, width=10, bd="2", textvariable=self.product_labelo)
        self.product_entrybox.place(x=720, y=43)

        # Add Button
        self.plus = Button(self.canvas2vas1, text="+", bd=2, bg="orange", fg="white", width=2, height=1,
                           font=("Arial bold", 10), padx=4, pady=4, command=self.save)
        self.plus.place(x=800, y=35)
        # minus Button
        self.plus = Button(self.canvas2vas1, text="--", bd=2, bg="orange", fg="white", width=2, height=1,
                           font=("Arial bold", 10), padx=4, pady=4, command=self.remove_item_tv)
        self.plus.place(x=850, y=35)

        # Canvas2 display
        # Just Display all the labels in sky blue color
        self.canvas_frame = Frame(self.frame, height=265, width=890)
        # Scroll option
        # self.scroll = Scrollbar(self.canvas_frame)
        # ttk.Treeview(anchor=tkinter.E)
        self.billstree = ttk.Treeview(self.canvas_frame, height=12,
                                      columns=('', 'Item Code', 'Product Name', 'Qty', 'Unit Price', 'Discount %'
                                                                                                     'SGST', 'CGST',
                                               'IGST', 'Total Price'), show='headings')

        self.billstree.column("#0", width=60, minwidth=60)
        # self.billstree.column("#1", width=60, minwidth=60)
        self.billstree.column("#1", width=80, minwidth=80)
        self.billstree.column("#2", width=170, minwidth=150)
        self.billstree.column("#3", width=70, minwidth=60)
        self.billstree.column("#4", width=80, minwidth=70)
        self.billstree.column("#5", width=70, minwidth=50)
        self.billstree.column("#6", width=70, minwidth=50)
        self.billstree.column("#7", width=60, minwidth=50)
        self.billstree.column("#8", width=80, minwidth=70)
        self.billstree.column("#9", width=80, minwidth=70)
        # self.billstree.grid(row=0, column=0, columnspan=18)
        self.billstree.column("#0", width=60, minwidth=60)
        # self.billstree.heading('#1', text="S. No.")
        self.billstree.heading('#1', text="Item Code")
        self.billstree.heading('#2', text="Product Name")
        self.billstree.heading('#3', text="Qty")
        self.billstree.heading('#4', text="Unit Price")
        self.billstree.heading('#5', text="Discount %")
        self.billstree.heading('#6', text="SGST")
        self.billstree.heading('#7', text="CGST")
        self.billstree.heading('#8', text="IGST")
        self.billstree.heading('#9', text="Total Price")
        self.billstree.pack(padx=50)
        self.canvas_frame.place(x=10, y=300)

        # Transport Details
        self.check_checkbutton2 = BooleanVar()
        self.check_checkbutton2.set(True)
        self.chk1 = Checkbutton(self.frame, text=" Transport Details  ", variable=self.check_checkbutton2,
                                font=("Arial", 10), command=self.trans)
        self.chk1.place(x=20, y=580)

        # Transport Name
        self.get_transname = StringVar()
        self.transport_name_label = Label(self.frame, text="Name ", font=("Arial", 10))
        self.transport_name_label.place(x=25, y=610)
        # TransportName Entry Box
        self.transport_name_entrybox = Entry(self.frame, state="disabled", textvariable=self.get_transname)
        self.transport_name_entrybox.place(x=100, y=610)

        # Address
        self.get_transadd = StringVar()
        self.transport_address_label = Label(self.frame, text="Address ", font=("Arial", 10))
        self.transport_address_label.place(x=25, y=640)
        # Address Entry BOx
        self.transport_address_entrybox = Entry(self.frame, width=20, state="disabled", text=self.get_transadd)
        self.transport_address_entrybox.place(x=100, y=640)

        # VehicleDetails
        self.transvec = StringVar()
        self.vehicle_label = Label(self.frame, text="Vehicle No. ", font=("Arial", 10))
        self.vehicle_label.place(x=25, y=670)
        # Total costing
        # self.total_price_var = StringVar()
        self.total_price_to_pay = Label(self.frame, text=" Total Price: ", font=("Arial", 10))
        self.total_price_to_pay.place(x=675, y=580)
        self.total_price_entry = Entry(self.frame)
        self.total_price_entry.place(x=800, y=580)

        # SGST costing
        self.total_sgst_price = Label(self.frame, text=" SGST: ", font=("Arial", 10))
        self.total_sgst_price.place(x=675, y=600)
        self.total_sgst_entry = Entry(self.frame)
        self.total_sgst_entry.place(x=800, y=600)

        # CGST costing
        self.total_cgst_price = Label(self.frame, text=" CGST: ", font=("Arial", 10))
        self.total_cgst_price.place(x=675, y=620)
        self.total_cgst_entry = Entry(self.frame)
        self.total_cgst_entry.place(x=800, y=620)

        # IGST costing
        self.total_igst_price = Label(self.frame, text=" IGST: ", font=("Arial", 10))
        self.total_igst_price.place(x=675, y=640)
        self.total_igst_entry = Entry(self.frame)
        self.total_igst_entry.place(x=800, y=640)

        # Grand Total
        self.grand_total_price = Label(self.frame, text=" Grand Total: ", font=("Arial", 10))
        self.grand_total_price.place(x=675, y=660)
        self.grand_total_entry = Entry(self.frame)
        self.grand_total_entry.place(x=800, y=660)

        # Vehicle Entry box
        self.vehicle_enrtybox = Entry(self.frame, state="disabled", textvariable=self.transvec)
        self.vehicle_enrtybox.place(x=100, y=690)
        # Cancel Button
        self.cancel = Button(self.frame, text="Cancel Bill ", command=lambda: controller.show_frame(FirstWin), bd=2,
                             bg="sky blue",
                             fg="white", width=10, height=1, font=("Arial bold", 10), padx=4, pady=4)
        self.cancel.place(x=800, y=700)

        # Generate Button
        self.generate = Button(self.frame, text="Generate Bill ", command=self.generate, bd=2, bg="sky blue",
                               fg="white", width=10, height=1, font=("Arial bold", 10), padx=4, pady=4)
        self.generate.place(x=675, y=700)

        self.frame.pack()

    def generate(self):
        self.get_mobile_no = self.first_mobile_entrybox.get()
        self.get_mobile_num = self.get_second_mobile.get()
        if len(CreateBill.main_list) < 1:
            messagebox.showwarning("Warning", "Please insert at-least one item in the bill.")

        elif self.get_mobile_no == "":
            messagebox.showwarning("Warning", "Please Enter valid mobile no.")
        elif (len(self.get_mobile_no) > 10) or (len(self.get_mobile_no) < 10):
            messagebox.showwarning("Warning", "Please Enter valid Mobile Number(must be of length 10)")
        # # elif(len(self.get_mobile_num)>10) or (len(self.get_mobile_num)<10):
        # # messagebox.showwarning("Warning","Please Enter valid Mobile Number(must be of length 10)")
        # elif self.item_entrybox.get() == "":
        #     messagebox.showwarning("Warning","Please Enter item Code")
        # # elif(self.quantity_entrybox.get()==""):
        # #    messagebox.showwarning("Warning","Please Enter Quantity")
        else:
            temp = messagebox.askquestion("Confirm", "Are you Sure to generate bill")
            if temp == "yes":
                CreateBill.transport_detail_dict = [self.get_transname.get(), self.get_transadd.get(),
                                                    self.transvec.get()]
                print(CreateBill.transport_detail_dict)
                CreateBill.customer_list.append(InterBilling.mobile_search_full(self.get_first_mobile))
                if self.get_second_mobile != "":
                    CreateBill.customer_list.append(InterBilling.mobile_search_full(self.get_second_mobile.get()))
                    print(CreateBill.customer_list)
                # SeaofBTCapp.show_frame(FirstWin, 0)
            else:
                pass
        print("********************************")
        print(CreateBill.main_list)
        print(CreateBill.transport_detail_dict)
        print(CreateBill.customer_list)
        print(CreateBill.price_list)

        ExcelToPdf.make_pdf_file(CreateBill.main_list, CreateBill.transport_detail_dict, CreateBill.customer_list, CreateBill.price_list)
        CreateBill.main_list.clear()
        CreateBill.transport_detail_dict.clear()
        CreateBill.customer_list.clear()
        CreateBill.price_list.clear()

    def shipment_mobile(self, event=0):
        if self.get_second_mobile.get() == "" or self.get_second_mobile.get() == " ":
            messagebox.showinfo("EMPTY", "No mobile number entered:")
        # clear entry box
        else:
            lst = InterBilling.mobile_search(self.get_second_mobile.get())
            self.final_custom = lst[1] + " " + lst[2]

            self.second_customername.configure(text=self.final_custom)
            self.final_add = lst[3]
            self.first_cutomerLabel_add.configure(text=self.final_add)
            if self.final == self.final_custom:
                print("Yes")
            else:
                print("no")

    def check(self):
        if self.get_second_mobile['state'] == 'normal':
            self.get_second_mobile['state'] = 'disabled'

        else:
            self.get_second_mobile['state'] = 'normal'

    # def getpr(self):
    #     InterBilling.print_list(CreateBill.main_list)

    def mobile_pass(self, event=0):
        if self.first_mobile_entrybox.get() == "" or self.first_mobile_entrybox.get() == " ":
            messagebox.showinfo("EMPTY", "No mobile number entered:")
        # clear entry box
        else:
            self.get_first_mobile = self.first_mobile_entrybox.get()
            list = InterBilling.mobile_search(self.get_first_mobile)
            print(type(list))
            if (len(self.get_first_mobile) < 10) or (len(self.get_first_mobile) > 10):
                messagebox.showwarning("Warning", "Please Enter a valid mobile number")
            # elif(type(list)=="<class 'NoneType'>"):
            #     messagebox.showwarning("Warning","Invalid Entry in database")
            self.state_label_entrybox.delete(first=0, last=END)
            self.equivalent_state = list[4]
            self.state_label_entrybox.insert(END, self.equivalent_state)
            self.final = list[1] + " " + list[2]
            self.get_cutomername.configure(text=self.final)
            self.second_customername.configure(text=self.final)
            self.final_add = list[3]
            self.first_cutomerLabel_add.configure(text=self.final_add)

    # Searching

    def item_pass(self, event=0):
        # print(self.item_entrybox.get())
        self.unitprice_entrybox.delete(first=0, last=END)
        self.product_entrybox.delete(first=0, last=END)

        self.sgst_entrybox.delete(first=0, last=END)
        self.cgst_entrybox.delete(first=0, last=END)
        try:
            self.get_state = self.state_label_entrybox.get()
            self.lower_state = self.get_state.lower()
            main_list = InterBilling.id_search(self.item_entrybox.get())
            self.qp = main_list[2]
            self.unitprice_entrybox.insert(END, self.qp)
            self.pn = main_list[1]
            self.product_entrybox.insert(END, self.pn)
            self.gst_get = main_list[3]
            self.hsn_code = main_list[4]
            if (self.lower_state == "punjab"):
                self.divide_gst = int(self.gst_get) / 2
                self.cgst_entrybox.insert(END, float(self.divide_gst))
                self.sgst_entrybox.insert(END, float(self.divide_gst))
            else:
                self.igst_entrybox.delete(first=0, last=END)
                self.igst_entrybox.insert(END, self.gst_get)
        except ValueError:
            messagebox.showwarning("Warning:", "Item code field left empty.")
        except Exception:
            messagebox.showwarning("Warning", "Invalid Entry in Database")

    # Discount Calculate
    def Discount(self, event=0):
        try:
            # if self.total_price_entry
            self.total_price_entry.configure(state="normal")
            self.total_sgst_entry.configure(state="normal")
            self.total_cgst_entry.configure(state="normal")
            self.total_igst_entry.configure(state="normal")
            self.grand_total_entry.configure(state="normal")
            self.total_price_entry.delete(0, END)
            self.total_sgst_entry.delete(0, END)
            self.total_cgst_entry.delete(0, END)
            self.total_igst_entry.delete(0, END)
            self.grand_total_entry.delete(0, END)

            self.totalprice_entrybox.delete(first=0, last=END)
            self.unitprice_labelpi = self.unitprice_labelp.get()
            self.discount_labelsi = self.discount_labels.get()
            # Discount find out
            self.get_quantity = int(self.quantity_entrybox.get())
            print(self.get_quantity)
            print(self.unitprice_labelpi)
            print(self.discount_labelsi)

            self.qn = (int(self.unitprice_labelpi) * self.get_quantity)
            CreateBill.total_price = CreateBill.total_price + self.qn
            self.f = (self.qn / 100) * int(self.discount_labelsi)
            # CreateBill.discount_price = CreateBill.discount_price + self.f
            self.totalprice_labelm = int(self.qn) - self.f
            self.a = (int(self.gst_get))
            self.final_val = self.totalprice_labelm * self.a
            self.final_value = self.final_val / 100
            if self.lower_state == "punjab":
                self.divide_gst = int(self.final_value) / 2
                CreateBill.total_sgst = CreateBill.total_sgst + self.final_value
                CreateBill.total_cgst = CreateBill.total_cgst + self.final_value
            else:
                CreateBill.total_igst = CreateBill.total_igst + self.final_value
            self.fin = int(self.totalprice_labelm) + self.final_value
            CreateBill.grand_total = CreateBill.grand_total + self.fin
            self.totalprice_entrybox.insert(END, self.fin)
            self.total_sgst_entry.insert(END, self.total_sgst)
            self.total_igst_entry.insert(END, self.total_igst)
            self.total_cgst_entry.insert(END, self.total_cgst)
            self.total_price_entry.insert(END, self.total_price)
            self.grand_total_entry.insert(END, self.grand_total)
            self.total_price_entry.configure(state="disabled")
            self.total_sgst_entry.configure(state="disabled")
            self.total_cgst_entry.configure(state="disabled")
            self.total_igst_entry.configure(state="disabled")
            self.grand_total_entry.configure(state="disabled")

        except Exception:
            messagebox.showwarning("Warning", "Discount value left empty")

    def trans(self):
        if ((self.transport_name_entrybox['state'] == 'normal') and (
                self.transport_address_entrybox['state'] == 'normal') and
                (self.vehicle_enrtybox['state'] == 'normal')):
            self.transport_name_entrybox['state'] = 'disabled'
            self.transport_address_entrybox['state'] = 'disabled'
            self.vehicle_enrtybox['state'] = 'disabled'
        else:
            self.transport_name_entrybox['state'] = 'normal'
            self.transport_address_entrybox['state'] = 'normal'
            self.vehicle_enrtybox['state'] = 'normal'

    def save(self):
        try:
            print("mksmkxmsk", self.item_entrybox.get(), "csmmks")
            if (self.item_entrybox.get() == "") and (self.quantity_entrybox.get() == "") and (
                    self.unitprice_entrybox.get() == "") \
                    and (self.discount_entrybox.get() == "") and (self.totalprice_entrybox.get() == "") and (
                    (self.sgst_entrybox.get() == "") or
                    (self.igst_entrybox.get() == "") or (self.cgst_entrybox.get() == "")):
                raise Exception
            else:
                self.control = 1

        except Exception:
            messagebox.showwarning("Warning", "Please fill all the fields")

        self.i = self.i + 25
        if self.control == 1:
            # Get Entry BOx Values
            self.iti = self.it.get()
            self.qti = self.qt.get()
            self.unitprice_labelpi = self.unitprice_labelp.get()
            self.discount_labelsi = self.discount_labels.get()
            self.sgst_labelgi = self.sgst_labelg.get()
            self.cgst_labelgi = self.cgst_labelg.get()
            self.igst_labelgi = self.igst_labelg.get()
            self.totalprice_labelpi = self.totalprice_labelp.get()
            self.product_labeli = self.product_labelo.get()

            if (self.item_entrybox.get() == "") and (self.quantity_entrybox.get() == "") and (
                    self.unitprice_entrybox.get() == "") \
                    and (self.discount_entrybox.get() == "") and (self.totalprice_entrybox.get() == "") and (
                    (self.sgst_entrybox.get() == "") or
                    (self.igst_entrybox.get() == "") or (self.cgst_entrybox.get() == "")):
                pass
            else:

                self.billstree.insert("", CreateBill.j, CreateBill.j, values=(
                self.iti, self.product_labeli, self.qti, self.unitprice_labelpi, self.discount_labelsi,
                self.sgst_labelgi, self.cgst_labelgi, self.igst_labelgi, self.totalprice_labelpi))
                CreateBill.j += 1
                self.dictionary()

            self.item_entrybox.delete(first=0, last=END)
            self.quantity_entrybox.delete(first=0, last=END)
            self.unitprice_entrybox.delete(first=0, last=END)
            self.discount_entrybox.delete(first=0, last=END)
            self.cgst_entrybox.delete(first=0, last=END)
            self.sgst_entrybox.delete(first=0, last=END)
            self.igst_entrybox.delete(first=0, last=END)
            self.totalprice_entrybox.delete(first=0, last=END)
            self.product_entrybox.delete(first=0, last=END)

    # def get_inputvalue_dic(self):
    #    temp_dic = {'item id': self.it.get(),'Quantity':self.qt.get(),'Unit Price':self.unitprice_labelp.get(),'Discount':self.discount_labels.get(),'sgst':self.sgst_labelg.get(),'cgst':self.cgst_labelg.get()
    #         ,'igst':self.igst_labelg.get(),'total price':self.totalprice_labelp.get(),'product name':self.product_labelo.get()}
    #    main_list.append(temp_dic)
    # print(main_list)

    # self.first_cutomerLabel(first customer name label)
    # self.second_customername(second customer name label)
    # self.customer_address(customer address label)
    # Adhar card n all (use from function mobile_pass method)
    def remove_item_tv(self):
        selected_item = self.billstree.selection()[0]
        # print(selected_item)
        try:
            # CreateBill.main_list.pop(int(selected_item))
            self.billstree.delete(selected_item)
            # print(self.billstree.getvar('S. No.'))
            # temp = 0

            # for i in CreateBill.main_list:
            #     temp += 1
            #     i['S. No.'] = temp

            #     self.billstree.insert("",temp,temp, values=(i['S. No.'], i['item id'], i['product name'],
            #                             i['Quantity'], i['Unit Price'], i['Discount'], i['sgst'], i['cgst']
            #                             , i['igst'], i['total price']))
            #     temp += 1
        except Exception:
            pass
            # print(CreateBill.main_list)
        del selected_item
        CreateBill.main_list = self.billstree.get_children()


    def dictionary(self):
        if (self.item_entrybox.get() == "") and (self.quantity_entrybox.get() == "") and (
                self.unitprice_entrybox.get() == "") \
                and (self.discount_entrybox.get() == "") and (self.totalprice_entrybox.get() == "") and (
                (self.sgst_entrybox.get() == "") or
                (self.igst_entrybox.get() == "") or (self.cgst_entrybox.get() == "")):
            pass
        else:
            temp_dic = [self.it.get(), self.product_labelo.get(), self.hsn_code, self.qt.get(),
                        self.unitprice_labelp.get(), self.discount_labels.get(), self.sgst_labelg.get(),
                        self.cgst_labelg.get(),
                        self.igst_labelg.get(), self.totalprice_labelp.get()]
            CreateBill.main_list.append(temp_dic)
        self.total_price_entry.configure(state="normal")
        self.total_sgst_entry.configure(state="normal")
        self.total_cgst_entry.configure(state="normal")
        self.total_igst_entry.configure(state="normal")
        self.grand_total_entry.configure(state="normal")

        CreateBill.price_list = [CreateBill.total_price, CreateBill.total_cgst, CreateBill.total_sgst,
                                 CreateBill.total_igst, CreateBill.grand_total, str(datetime.date.today())]

        self.total_price_entry.configure(state="disabled")
        self.total_sgst_entry.configure(state="disabled")
        self.total_cgst_entry.configure(state="disabled")
        self.total_igst_entry.configure(state="disabled")
        self.grand_total_entry.configure(state="disabled")

