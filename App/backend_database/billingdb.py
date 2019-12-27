from App.backend_database.getConnection import Connection


class FetchData:
    @staticmethod
    def fetchdata(id):
        db_obj=Connection.dbConnnect()
        mycursor = db_obj.cursor()
        statement = "Select * from items WHERE item_id= '%s' " % id
        return_list = mycursor.execute(statement)
        for return_list in mycursor:
            return return_list[0], return_list[1], return_list[2], return_list[3], return_list[4]

    @staticmethod
    def fetchCustomerdet(mobno):
        db_objj=Connection.dbConnnect()
        mycursor_obj=db_objj.cursor()
        stmt="Select * from customers WHERE phone_number= %s " %mobno
        mycursor_obj.execute(stmt)
        for return_lst in mycursor_obj:

            return return_lst[0],return_lst[1],return_lst[2],return_lst[3],return_lst[4]

    @staticmethod
    def fetchAllCustomerdet(mobno):
        db_objj = Connection.dbConnnect()
        mycursor_obj = db_objj.cursor()
        stmt = "Select * from customers WHERE phone_number= (%s) "
        mycursor_obj.execute(stmt,(mobno,))
        for return_lst in mycursor_obj:
            temp_dic = [return_lst[1], return_lst[2], return_lst[3], return_lst[6], return_lst[7], return_lst[8], return_lst[9]]
            return temp_dic

