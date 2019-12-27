# from bakend_database.database_connection import DBConnection


class InDeUp:
    d = []
    c = []
    b = []
    a = []
    @staticmethod
    def upload_to_database_customer(entry, m_d):
        my_cursor = m_d.cursor()
        for i in entry.values():
            InDeUp.a.append(i)
        data = (InDeUp.a[0], InDeUp.a[1], InDeUp.a[2], InDeUp.a[3], InDeUp.a[4], InDeUp.a[5], InDeUp.a[6],
                InDeUp.a[7], InDeUp.a[8])
        InDeUp.a.clear()
        sql_formula1 = ("""INSERT INTO customers (first_name,last_name,address,state,city,gst_number,
                                                    addhar_card_number,pan_number,phone_number)
                                 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
        my_cursor.execute(sql_formula1, data)
        m_d.commit()

    @staticmethod
    def upload_to_database_items(entry, m_d):
        my_cursor = m_d.cursor()
        for i in entry.values():
            InDeUp.b.append(i)
        data = (InDeUp.b[0], InDeUp.b[1], InDeUp.b[2], InDeUp.b[3], InDeUp.b[4])
        sql_formula1 = ("""INSERT INTO items (item_id, item_name, price, gst_per, hsn_code)
                                     VALUES(%s,%s,%s,%s,%s)""")
        InDeUp.b.clear()
        my_cursor.execute(sql_formula1, data)
        m_d.commit()

    @staticmethod
    def search_data_customer(rec_data, m_d):
        my_cursor = m_d.cursor()
        my_cursor.execute(""" SELECT * FROM customers WHERE phone_number = %s """ % rec_data)

        result = my_cursor.fetchone()
        return result

    @staticmethod
    def update_to_database_customer(entry, m_d, ph_re):
        my_cursor = m_d.cursor()
        for i in entry.values():
            InDeUp.c.append(i)
        data = [InDeUp.c[0], InDeUp.c[1], InDeUp.c[2], InDeUp.c[3], InDeUp.c[4], InDeUp.c[5], InDeUp.c[6], InDeUp.c[7],
                InDeUp.c[8]]
        my_cursor.execute(""" DELETE FROM customers WHERE phone_number = %s""" % ph_re)
        m_d.commit()
        sql_formula1 = ("""INSERT INTO customers (first_name,last_name,address,state,city,gst_number,
                                                            addhar_card_number,pan_number,phone_number)
                                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
        my_cursor.execute(sql_formula1, data)
        m_d.commit()
        InDeUp.c.clear()

    @staticmethod
    def search_data_item(rec_data, m_d):
        my_cursor = m_d.cursor()
        my_cursor.execute(""" SELECT * FROM items WHERE item_id = '%s' """ % rec_data)
        result = my_cursor.fetchone()
        print(result)
        return result

    @staticmethod
    def update_to_database_item(entry, m_d, i_code):
        my_cursor = m_d.cursor()
        for i in entry.values():
            InDeUp.d.append(i)
        data = (InDeUp.d[0], InDeUp.d[1], InDeUp.d[2], InDeUp.d[3], InDeUp.d[4])
        my_cursor.execute(""" DELETE FROM items WHERE  `item_id` = '%s' """ % i_code)
        m_d.commit()
        sql_formula1 = ("""INSERT INTO items (item_id,item_name,price,gst_per,hsn_code)
                                             VALUES(%s,%s,%s,%s,%s)""")
        my_cursor.execute(sql_formula1, data)
        m_d.commit()
        InDeUp.d.clear()

    # @ staticmethod
    # def retrive_hash_salt():
    #     my_conn = DBConnection.get_connection()
    #     my_cursor = my_conn.cursor()
    #     my_cursor.execute('SELECT * FROM password_check')
    #     result = my_cursor.fetchone()
    #     my_conn.commit()
    #     return result
