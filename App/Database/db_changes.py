from App.Database.database_connection import DBConnection

"""Here we handle password (hash salt) and email in database"""


class UploadRetrievePassword:  # here we upload and retrieve password (hash salt) and email
    @classmethod  # here we retrieve the hash and salt from the db
    def retrieve_salt_pass(cls):
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        my_cursor.execute("""SELECT * FROM passwords""")
        r_p = my_cursor.fetchone()
        return r_p

    @classmethod  # here we retrieve registered email
    def retrieve_email(cls):
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        my_cursor.execute("""SELECT * FROM passwords""")
        r_p = my_cursor.fetchone()
        return r_p[2]

    @classmethod
    def retrieve_ph_no(cls):  # retrieve registered phone number
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        my_cursor.execute("""SELECT * FROM passwords""")
        r_p = my_cursor.fetchone()
        return r_p[3]

    @classmethod
    def update_password(cls, has, salt):  # update password (hash + salt)
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()

        email = UploadRetrievePassword.retrieve_email()  # get email
        data = [has, salt, email]
        query = """ UPDATE passwords SET hash = %s, salt = %s WHERE email = %s """
        my_cursor.execute(query, data)
        my_db.commit()


"""Here we do update Customer and Items details"""


class Customer:  # In class Customer we will handle all the customer's update, insert and search
    @classmethod
    def insert_customer(cls, cus_det):  # cus_det contains customer details list
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        data = (cus_det[0], cus_det[1], cus_det[2], cus_det[3], cus_det[4], cus_det[5], cus_det[6], cus_det[7],
                cus_det[8])
        sql_formula = ("""INSERT INTO customers (first_name,last_name,address,state,city,gst_number,
                                                            addhar_card_number,pan_number,phone_number)
                                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
        my_cursor.execute(sql_formula, data)
        my_db.commit()

    @classmethod
    def update_customer(cls, cus_det, mob_no):  # cus_det contains customer details list
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        data = [cus_det[0], cus_det[1], cus_det[2], cus_det[3], cus_det[4], cus_det[5], cus_det[6], cus_det[7],
                cus_det[8]]
        my_cursor.execute(""" DELETE FROM customers WHERE phone_number = %s""" % mob_no)
        my_db.commit()
        sql_formula = ("""INSERT INTO customers (first_name,last_name,address,state,city,gst_number,
                                                            addhar_card_number,pan_number,phone_number)
                                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
        my_cursor.execute(sql_formula, data)
        my_db.commit()

    @classmethod
    def search_customer(cls, mob_no):  # search customer using mobile number
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        sql_formula = "Select * from customers WHERE phone_number= (%s) "
        my_cursor.execute(sql_formula, (mob_no,))
        for data in my_cursor:
            temp_dic = [data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8],
                        data[9]]
            return temp_dic
        my_db.commit()

    @classmethod
    def get_customers(cls):
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        my_cursor.execute(""" SELECT * FROM customers order by first_name asc""")
        result = my_cursor.fetchall()
        return result


class Items:  # In class Items we will handle all the items update, insert and search
    @classmethod
    def insert_item(cls, item_det):  # item_det contains customer details list
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        data = (item_det[0], item_det[1], item_det[2], item_det[3], item_det[4])
        sql_formula = ("""INSERT INTO items (item_id, item_name, price, gst_per, hsn_code)
                                             VALUES(%s,%s,%s,%s,%s)""")
        my_cursor.execute(sql_formula, data)
        my_db.commit()

    @classmethod
    def update_item(cls, item_det, item_id):  # item_det contains customer details list
        print(item_det)
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        data = [item_det[0], item_det[1], item_det[2], item_det[3], item_det[4]]
        my_cursor.execute(""" DELETE FROM items WHERE  `item_id` = '%s' """ % item_id)
        my_db.commit()
        sql_formula = ("""INSERT INTO items (item_id,item_name,price,gst_per,hsn_code)
                                                     VALUES(%s,%s,%s,%s,%s)""")
        my_cursor.execute(sql_formula, data)
        my_db.commit()

    @classmethod
    def search_item(cls, item_id):  # search item using item id
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        my_cursor.execute(""" SELECT * FROM items WHERE item_id = '%s' """ % item_id)
        result = my_cursor.fetchone()
        return result

    @classmethod
    def get_items(cls):
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        my_cursor.execute(""" SELECT * FROM items order by item_name asc""")
        result = my_cursor.fetchall()
        return result


class Invoice:

    @classmethod
    def insert_invoice_data(cls, invoice_det):
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        data = [invoice_det[0], invoice_det[1], invoice_det[2]]  # only date and grand total is saved
        sql_formula = """ INSERT INTO invoice(date, total_without_gst, grand_total_with_gst) VALUES(%s, %s, %s)"""
        my_cursor.execute(sql_formula, data)
        my_db.commit()

    @classmethod
    def retrieve_invoice_data(cls):
        my_db = DBConnection.get_connection()
        my_cursor = my_db.cursor()
        date = """SELECT date FROM invoice"""
        my_cursor.execute(date)
        date = my_cursor.fetchall()
        total_without_gst = """SELECT total_without_gst FROM invoice"""
        my_cursor.execute(total_without_gst)
        total_without_gst = my_cursor.fetchall()
        grand_total_with_gst = """SELECT grand_total_with_gst FROM invoice"""
        my_cursor.execute(grand_total_with_gst)
        grand_total_with_gst = my_cursor.fetchall()
        return date, total_without_gst, grand_total_with_gst
