import mysql.connector


class Connection:
    @staticmethod
    def dbConnnect():
        mydb=mysql.connector.connect(host="localhost", user="root",passwd="", database="billing")

        return mydb
