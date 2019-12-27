import mysql.connector


class DBConnection:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(host='localhost', user='root', password='', database='billing')
