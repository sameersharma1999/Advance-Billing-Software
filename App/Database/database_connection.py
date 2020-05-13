import mysql.connector


class DBConnection:
    @classmethod
    def get_connection(cls):
        return mysql.connector.connect(host='localhost', user='root', password='', database='billing')