import os  # for removing image file
from PyQt5 import QtWidgets
from App.PythonUi.password import Ui_pLoginWindow
from App.PythonUi.forgot_password import Ui_fpMainWindow
from App.PythonUi.menu import UiMwMainWindow
from App.PythonUi.tabs import Ui_tabs_MainWindow
from App.Backend.hash_password import Passwords
from App.Backend.email_sms import Mail, SMS
from App.Backend.patterns_validations import PatternsValidations
from PyQt5.QtWidgets import QMessageBox
from App.Database.db_changes import UploadRetrievePassword, Customer, Items, Invoice
from random import randint
from PyQt5.QtWidgets import *
from mysql.connector.errors import IntegrityError
import datetime
from PyQt5.QtGui import QStandardItemModel, QTextCursor
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from PyQt5 import QtGui  # for plotting graph on label


class UserInteraction(QtWidgets.QMainWindow):
    FROM, SUBJECT, DATE = range(3)

    def __init__(self, parent=None):
        super(UserInteraction, self).__init__(parent)
        self.main_login_window_setup('p_w')
        self.msg = QMessageBox()
        self.otp = ...
        self.track_tabs = []  # here we keep track of opening and closing of tabs
        self.mobile_number_to_edit = ...
        self.item_id_to_edit = ...
        self.same_check_box = False
        self.date = datetime.date.today()
        self.final_items_in_invoice = []
        self.final_customer_transport_totalbill_details_in_invoice = []
        # flag for invoice list to check whether the input of + button if after edit function or not
        self.edit_check_flag_invoice_list = 0
        self.dic_gst = {'cgst': 0, 'sgst': 0, 'igst': 0}

    def main_login_window_setup(self, screen):  # here we setup login window
        if screen == 'reset_window':  # hide password reset window
            self.fpMainWindow.hide()
        self.pLoginWindow = QtWidgets.QMainWindow()  # object of window (password.py file)
        self.plUi = Ui_pLoginWindow()  # object of login password ui class (Ui_pLoginWindow()) (password.py file# )
        self.plUi.setup_ui(self.pLoginWindow)
        self.pLoginWindow.show()

        self.plUi.pPasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)  # hide password
        self.plUi.pPasswordLineEdit.returnPressed.connect(
            lambda: self.enter(self.plUi.pPasswordLineEdit.text()))  # pressing enter
        self.plUi.pArrowLlabel.mousePressEvent = self.enter_label  # added mouse event to arrow label and bind function
        self.plUi.pForgotPasswordLabel.mousePressEvent = self.reset_password  # added mouse event to Forget Password? label and bind functio

    def password_reset_window_setup(self, screen):  # here we setup reset_password window
        if screen == 'password_window':  # Hided login window
            self.pLoginWindow.hide()
        self.fpMainWindow = QtWidgets.QMainWindow()  # object of window (forgot_password.py file)
        self.fpUi = Ui_fpMainWindow()  # object of forgot password ui class (Ui_fpMainWindow()) (forgot_password.py file# )
        self.fpUi.setup_fp(self.fpMainWindow)
        self.fpMainWindow.show()
        self.hover_effect('fpUi')
        self.fpUi.fpSaveButton.clicked.connect(self.get_new_password)
        self.fpUi.fpSaveButton.setEnabled(False)  # initially disabled
        self.fpUi.fpNpLineEdit.setEnabled(False)  # initially disabled
        self.fpUi.fpCpLineEdit.setEnabled(False)  # initially disabled
        self.fpUi.fpNpLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)  # hide new password
        self.fpUi.fpCpLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)  # hide confirm password

    def main_option_window_setup(self, screen):  # here we setup option/menu window
        if screen == 'password_window':  # Hide login window
            self.pLoginWindow.hide()
        self.mwMainWindow = QtWidgets.QMainWindow()  # object of window (menu.py file)
        self.mwUi = UiMwMainWindow()  # object of option/menu ui class (UiMwMainWindow()) (menu.py file# )
        self.mwUi.setup_main_window(self.mwMainWindow)
        self.mwMainWindow.show()
        self.hover_effect('mwUi')
        self.mwUi.mwAddCustomelrLabel.mousePressEvent = self.add_customer_tab
        self.mwUi.mwAddItemLabel.mousePressEvent = self.add_item_tab
        self.mwUi.mwEditCustomerLabel.mousePressEvent = self.edit_customer_tab
        self.mwUi.mwEditItemLabel.mousePressEvent = self.edit_item_tab
        self.mwUi.mwInvoiceLabel.mousePressEvent = self.billing_tab
        self.mwUi.mmLockLabel.mousePressEvent = self.change_password_tab
        self.mwUi.mmCustomerLabel.mousePressEvent = self.view_all_customer_tab
        self.mwUi.mmItemLabel.mousePressEvent = self.view_all_items_tab
        self.mwUi.label_6.mousePressEvent = self.graphs_tab

    def open_main_tabs_window(self, tab_name):
        self.tabsMainWindow = QtWidgets.QMainWindow()
        self.tabs_ui = Ui_tabs_MainWindow()
        self.tabs_ui.setup_tabs_window(self.tabsMainWindow)
        self.hover_effect('tabs_ui')
        self.tabsMainWindow.show()
        self.tabs_ui.tabs.setTabsClosable(True)
        self.tabs_ui.tabs.tabCloseRequested.connect(self.close_respective_tab)  # here we close the respective tab and remove its track

        """One of the tab below will be opened initially as per request from menu.py"""
        if tab_name == 'add_customer_tab':
            self.open_add_customer_tab('')
            self.hover_effect('tabs_ui')

        elif tab_name == 'add_item_tab':
            self.open_add_item_tab('')
            self.hover_effect('tabs_ui')

        elif tab_name == 'edit_customer_tab':
            self.open_edit_customer_tab('')
            self.hover_effect('tabs_ui')

        elif tab_name == 'edit_item_tab':
            self.open_edit_item_tab('')
            self.hover_effect('tabs_ui')

        elif tab_name == 'billing_tab':
            self.open_billing_tab('')
            self.invoice_number()
            self.hover_effect('tabs_ui')

        elif tab_name == 'graphs_tab':
            self.open_graphs_tab('')
            self.retrieve_data_from_db()
            self.hover_effect('tabs_ui')

        elif tab_name == 'view_all_customer_tab':
            self.open_view_customer_tab('')
            self.all_customers('')
            self.hover_effect('tabs_ui')

        elif tab_name == 'view_all_items_tab':
            self.open_view_items_tab('')
            self.all_items('')
            self.hover_effect('tabs_ui')

        elif tab_name == 'change_password_tab':
            self.open_change_password_tab('')
            self.hover_effect('tabs_ui')

        """opening tabs from the labels in tabs window only"""
        self.tabs_ui.addCusIconLabel_2.mousePressEvent = self.open_add_customer_tab
        self.tabs_ui.editCusIconLabel.mousePressEvent = self.open_edit_customer_tab
        self.tabs_ui.addItemIconLabel.mousePressEvent = self.open_add_item_tab
        self.tabs_ui.editItemIconLabel.mousePressEvent = self.open_edit_item_tab
        self.tabs_ui.invoiceIconLabel.mousePressEvent = self.open_billing_tab
        self.tabs_ui.label.mousePressEvent = self.open_view_customer_tab
        self.tabs_ui.label_4.mousePressEvent = self.open_view_items_tab
        self.tabs_ui.passwordIconLabel.mousePressEvent = self.open_change_password_tab
        self.tabs_ui.graphsIconLabel.mousePressEvent = self.open_graphs_tab

        """
        Below is everything about change password in tabs
        """
        self.tabs_ui.mmCpasNpLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)  # hide password
        self.tabs_ui.mmCpasLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)  # hide password

        self.tabs_ui.mmCpasNpLineEdit.setEnabled(False)  # initially kept disabled
        self.tabs_ui.mmCpasLineEdit.setEnabled(False)  # initially kept disabled
        self.tabs_ui.mmCpasSaveLabel.setEnabled(False)  # initially kept disabled

        self.tabs_ui.mmCpasOtpLineEdit.returnPressed.connect(
            lambda: self.old_pass_enter(self.tabs_ui.mmCpasOtpLineEdit.text()))  # pressing enter
        self.tabs_ui.mmCpasArrowLabel.mousePressEvent = self.old_pass_label  # added mouse event to arrow label and bind function
        self.tabs_ui.mmCpasSaveLabel.clicked.connect(self.up_new_password)  # updated new password

        """
        Below is everything about add customer details
        """
        self.tabs_ui.mmAcSaveButton.clicked.connect(self.get_customer_details)
        self.tabs_ui.mmAcClearButton.clicked.connect(self.clear_customer_details)

        """
        Below is everything about edit customer details
        """
        self.tabs_ui.mmEcLabel12.mousePressEvent = self.search_edit_customer_details_label
        self.tabs_ui.mmEcLineEdit1.returnPressed.connect(lambda: self.search_edit_customer_details_enter(self.tabs_ui.mmEcLineEdit1.text()))
        self.tabs_ui.mmEcClearButton.clicked.connect(self.clear_edit_customer_details)
        self.tabs_ui.mmEcSaveButton.clicked.connect(self.get_edit_customer_details)

        """
        Below is everything about add item details
        """
        self.tabs_ui.mmAiSaveButton.clicked.connect(self.save_items)
        self.tabs_ui.mmAiClearButton.clicked.connect(self.clear_items)

        """
        Below is everything about edit item details
        """
        self.tabs_ui.mmEiLineEdit1.returnPressed.connect(lambda: self.get_item_id_enter(self.tabs_ui.mmEiLineEdit1.text()))
        self.tabs_ui.mmEiLabel8.mousePressEvent = self.get_item_id_label
        self.tabs_ui.mmEiSaveButton.clicked.connect(self.save_edited_items)
        self.tabs_ui.mmEiClearButton.clicked.connect(self.clear_edited_items)

        """
        Below is everything about the invoice tab
        """

        self.tabs_ui.mmInLineEdit1.returnPressed.connect(lambda: self.get_mobile_invoice(self.tabs_ui.mmInLineEdit1.text()))
        date = str(self.date).split('-')
        new_date = f'{date[2]}-{date[1]}-{date[0]}'
        self.tabs_ui.mmInLabe26.setText(new_date)
        self.same_customer_details_enabled_disabled(False)
        self.tabs_ui.mmInComboBox1.clicked.connect(lambda: self.check(self.tabs_ui.mmInLineEdit1.text()))
        self.tabs_ui.mmInLineEdit3.returnPressed.connect(lambda: self.another_shipper(self.tabs_ui.mmInLineEdit3.text()))
        self.tabs_ui.mmInLineEdit4.returnPressed.connect(self.item_details_from_db)  # retrieving data from item db
        self.tabs_ui.mmInLineEdit7.returnPressed.connect(self.calculating_total_price)

        # setting transport details disabled before check box is set
        self.tabs_ui.mmInLineEdit13.setEnabled(False)
        self.tabs_ui.mmInLineEdit14.setEnabled(False)
        self.tabs_ui.mmInLineEdit15.setEnabled(False)
        self.tabs_ui.mmInComboBox2.clicked.connect(self.enable_transport_details)

        # setting all auto updating items disabled for user
        self.tabs_ui.mmInLineEdit6.setEnabled(False)
        self.tabs_ui.mmInLineEdit8.setEnabled(False)
        self.tabs_ui.mmInLineEdit9.setEnabled(False)
        self.tabs_ui.mmInLineEdit10.setEnabled(False)
        self.tabs_ui.mmInLineEdit11.setEnabled(False)
        self.tabs_ui.mmInLineEdit12.setEnabled(False)
        self.tabs_ui.mmInLineEdit16.setEnabled(False)
        self.tabs_ui.mmInLineEdit17.setEnabled(False)
        self.tabs_ui.mmInLineEdit18.setEnabled(False)
        self.tabs_ui.mmInLineEdit19.setEnabled(False)
        self.tabs_ui.mmInLineEdit20.setEnabled(False)

        # click event
        self.tabs_ui.mmInTableWidget.clicked.connect(self.edit_option_in_invoice)

        # Add item in tree view
        self.tabs_ui.mmInPushButton1.clicked.connect(self.add_item_in_invoice)

        # remove item from tree view
        self.tabs_ui.mmInPushButton2.clicked.connect(self.remove_item_from_invoice)

        # generate button function binding
        self.tabs_ui.mmInPushButton4.clicked.connect(self.generate_button_function)

        # clearing file
        self.tabs_ui.mmInPushButton3.clicked.connect(self.clearing_whole_invoice_tab)

        """
        Below is everything about the all item's tab
        """
        self.tabs_ui.mmIiLabel2.mousePressEvent = self.all_items

        """
        Below is everything about the all customer's tab
        """
        self.tabs_ui.mmCiLabel2.mousePressEvent = self.all_customers

        """
        Below is everything about the Graph's tab
        """
        self.tabs_ui.mmGPushButton.clicked.connect(self.save_graph)
        self.tabs_ui.mmGPushButton.setShortcut("Ctrl+S")

        # combo box link with function
        # self.tabs_ui.mmGComboBox.activated[str].connect(self.graph_combo_box)

    # below are gui hover and initial setting functions
    def hover_effect(self, control):
        # adding hover effect
        if control == 'tabs_ui':
            self.tabs_ui.mmInnerFrame.setStyleSheet("QPushButton:hover\n"
                                                    "{\n"
                                                    "    background-color: rgb(213, 213, 213);\n"
                                                    "}")
            self.tabs_ui.addCusIconLabel_2.setStyleSheet("QLabel:hover\n"
                                                "{\n"
                                                "    background-color: rgb(213, 213, 213);\n"
                                                "}")
            self.tabs_ui.editCusIconLabel.setStyleSheet("QLabel:hover\n"
                                                "{\n"
                                                "    background-color: rgb(213, 213, 213);\n"
                                                "}")
            self.tabs_ui.invoiceIconLabel.setStyleSheet("QLabel:hover\n"
                                                "{\n"
                                                "    background-color: rgb(213, 213, 213);\n"
                                                "}")
            self.tabs_ui.passwordIconLabel.setStyleSheet("QLabel:hover\n"
                                                "{\n"
                                                "    background-color: rgb(213, 213, 213);\n"
                                                "}")
            self.tabs_ui.graphsIconLabel.setStyleSheet("QLabel:hover\n"
                                                "{\n"
                                                "    background-color: rgb(213, 213, 213);\n"
                                                "}")
            self.tabs_ui.label.setStyleSheet("QLabel:hover\n"
                                                "{\n"
                                                "    background-color: rgb(213, 213, 213);\n"
                                                "}")
            self.tabs_ui.label_4.setStyleSheet("QLabel:hover\n"
                                                "{\n"
                                                "    background-color: rgb(213, 213, 213);\n"
                                                "}")
            self.tabs_ui.editItemIconLabel.setStyleSheet("QLabel:hover\n"
                                                "{\n"
                                                "    background-color: rgb(213, 213, 213);\n"
                                                "}")
            self.tabs_ui.addItemIconLabel.setStyleSheet("QLabel:hover\n"
                                                "{\n"
                                                "    background-color: rgb(213, 213, 213);\n"
                                                "}")

        elif control == 'mwUi':
            self.mwUi.mwInnerFrame.setStyleSheet("QLabel:hover\n"
                                            "{\n"
                                            "    background-color: rgb(213, 213, 213);\n"
                                            "}")
        else:
            self.fpUi.fpInnerFrame.setStyleSheet("QPushButton:hover\n"
                                            "{\n"
                                            "    background-color: rgb(213, 213, 213);\n"
                                            "}")

    def enable_transport_details(self):
        if self.tabs_ui.mmInComboBox2.isChecked():
            # setting transport details enabled after check box is set
            self.tabs_ui.mmInLineEdit13.setEnabled(True)
            self.tabs_ui.mmInLineEdit14.setEnabled(True)
            self.tabs_ui.mmInLineEdit15.setEnabled(True)
        else:
            # setting transport details disabled before check box is set
            self.tabs_ui.mmInLineEdit13.setEnabled(False)
            self.tabs_ui.mmInLineEdit14.setEnabled(False)
            self.tabs_ui.mmInLineEdit15.setEnabled(False)

    # below are all functions of invoice tab
    def invoice_number(self):
            self.invoice_file_object = open("../invoice_number.txt", "r")  # opening invoice file
            self.tabs_ui.mmInLabe30.setText(str(int(self.invoice_file_object.readline())))
            self.invoice_file_object.close()

    def enter_values_in_database(self):
        if self.tabs_ui.mmInLineEdit20.text() != '':
            invoice_det = [str(self.date),  str(self.tabs_ui.mmInLineEdit16.text()), str(self.tabs_ui.mmInLineEdit20.text())]
            Invoice.insert_invoice_data(invoice_det)
            return True
        else:
            self.msg.setWindowTitle("Error")
            self.msg.setText("No items are added in the bill.")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()
            return False

    def invoice_number_update(self):
        invoice_file_object = open("../invoice_number.txt", "+w")
        invoice_file_object.write(str(int(self.tabs_ui.mmInLabe30.text()) + 1))
        invoice_file_object.close()

    def setting_final_list_of_invoice_tab(self):
        self.final_customer_transport_totalbill_details_in_invoice.append(
            [self.tabs_ui.mmInLineEdit1.text(), self.tabs_ui.mmInLineEdit2.text(), self.tabs_ui.mmInLabe27.text()]
        )  # storing customer basic info
        self.final_customer_transport_totalbill_details_in_invoice.append(
            [self.tabs_ui.mmInLineEdit3.text(), self.tabs_ui.mmInLabe28.text(), self.tabs_ui.mmInLabe29.text()]
        )  # storing shipping address
        self.final_customer_transport_totalbill_details_in_invoice.append(
            [self.tabs_ui.mmInLineEdit13.text(), self.tabs_ui.mmInLineEdit14.text(), self.tabs_ui.mmInLineEdit15.text()]
        )  # transportation details
        self.final_customer_transport_totalbill_details_in_invoice.append(
            [self.tabs_ui.mmInLineEdit16.text(), self.tabs_ui.mmInLineEdit17.text(), self.tabs_ui.mmInLineEdit18.text(),
             self.tabs_ui.mmInLineEdit19.text(), self.tabs_ui.mmInLineEdit20.text()]
        )

    def generate_button_function(self):
        if self.tabs_ui.mmInLineEdit1.text() != '' and self.tabs_ui.mmInLineEdit2.text() != '':
            if self.enter_values_in_database():
                self.msg.setWindowTitle("Information")
                self.msg.setText("Data Saved")
                self.msg.setIcon(QMessageBox.Information)
                self.msg.exec_()
                # creating final list of customer, transport and grandtotal details
                self.setting_final_list_of_invoice_tab()
                self.invoice_number_update()  # updating invoice number
                self.clearing_whole_invoice_tab()  # clearing values of invoice tab

    def clearing_whole_invoice_tab(self):
        # clearing line edit data
        self.tabs_ui.mmInLineEdit1.clear()
        self.tabs_ui.mmInLineEdit2.clear()
        self.tabs_ui.mmInLineEdit3.clear()
        self.tabs_ui.mmInLineEdit4.clear()
        self.tabs_ui.mmInLineEdit5.clear()
        self.tabs_ui.mmInLineEdit6.clear()
        self.tabs_ui.mmInLineEdit7.clear()
        self.tabs_ui.mmInLineEdit8.clear()
        self.tabs_ui.mmInLineEdit9.clear()
        self.tabs_ui.mmInLineEdit10.clear()
        self.tabs_ui.mmInLineEdit11.clear()
        self.tabs_ui.mmInLineEdit12.clear()
        self.tabs_ui.mmInLineEdit13.clear()
        self.tabs_ui.mmInLineEdit14.clear()
        self.tabs_ui.mmInLineEdit15.clear()
        self.tabs_ui.mmInLineEdit16.clear()
        self.tabs_ui.mmInLineEdit17.clear()
        self.tabs_ui.mmInLineEdit18.clear()
        self.tabs_ui.mmInLineEdit19.clear()
        self.tabs_ui.mmInLineEdit20.clear()
        # clearing label data
        self.tabs_ui.mmInLabe27.clear()
        self.tabs_ui.mmInLabe28.clear()
        self.tabs_ui.mmInLabe29.clear()
        # clearing final list of invoice data
        self.final_items_in_invoice = []
        # clearing final list of customer, transport and total bill details
        self.final_customer_transport_totalbill_details_in_invoice = []
        # clearing tree view
        self.display_in_tree_view()
        # disabling combo boxes
        if self.tabs_ui.mmInComboBox1.isChecked():
            self.tabs_ui.mmInComboBox1.nextCheckState()
        if self.tabs_ui.mmInComboBox2.isChecked():
            self.tabs_ui.mmInComboBox2.nextCheckState()
        # updating invoice number
        self.invoice_number()

    def calculating_total_price(self):
        if self.tabs_ui.mmInLineEdit7.text() and self.tabs_ui.mmInLineEdit5 is not None:
            price = int(self.tabs_ui.mmInLineEdit5.text()) * int(self.tabs_ui.mmInLineEdit6.text())
            discount_price = price - (price*int(self.tabs_ui.mmInLineEdit7.text())/100)
            try:
                if float(self.tabs_ui.mmInLineEdit8.text()) == 0.0 and float(self.tabs_ui.mmInLineEdit9.text()) == 0.0:
                    self.dic_gst['igst'] = (discount_price * float(self.tabs_ui.mmInLineEdit10.text()))/100
                    self.tabs_ui.mmInLineEdit11.setText(str(discount_price))

                else:
                    self.dic_gst['cgst'] = (discount_price * (float(self.tabs_ui.mmInLineEdit8.text())))/100
                    self.dic_gst['sgst'] = (discount_price * (float(self.tabs_ui.mmInLineEdit9.text())))/100
                    self.tabs_ui.mmInLineEdit11.setText(str(discount_price))
            except Exception as e:
                print(e)

    def item_details_from_db(self):
        result = Items.search_item(self.tabs_ui.mmInLineEdit4.text())
        if result is not None:
            self.tabs_ui.mmInLineEdit6.setText(result[2])
            if self.tabs_ui.mmInLineEdit2.text() == 'Punjab':
                try:
                    self.tabs_ui.mmInLineEdit8.setText(str(int(result[3])/2))
                    self.tabs_ui.mmInLineEdit9.setText(str(int(result[3])/2))
                    self.tabs_ui.mmInLineEdit10.setText('0')
                except Exception as e:
                    print(e)
            else:
                self.tabs_ui.mmInLineEdit8.setText('0')
                self.tabs_ui.mmInLineEdit9.setText('0')
                self.tabs_ui.mmInLineEdit10.setText(result[3])
            self.tabs_ui.mmInLineEdit12.setText(result[1])
        else:
            # message to user that item doesn't exist
            self.msg.setWindowTitle("Error")
            self.msg.setText("Item code doesn't exist in database. Try with some other value of item code")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()

    def calculating_index_at_selection(self):  # returns selected index value of item code
        # returns value of 0 index of selected row
        return self.tabs_ui.mmInTableWidget.model().data(self.tabs_ui.mmInTableWidget.model().
                                                         index(self.tabs_ui.mmInTableWidget.currentIndex().row(), 0))

    def edit_option_in_invoice(self):
        try:
            for i in range(len(self.final_items_in_invoice)):
                if self.final_items_in_invoice[i][0] == self.calculating_index_at_selection():
                    self.tabs_ui.mmInLineEdit4.setText(self.final_items_in_invoice[i][0])
                    self.tabs_ui.mmInLineEdit5.setText(self.final_items_in_invoice[i][1])
                    self.tabs_ui.mmInLineEdit6.setText(self.final_items_in_invoice[i][2])
                    self.tabs_ui.mmInLineEdit7.setText(self.final_items_in_invoice[i][3])
                    self.tabs_ui.mmInLineEdit8.setText(self.final_items_in_invoice[i][4])
                    self.tabs_ui.mmInLineEdit9.setText(self.final_items_in_invoice[i][5])
                    self.tabs_ui.mmInLineEdit10.setText(self.final_items_in_invoice[i][6])
                    self.tabs_ui.mmInLineEdit11.setText(self.final_items_in_invoice[i][7])
                    self.tabs_ui.mmInLineEdit12.setText(self.final_items_in_invoice[i][8])
                    # flag for invoice list to check whether the input of + button if after edit function or not
                    self.calculating_total_price()  # to remove correct values from total bill
                    self.edit_check_flag_invoice_list = 1
                    break
        except Exception as e:
            print(e)

    def append_final_items_in_invoice(self):
        self.final_items_in_invoice.append([self.tabs_ui.mmInLineEdit4.text(), self.tabs_ui.mmInLineEdit5.text(),
                                            self.tabs_ui.mmInLineEdit6.text(), self.tabs_ui.mmInLineEdit7.text(),
                                            self.tabs_ui.mmInLineEdit8.text(), self.tabs_ui.mmInLineEdit9.text(),
                                            self.tabs_ui.mmInLineEdit10.text(), self.tabs_ui.mmInLineEdit11.text(),
                                            self.tabs_ui.mmInLineEdit12.text()])

    def setting_final_price(self, control, item_code):
        for i in range(len(self.final_items_in_invoice)):
            if self.final_items_in_invoice[i][0] == item_code:
                if control == 'add':
                    try:
                        # setting total price
                        if self.tabs_ui.mmInLineEdit16.text() != '':
                            self.tabs_ui.mmInLineEdit16.setText(str(float(self.tabs_ui.mmInLineEdit16.text()) + float(self.final_items_in_invoice[i][7])))
                        if self.tabs_ui.mmInLineEdit16.text() == '':
                            self.tabs_ui.mmInLineEdit16.setText(str(float(self.final_items_in_invoice[i][7])))
                        if self.tabs_ui.mmInLineEdit17.text() != '':
                            self.tabs_ui.mmInLineEdit17.setText(
                                str(float(self.tabs_ui.mmInLineEdit17.text()) + float(self.dic_gst['sgst'])))
                        if self.tabs_ui.mmInLineEdit17.text() == '':
                            self.tabs_ui.mmInLineEdit17.setText(str(float(self.dic_gst['sgst'])))
                        if self.tabs_ui.mmInLineEdit18.text() != '':
                            self.tabs_ui.mmInLineEdit18.setText(
                                str(float(self.tabs_ui.mmInLineEdit18.text()) + float(self.dic_gst['cgst'])))
                        if self.tabs_ui.mmInLineEdit18.text() == '':
                            self.tabs_ui.mmInLineEdit18.setText(str(float(self.dic_gst['cgst'])))
                        if self.tabs_ui.mmInLineEdit19.text() != '':
                            self.tabs_ui.mmInLineEdit19.setText(
                                str(float(self.tabs_ui.mmInLineEdit19.text()) + float(self.dic_gst['igst'])))
                        if self.tabs_ui.mmInLineEdit19.text() == '':
                            self.tabs_ui.mmInLineEdit19.setText(str(float(self.dic_gst['igst'])))
                    except Exception as e:
                        print(e)
                if control == 'remove':
                    if self.tabs_ui.mmInLineEdit16.text() != '':
                        self.tabs_ui.mmInLineEdit16.setText(str(float(self.tabs_ui.mmInLineEdit16.text()) - float(self.final_items_in_invoice[i][7])))
                    if self.tabs_ui.mmInLineEdit17.text() != '':
                        self.tabs_ui.mmInLineEdit17.setText(
                            str(float(self.tabs_ui.mmInLineEdit17.text()) - float(self.dic_gst['sgst'])))
                    if self.tabs_ui.mmInLineEdit18.text() != '':
                        self.tabs_ui.mmInLineEdit18.setText(
                            str(float(self.tabs_ui.mmInLineEdit18.text()) - float(self.dic_gst['cgst'])))
                    if self.tabs_ui.mmInLineEdit19.text() != '':
                        self.tabs_ui.mmInLineEdit19.setText(
                            str(float(self.tabs_ui.mmInLineEdit19.text()) - float(self.dic_gst['igst'])))
                # setting grand total based on values above it
                try:
                    if (self.tabs_ui.mmInLineEdit16.text(), self.tabs_ui.mmInLineEdit17.text(),
                            self.tabs_ui.mmInLineEdit18.text(), self.tabs_ui.mmInLineEdit19.text()) != ('', '', '', ''):
                        self.tabs_ui.mmInLineEdit20.setText(str(float(self.tabs_ui.mmInLineEdit16.text()) +
                                                            float(self.tabs_ui.mmInLineEdit17.text()) +
                                                            float(self.tabs_ui.mmInLineEdit18.text()) +
                                                            float(self.tabs_ui.mmInLineEdit19.text())))
                except Exception as e:
                    print(e)

    def add_item_in_invoice(self):  # function to add item in tree view (invoice tab)
        # to verify customer details are filed properly as gst depend on state
        if self.tabs_ui.mmInLineEdit1.text() != '':
            if self.tabs_ui.mmInLineEdit2.text() == '':
                self.get_mobile_invoice(self.tabs_ui.mmInLineEdit1.text())
            # check all the values in line edit
            if self.tabs_ui.mmInLineEdit4.text() != '' and self.tabs_ui.mmInLineEdit5.text() != '' and self.tabs_ui.mmInLineEdit7.text() != '':
                self.item_details_from_db()  # to verify last time update in item code before pressing enter
                self.calculating_total_price()  # to verify last time update in discount or quantity before adding
                if len(self.final_items_in_invoice) >= 1:
                    if self.tabs_ui.mmInLineEdit4.text() not in \
                            [self.final_items_in_invoice[i][0] for i in range(len(self.final_items_in_invoice))]:
                        self.append_final_items_in_invoice()
                        self.setting_final_price('add', self.tabs_ui.mmInLineEdit4.text())  # used to add the values in invoice total price
                        self.clearing_line_edit_item_invoice()

                    else:  # if item gets matched with already existing item id of the list
                        if self.edit_check_flag_invoice_list == 1:
                            self.remove_item_from_invoice()  # removing selected item with previous values
                            self.append_final_items_in_invoice()  # updating with new values to previous item code only
                            self.setting_final_price('add', self.tabs_ui.mmInLineEdit4.text())  # used to add the values in invoice total price
                            self.clearing_line_edit_item_invoice()
                        # warning for same item added in the list
                        if self.edit_check_flag_invoice_list == 0:
                            self.msg.setWindowTitle("Error")
                            self.msg.setText('Already present in the invoice list.')
                            self.msg.setIcon(QMessageBox.Warning)
                            self.msg.exec_()

                else:
                    self.append_final_items_in_invoice()
                    self.setting_final_price('add', self.tabs_ui.mmInLineEdit4.text())  # used to add the values in invoice total price
                    self.clearing_line_edit_item_invoice()
                # add it in tree view
                self.display_in_tree_view()
        else:
            self.msg.setWindowTitle("Error")
            self.msg.setText("Enter phone number to add items in bill.")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()

    def clearing_line_edit_item_invoice(self):
        self.tabs_ui.mmInLineEdit4.clear()
        self.tabs_ui.mmInLineEdit5.clear()
        self.tabs_ui.mmInLineEdit6.clear()
        self.tabs_ui.mmInLineEdit7.clear()
        self.tabs_ui.mmInLineEdit8.clear()
        self.tabs_ui.mmInLineEdit9.clear()
        self.tabs_ui.mmInLineEdit10.clear()
        self.tabs_ui.mmInLineEdit11.clear()
        self.tabs_ui.mmInLineEdit12.clear()

    def display_in_tree_view(self):
        model = self.create_tree_model(self)
        self.tabs_ui.mmInTableWidget.setModel(model)
        for i in range(len(self.final_items_in_invoice)):
            self.add_tree(model, self.final_items_in_invoice[i][0], self.final_items_in_invoice[i][1],
                         self.final_items_in_invoice[i][2], self.final_items_in_invoice[i][3],
                         self.final_items_in_invoice[i][4], self.final_items_in_invoice[i][5],
                         self.final_items_in_invoice[i][6], self.final_items_in_invoice[i][7],
                         self.final_items_in_invoice[i][8])

    def create_tree_model(self, parent):
        model = QStandardItemModel(0, 9, parent)
        model.setHeaderData(0, Qt.Horizontal, "Item Code")
        model.setHeaderData(1, Qt.Horizontal, "Quantity")
        model.setHeaderData(2, Qt.Horizontal, "Unit Price")
        model.setHeaderData(3, Qt.Horizontal, "Discount %")
        model.setHeaderData(4, Qt.Horizontal, "SGST")
        model.setHeaderData(5, Qt.Horizontal, "CGST")
        model.setHeaderData(6, Qt.Horizontal, "IGST")
        model.setHeaderData(7, Qt.Horizontal, "Total Price")
        model.setHeaderData(8, Qt.Horizontal, "Product Name")
        return model

    def add_tree(self, model, item_code, quantity, unit_price, discount, sgst, cgst, igst, total_price, product_name):
        model.insertRow(0)
        model.setData(model.index(0, 0), item_code)
        model.setData(model.index(0, 1), quantity)
        model.setData(model.index(0, 2), unit_price)
        model.setData(model.index(0, 3), discount)
        model.setData(model.index(0, 4), sgst)
        model.setData(model.index(0, 5), cgst)
        model.setData(model.index(0, 6), igst)
        model.setData(model.index(0, 7), total_price)
        model.setData(model.index(0, 8), product_name)

    def remove_item_from_invoice(self):  # function to remove item from tree view (invoice tab)

        self.setting_final_price('remove', self.tabs_ui.mmInLineEdit4.text())  # used to subtract the values in invoice total price
        try:

            for i in range(len(self.final_items_in_invoice)):
                if self.final_items_in_invoice[i][0] == self.calculating_index_at_selection():
                    t = self.final_items_in_invoice.pop(i)
                    self.display_in_tree_view()
                    break
        except Exception as e:
            print(e)

    # below are all functions related to customer db tab
    def all_customers(self, event):  # displaying all customers present in customer database
        result = Customer.get_customers()
        self.tabs_ui.mmCitableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tabs_ui.mmCitableWidget.setRowCount(row_number+1)
            for column_number, data in enumerate(row_data):
                self.tabs_ui.mmCitableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    # below are all functions related to item db tab
    def all_items(self, event):  # display all the items present in items database
        result = Items.get_items()
        self.tabs_ui.mmIitableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tabs_ui.mmIitableWidget.setRowCount(row_number+1)
            for column_number, data in enumerate(row_data):
                self.tabs_ui.mmIitableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    # below are function for graph tab

    def retrieve_data_from_db(self):
        self.date_data, self.total_without_gst, self.grand_total_with_gst = Invoice.retrieve_invoice_data()
        # plotting values
        self.plot_graph(0)

    def plot_graph(self, control):
        x = []
        for i in self.date_data:
            x.append(i[0])
        self.date_data = x
        y = []
        for i in self.total_without_gst:
            y.append(float(i[0]))
        self.total_without_gst = y
        plt.subplot(2, 1, 1)
        plt.plot(x, y, 'o-')
        plt.gcf().autofmt_xdate()
        plt.title('Graph Representation of Sale')
        plt.ylabel('Total with GST')
        y = []
        for i in self.grand_total_with_gst:
            y.append(float(i[0]))
        self.grand_total_with_gst = y
        plt.subplot(2, 1, 2)
        plt.plot(x, y, '.-')
        plt.gcf().autofmt_xdate()
        plt.xlabel('Date')
        plt.ylabel('Total with GST')
        if control == 0:
            plt.savefig('graph.png', dpi=(130))
            self.tabs_ui.mmGLabel1.setPixmap(QtGui.QPixmap("graph.png"))
            self.tabs_ui.mmGLabel1.setScaledContents(True)
            plt.close()
            # deleting file
            os.remove("graph.png")
        else:
            file_name = self.saveFileDialog()
            plt.savefig(file_name, dpi=(130))
            plt.close()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Graph", "",
                                                            "All Files (*);;Image Files (*.png *.jpg *.bmp)", options=options)
        return file_name

    def save_graph(self):
        self.plot_graph(1)  # to save file

    # other functions by Sameer
    def another_shipper(self, mob_no):
        try:
            mob_no = mob_no.strip().lower()
            data = Customer.search_customer(mob_no)
            name = f'{data[0]} {data[1]}'
            address = data[2]
            if data is not None:
                if name == '':
                    name = 'None'
                if address == '':
                    address = 'None'
                self.tabs_ui.mmInLabe28.setText(name)
                self.tabs_ui.mmInLabe29.setText(address)
            else:
                self.msg.setWindowTitle("Error")
                self.msg.setText('Invalid phone number or phone number might not be registered.')
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()
                self.tabs_ui.mmInLineEdit3.clear()
        except TypeError:
            self.msg.setWindowTitle("Error")
            self.msg.setText('Invalid phone number or phone number might not be registered.')
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()
            self.tabs_ui.mmInLineEdit3.clear()
            self.tabs_ui.mmInLabe28.clear()
            self.tabs_ui.mmInLabe29.clear()

    def check(self, mob_no):
        try:
            mob_no = mob_no.strip().lower()
            data = Customer.search_customer(mob_no)
            if self.same_check_box is True:
                self.same_check_box = False
                self.tabs_ui.mmInLineEdit3.clear()
                self.tabs_ui.mmInLabe28.clear()
                self.tabs_ui.mmInLabe29.clear()
            else:
                self.same_check_box = True
                self.tabs_ui.mmInLineEdit3.setText(data[8])
                cus_name = data[0] + ' ' + data[1]
                if cus_name == '':
                    self.tabs_ui.mmInLabe28.setText('None')
                else:
                    self.tabs_ui.mmInLabe28.setText(cus_name)
                self.tabs_ui.mmInLabe29.setText(data[2])
        except TypeError:
            pass

    def same_customer_details_enabled_disabled(self, bool):
        self.tabs_ui.mmInComboBox1.setEnabled(bool)
        self.tabs_ui.mmInLineEdit3.setEnabled(bool)
        self.tabs_ui.mmInLabe28.setEnabled(bool)
        self.tabs_ui.mmInLabe29.setEnabled(bool)

    def get_mobile_invoice(self, mob_no):
        mob_no = mob_no.strip().lower()
        data = Customer.search_customer(mob_no)
        if data is not None:
            self.tabs_ui.mmInLineEdit2.setText(data[3])  # set state of respective customer
            cus_name = data[0] + ' ' + data[1]
            if cus_name == '':
                self.tabs_ui.mmInLabe27.setText('None')
            else:
                self.same_customer_details_enabled_disabled(True)
                self.tabs_ui.mmInLabe27.setText(cus_name)
        else:
            self.msg.setWindowTitle("Error")
            self.msg.setText('Invalid phone number or phone number might not be registered.')
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()
            self.tabs_ui.mmInLineEdit2.clear()
            self.tabs_ui.mmInLabe27.clear()

    def get_item_id_enter(self, item_id):
        item_id = self.tabs_ui.mmEiLineEdit1.text().strip().lower()
        self.show_edit_items(item_id)

    def get_item_id_label(self, event):
        item_id = self.tabs_ui.mmEiLineEdit1.text().strip().lower()
        self.show_edit_items(item_id)

    def show_edit_items(self, item_id):
        self.item_id_to_edit = item_id
        data = Items.search_item(item_id)
        if data is not None:
            self.tabs_ui.mmEiLineEdit2.setText(data[0])
            self.tabs_ui.mmEiLineEdit3.setText(data[1])
            self.tabs_ui.mmEiLineEdit4.setText(data[2])
            self.tabs_ui.mmEiComboBox.setCurrentText(data[3])
            self.tabs_ui.mmEiLineEdit5.setText(data[4])
        else:
            self.msg.setWindowTitle("Error")
            self.msg.setText('Item id is not valid')
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()

    def save_edited_items(self):
        item_id = self.tabs_ui.mmEiLineEdit2.text().strip().lower()
        item_name = self.tabs_ui.mmEiLineEdit3.text().strip().lower()
        price = self.tabs_ui.mmEiLineEdit4.text().strip().lower()
        gst = self.tabs_ui.mmEiComboBox.currentText().strip()
        hsn_code = self.tabs_ui.mmEiLineEdit5.text().strip().lower()

        if item_id != '':
            if price != '':
                try:
                    price = int(price)
                except ValueError:
                    self.msg.setWindowTitle("Error")
                    self.msg.setText('Please enter the valid price.')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
                    return -1
                price = str(price)
                data = [item_id, item_name, price, gst, hsn_code]
                try:
                    Items.update_item(data, self.item_id_to_edit)
                    self.msg.setWindowTitle("Data updated")
                    self.msg.setText('Item updated successfully.')
                    self.msg.setIcon(QMessageBox.Information)
                    self.msg.exec_()
                except IntegrityError:  # if item id is already saved
                    self.msg.setWindowTitle("Error")
                    self.msg.setText(
                        'This item id is already saved, if u want to update something then go to edit item id tab.')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
            else:
                self.msg.setWindowTitle("Price")
                self.msg.setText('Price is mandatory.')
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()
        else:
            self.msg.setWindowTitle("Item")
            self.msg.setText('Item id is mandatory.')
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()

    def clear_edited_items(self):
        try:
            self.tabs_ui.mmEiLineEdit2.clear()
            self.tabs_ui.mmEiLineEdit3.clear()
            self.tabs_ui.mmEiLineEdit4.clear()
            self.tabs_ui.mmEiLineEdit5.clear()
            self.tabs_ui.mmEiComboBox.setCurrentIndex(0)
        except Exception as e:
            print(e)

    def save_items(self):
        item_id = self.tabs_ui.mmAiLineEdit1.text().strip().lower()
        item_name = self.tabs_ui.mmAiLineEdit2.text().strip().lower()
        price = self.tabs_ui.mmAiLineEdit3.text().strip().lower()
        gst = self.tabs_ui.mmEcComboBox_2.currentText().strip()
        hsn_code = self.tabs_ui.mmAiLineEdit4.text().strip().lower()

        if item_id != '':
            if price != '':
                try:
                    price = int(price)
                except ValueError:
                    self.msg.setWindowTitle("Error")
                    self.msg.setText('Please enter the valid price.')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
                    return -1
                price = str(price)
                try:
                    Items.insert_item([item_id, item_name, price, gst, hsn_code])
                    self.msg.setWindowTitle("Data saved")
                    self.msg.setText('Item saved successfully.')
                    self.msg.setIcon(QMessageBox.Information)
                    self.msg.exec_()
                except IntegrityError:  # if item id is already saved
                    self.msg.setWindowTitle("Error")
                    self.msg.setText(
                        'This item id is already saved, if u want to update something then go to edit item id tab.')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
            else:
                self.msg.setWindowTitle("Price")
                self.msg.setText('Price is mandatory')
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()
        else:
            self.msg.setWindowTitle("Item")
            self.msg.setText('Item id is mandatory')
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()

    def clear_items(self):
        self.tabs_ui.mmAiLineEdit1.clear()
        self.tabs_ui.mmAiLineEdit2.clear()
        self.tabs_ui.mmAiLineEdit3.clear()
        self.tabs_ui.mmEcComboBox_2.setCurrentIndex(0)
        self.tabs_ui.mmAiLineEdit4.clear()

    def get_edit_customer_details(self):
        first_name = self.tabs_ui.mmEcLineEdit2.text().strip().lower()
        last_name = self.tabs_ui.mmEcLineEdit3.text().strip().lower()
        address = self.tabs_ui.lineEdit_4.text().strip().lower()
        state = self.tabs_ui.mmEcComboBox.currentText().strip()
        city = self.tabs_ui.mmEcLineEdit5.text().strip().lower()
        gst_no = self.tabs_ui.mmEcLineEdit6.text().strip().lower()
        addhar_no = self.tabs_ui.mmEcLineEdit7.text().strip().lower()
        pan_no = self.tabs_ui.mmEcLineEdit8.text().strip().lower()
        mobile_no = self.tabs_ui.mmEcLineEdit9.text().strip().lower()

        if mobile_no != '':
            if gst_no == '' and addhar_no == '' and pan_no == '':
                self.msg.setWindowTitle("Error")
                self.msg.setText(
                    "One of the following is mandatory:\n1. GST number\n2. PAN number\n3. AddharCard number")
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()
            else:
                result = PatternsValidations.validate(gst_no, addhar_no, mobile_no, pan_no)  # validate
                if result == 'Right':
                    try:
                        Customer.update_customer([first_name, last_name, address, state, city, gst_no, addhar_no, pan_no, mobile_no], self.mobile_number_to_edit)  # updated data
                        self.msg.setWindowTitle("Data updated")
                        self.msg.setText('Customer updated successfully')
                        self.msg.setIcon(QMessageBox.Information)
                        self.msg.exec_()
                    except IntegrityError:  # if phone number is already saved
                        self.msg.setWindowTitle("Phone number already saved")
                        self.msg.setText('This phone number is already saved, if u want to update something then go to edit customer tab.')
                        self.msg.setIcon(QMessageBox.Warning)
                        self.msg.exec_()
                elif result == 'wrong_gst':
                    self.msg.setWindowTitle("Wrong GST number")
                    self.msg.setText('Please check the GST number again')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
                elif result == 'wrong_addhar':
                    self.msg.setWindowTitle("Wrong addhar card number")
                    self.msg.setText('Please check the addhar card number again')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
                elif result == 'wrong_phone_no':
                    self.msg.setWindowTitle("Wrong phone number")
                    self.msg.setText('Please check the phone number again')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
                elif result == 'wrong_pan':
                    self.msg.setWindowTitle("Wrong PAN number")
                    self.msg.setText('Please check the PAN number again')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
        else:
            self.msg.setWindowTitle("Error")
            self.msg.setText("Phone number is mandatory")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()

    def search_edit_customer_details_label(self, event):
        mob_no = self.tabs_ui.mmEcLineEdit1.text().strip()
        self.search_edit_customer_details(mob_no)

    def search_edit_customer_details_enter(self, mob_no):
        mob_no = mob_no.strip()
        self.search_edit_customer_details(mob_no)

    def search_edit_customer_details(self, mob_no):
        self.mobile_number_to_edit = mob_no.strip().lower()
        result = Customer.search_customer(mob_no)
        if result is not None:
            """print all data in the line edit's"""
            self.tabs_ui.mmEcLineEdit2.setText(result[0])
            self.tabs_ui.mmEcLineEdit3.setText(result[1])
            self.tabs_ui.lineEdit_4.setText(result[2])
            self.tabs_ui.mmEcComboBox.setCurrentText(result[3])
            self.tabs_ui.mmEcLineEdit5.setText(result[4])
            self.tabs_ui.mmEcLineEdit6.setText(result[5])
            self.tabs_ui.mmEcLineEdit7.setText(result[6])
            self.tabs_ui.mmEcLineEdit8.setText(result[7])
            self.tabs_ui.mmEcLineEdit9.setText(result[8])
        else:
            self.msg.setWindowTitle("Phone number din't match")
            self.msg.setText('Please check the phone number again or might be this phone number is not registered')
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()

    def clear_edit_customer_details(self):
        self.tabs_ui.mmEcLineEdit2.clear()
        self.tabs_ui.mmEcLineEdit3.clear()
        self.tabs_ui.lineEdit_4.clear()
        self.tabs_ui.mmEcComboBox.setCurrentIndex(0)
        self.tabs_ui.mmEcLineEdit5.clear()
        self.tabs_ui.mmEcLineEdit6.clear()
        self.tabs_ui.mmEcLineEdit7.clear()
        self.tabs_ui.mmEcLineEdit8.clear()
        self.tabs_ui.mmEcLineEdit9.clear()

    def get_customer_details(self):
        first_name = self.tabs_ui.mmAcLineEdit1.text().strip().lower()
        last_name = self.tabs_ui.mmAcLineEdit2.text().strip().lower()
        address = self.tabs_ui.mmAcLineEdit3.text().strip().lower()
        state = self.tabs_ui.mmAcCombobox.currentText().strip()
        city = self.tabs_ui.mmAcLineEdit5.text().strip().lower()
        gst_no = self.tabs_ui.mmAcLineEdit6.text().strip().lower()
        addhar_no = self.tabs_ui.mmAcLineEdit7.text().strip().lower()
        pan_no = self.tabs_ui.mmAcLineEdit8.text().strip().lower()
        mobile_no = self.tabs_ui.mmAcLineEdit9.text().strip().lower()

        if mobile_no != '':
            if gst_no == '' and addhar_no == '' and pan_no == '':
                self.msg.setWindowTitle("Error")
                self.msg.setText("One of the following is mandatory\n1. GST number\n2. PAN number\n3. AddharCard number")
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()
            else:
                result = PatternsValidations.validate(gst_no, addhar_no, mobile_no, pan_no)  # validate
                if result == 'Right':
                    try:
                        Customer.insert_customer([first_name, last_name, address, state, city, gst_no, addhar_no, pan_no, mobile_no])  # inserted data
                        self.msg.setWindowTitle("Data saved")
                        self.msg.setText('Customer saved successfully')
                        self.msg.setIcon(QMessageBox.Information)
                        self.msg.exec_()
                    except IntegrityError:  # if phone number is already saved
                        self.msg.setWindowTitle("Phone number already saved")
                        self.msg.setText('This phone number is already saved, if u want to update something then go to edit customer.')
                        self.msg.setIcon(QMessageBox.Warning)
                        self.msg.exec_()
                elif result == 'wrong_gst':
                    self.msg.setWindowTitle("Wrong GST number")
                    self.msg.setText('Please check the GST number again')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
                elif result == 'wrong_addhar':
                    self.msg.setWindowTitle("Wrong addhar card number")
                    self.msg.setText('Please check the addhar card number again')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
                elif result == 'wrong_phone_no':
                    self.msg.setWindowTitle("Wrong phone number")
                    self.msg.setText('Please check the phone number again')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
                elif result == 'wrong_pan':
                    self.msg.setWindowTitle("Wrong PAN number")
                    self.msg.setText('Please check the PAN number again')
                    self.msg.setIcon(QMessageBox.Warning)
                    self.msg.exec_()
        else:
            self.msg.setWindowTitle("Error")
            self.msg.setText("Phone number is mandatory")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()

    def clear_customer_details(self):
        self.tabs_ui.mmAcLineEdit1.clear()
        self.tabs_ui.mmAcLineEdit2.clear()
        self.tabs_ui.mmAcLineEdit3.clear()
        self.tabs_ui.mmAcLineEdit5.clear()
        self.tabs_ui.mmAcLineEdit6.clear()
        self.tabs_ui.mmAcLineEdit7.clear()
        self.tabs_ui.mmAcLineEdit8.clear()
        self.tabs_ui.mmAcLineEdit9.clear()

    def old_pass_label(self, event):  # get old password by pressing label
        password = self.tabs_ui.mmCpasOtpLineEdit.text().strip()
        self.validate_old_password(password)

    def old_pass_enter(self, password):  # get old password by pressing enter
        password = password.strip()
        self.validate_old_password(password)

    def validate_old_password(self, password):  # here we validate old password label
        if Passwords.receive_hash(password):
            self.tabs_ui.mmCpasOtpLineEdit.setEnabled(False)
            self.tabs_ui.mmCpasArrowLabel.setEnabled(False)

            self.tabs_ui.mmCpasNpLineEdit.setEnabled(True)
            self.tabs_ui.mmCpasLineEdit.setEnabled(True)
            self.tabs_ui.mmCpasSaveLabel.setEnabled(True)
        else:
            self.msg.setWindowTitle("Error")
            self.msg.setText("Wrong password")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()
            self.tabs_ui.mmCpasOtpLineEdit.clear()

    def up_new_password(self):  # update password from tabs window
        if str(self.tabs_ui.mmCpasNpLineEdit.text()).strip() == str(self.tabs_ui.mmCpasLineEdit.text()).strip() and str(
                self.tabs_ui.mmCpasLineEdit.text()).strip() != '':
            has, salt = Passwords.make_hash_salt(str(self.tabs_ui.mmCpasLineEdit.text()).strip())
            UploadRetrievePassword.update_password(has, salt)  # password updated
            self.msg.setWindowTitle("Update password")
            self.msg.setText("Password updated successfully")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.exec_()
            self.tabs_ui.mmCpasOtpLineEdit.clear()
            self.tabs_ui.mmCpasNpLineEdit.clear()
            self.tabs_ui.mmCpasLineEdit.clear()
            self.tabs_ui.mmCpasOtpLineEdit.setEnabled(True)
            self.tabs_ui.mmCpasArrowLabel.setEnabled(True)
        else:
            self.msg.setWindowTitle("Error")
            self.msg.setText("Password din't match\nTry again")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()
            self.tabs_ui.mmCpasNpLineEdit.clear()
            self.tabs_ui.mmCpasLineEdit.clear()

    # here we close the respective tab and remove its track
    def close_respective_tab(self, index):
        tab_name = self.tabs_ui.tabs.tabText(index)
        self.track_tabs.remove(tab_name)  # removed track of tab that is to be closed
        self.tabs_ui.tabs.removeTab(index)  # remove the tab

    """ BELOW are OPEN TABS FUNCTIONS
       Here we open tabs and also add the track of the respective tab
    """
    def open_add_customer_tab(self, event):
        if "Add customer" not in self.track_tabs:  # if tab if not opened, then only open it
            self.tabs_ui.tabs.addTab(self.tabs_ui.add_customer, self.tabs_ui.icon2, "Add customer")  # write name of tab also in 3rd argument # here we open/added the tab
            self.track_tabs.append('Add customer')  # added the track of the tab
            self.tabs_ui.tabs.setCurrentIndex(len(self.track_tabs) - 1)  # focus on current opened index

    def open_edit_customer_tab(self, event):
        if "Edit customer" not in self.track_tabs:
            self.tabs_ui.tabs.addTab(self.tabs_ui.edit_customer, self.tabs_ui.icon3, "Edit customer")
            self.track_tabs.append('Edit customer')
            self.tabs_ui.tabs.setCurrentIndex(len(self.track_tabs) - 1)

    def open_add_item_tab(self, event):
        if "Add item" not in self.track_tabs:
            self.tabs_ui.tabs.addTab(self.tabs_ui.add_item, self.tabs_ui.icon4, "Add item")
            self.track_tabs.append('Add item')
            self.tabs_ui.tabs.setCurrentIndex(len(self.track_tabs) - 1)

    def open_edit_item_tab(self, event):
        if "Edit item" not in self.track_tabs:
            self.tabs_ui.tabs.addTab(self.tabs_ui.edit_item, self.tabs_ui.icon5, "Edit item")
            self.track_tabs.append('Edit item')
            self.tabs_ui.tabs.setCurrentIndex(len(self.track_tabs) - 1)

    def open_billing_tab(self, event):
        if "Invoice" not in self.track_tabs:
            self.tabs_ui.tabs.addTab(self.tabs_ui.invoice, self.tabs_ui.icon6, "Invoice")
            self.track_tabs.append('Invoice')
            self.tabs_ui.tabs.setCurrentIndex(len(self.track_tabs) - 1)
        self.invoice_number()

    def open_graphs_tab(self, event):
        if "Graphs" not in self.track_tabs:
            self.tabs_ui.tabs.addTab(self.tabs_ui.graphs, self.tabs_ui.icon7, "Graphs")
            self.track_tabs.append('Graphs')
            self.tabs_ui.tabs.setCurrentIndex(len(self.track_tabs) - 1)
            self.retrieve_data_from_db()

    def open_view_customer_tab(self, event):
        if "All customer's" not in self.track_tabs:
            self.tabs_ui.tabs.addTab(self.tabs_ui.ShowAllCustomers, self.tabs_ui.icon8, "All customer's")
            self.track_tabs.append("All customer's")
            self.tabs_ui.tabs.setCurrentIndex(len(self.track_tabs) - 1)
            # displaying contents of database
            self.all_customers('')

    def open_view_items_tab(self, event):
        if "All item's" not in self.track_tabs:
            self.tabs_ui.tabs.addTab(self.tabs_ui.ShowAllItems, self.tabs_ui.icon9, "All item's")
            self.track_tabs.append("All item's")
            self.tabs_ui.tabs.setCurrentIndex(len(self.track_tabs) - 1)
            # displaying contents of database
            self.all_items('')

    def open_change_password_tab(self, event):
        if "Change password" not in self.track_tabs:
            self.tabs_ui.tabs.addTab(self.tabs_ui.ChangePassword, self.tabs_ui.icon10, "Change password")
            self.track_tabs.append('Change password')
            self.tabs_ui.tabs.setCurrentIndex(len(self.track_tabs) - 1)

    """BELOW FUNCTIONS first hide the menu.py window then open main tabs window and open the tab of which name is passed"""
    def add_customer_tab(self, event):
        self.mwMainWindow.hide()
        self.open_main_tabs_window('add_customer_tab')

    def add_item_tab(self, event):
        self.mwMainWindow.hide()
        self.open_main_tabs_window('add_item_tab')

    def edit_customer_tab(self, event):
        self.mwMainWindow.hide()
        self.open_main_tabs_window('edit_customer_tab')

    def edit_item_tab(self, event):
        self.mwMainWindow.hide()
        self.open_main_tabs_window('edit_item_tab')

    def billing_tab(self, event):
        self.mwMainWindow.hide()
        self.open_main_tabs_window('billing_tab')

    def graphs_tab(self, event):
        self.mwMainWindow.hide()
        self.open_main_tabs_window('graphs_tab')

    def view_all_customer_tab(self, event):
        self.mwMainWindow.hide()
        self.open_main_tabs_window('view_all_customer_tab')

    def view_all_items_tab(self, event):
        self.mwMainWindow.hide()
        self.open_main_tabs_window('view_all_items_tab')

    def change_password_tab(self, event):
        self.mwMainWindow.hide()
        self.open_main_tabs_window('change_password_tab')

    """BELOW are the other functions... of login window and password reset window"""
    def enter(self, password):  # get password by pressing enter
        password = password.strip()
        self.check_password(password)

    def enter_label(self, event):  # get password by pressing arrow
        password = self.plUi.pPasswordLineEdit.text().strip()
        self.check_password(password)

    def check_password(self, password):
        if Passwords.receive_hash(password):
            self.main_option_window_setup('password_window')
        else:
            self.msg.setWindowTitle('Incorrect password')
            self.msg.setText('Password did not matched')
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()

    def reset_password(self, event):
        if Mail.check_internet_connection():  # if internet is connected
            self.msg.setWindowTitle("Email")
            self.msg.setText('OTP Send to registered email and phone number')
            self.msg.setIcon(QMessageBox.Information)
            self.msg.exec_()

            self.password_reset_window_setup('password_window')  # here we setup password reset window

            otp = randint(1000, 9999)  # 4 digit otp generated
            get = Mail().send_email(otp)  # otp sent to email if we are able to send email
            if get is True:
                self.otp = str(otp)
                self.fpUi.fpArrowLabel.mousePressEvent = self.opt_arrow_press  # otp_arrow_pressed
                self.fpUi.fpOtpLineEdit.returnPressed.connect(lambda: self.otp_enter(self.fpUi.fpOtpLineEdit.text().strip()))  # otp_enter_pressed
            elif get == -1:
                self.msg.setWindowTitle("Connection problem")
                self.msg.setText('Not connected to internet')
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()
            elif get == -2:
                self.msg.setWindowTitle("Check your email")
                self.msg.setText('Unable to send OTP to your email')
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()
            else:  # if we can't send email to some reason
                self.msg.setWindowTitle("Connection problem")
                self.msg.setText('Unable to send email, please try again.')
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()
            try:
                SMS(sms=str(otp)).send_sms()  # sms send to mobile number
            except Exception as e:
                print(e)
        else:  # if no internet connection
            self.msg.setWindowTitle("No Internet")
            self.msg.setText('Please connect to internet to reset password')
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()

    def opt_arrow_press(self, event):  # get otp by pressing arrow
        otp = self.fpUi.fpOtpLineEdit.text().strip()
        self.validate_otp(otp)

    def otp_enter(self, otp):  # get otp by pressing enter
        self.validate_otp(otp)

    def validate_otp(self, otp):
        if self.otp == otp:  # otp matched
            self.fpUi.fpSaveButton.setEnabled(True)  # set enabled
            self.fpUi.fpNpLineEdit.setEnabled(True)  # set enabled
            self.fpUi.fpCpLineEdit.setEnabled(True)  # set enabled
            self.fpUi.fpOtpLineEdit.setEnabled(False)  # disabled otp LineEdit
            self.fpUi.fpArrowLabel.setEnabled(False)  # disabled otp arrow
        else:  # otp din't matched
            self.msg.setWindowTitle("Error")
            self.msg.setText("OTP din't matched.")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()

    def get_new_password(self):
        if str(self.fpUi.fpNpLineEdit.text()).strip() == str(self.fpUi.fpCpLineEdit.text()).strip() and str(self.fpUi.fpNpLineEdit.text()).strip() != '':  # password matched
            has, salt = Passwords.make_hash_salt(str(self.fpUi.fpNpLineEdit.text()).strip())
            UploadRetrievePassword.update_password(has, salt)  # password updated
            self.msg.setWindowTitle("Reset password")
            self.msg.setText("Password updated successfully")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.exec_()
            self.main_login_window_setup('reset_window')  # here we went back to main password window
        else:  # password not matched
            self.msg.setWindowTitle("Error")
            self.msg.setText("Password din't match\nTry again")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.exec_()
            self.fpUi.fpNpLineEdit.clear()
            self.fpUi.fpCpLineEdit.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    UserInteraction()
    app.exec_()

