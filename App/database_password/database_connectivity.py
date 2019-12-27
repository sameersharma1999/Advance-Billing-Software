import mysql.connector


class database_connection:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(host='localhost', user='root', password='', database='billing')