from App.database_password.register_hash_pass import RegPass
from App.database_password.database_connectivity import database_connection


class MakeChanges:

    @staticmethod
    def upload():
        my_db = database_connection.get_connection()
        my_cursor = my_db.cursor()

        h_p_received = RegPass.reg()
        data = [h_p_received[0], h_p_received[1]]

        sql_formula1 = ("""INSERT INTO passwords (hash, salt)
                                                 VALUES(%s,%s)""")
        my_cursor.execute(sql_formula1, data)
        my_db.commit()

    @staticmethod
    def retrive():
        my_db = database_connection.get_connection()
        my_cursor = my_db.cursor()

        my_cursor.execute("""SELECT * FROM passwords""")
        r_p = my_cursor.fetchone()
        return r_p


