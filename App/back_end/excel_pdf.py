import win32api
from App.back_end.py_to_excel import PyToPdf
import os


class ExcelToPdf:
    @staticmethod
    def make_pdf_file(main_list, transport_list, customer_list, price_list):
        ml = main_list
        tl = transport_list
        cl = customer_list
        pl = price_list
        excel_file = PyToPdf.upload_to_excel(ml, tl, cl, pl)
        xfile = "..\\back_end\\" + excel_file

        printer_name = 'Microsoft Print to PDF'  # name of the printer
        out = '/d:"%s"' % printer_name

        # print the PDF to the proper Printer
        win32api.ShellExecute(0, "print", xfile, out, ".", 0)

        # remove excel file
        print(excel_file)
        os.remove("..\\back_end\\" + excel_file)

