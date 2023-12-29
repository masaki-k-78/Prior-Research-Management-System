import mysql.connector
from mysql.connector import Error

#参考：https://www.freecodecamp.org/japanese/news/connect-python-with-sql/

class Functions_MySQL():

    def __init__(self):
        ...

    #MySQLのサーバーに接続する関数
    def create_server_connection(self, host_name, user_name, user_password):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection
    
    #データベースを作成する関数
    def create_database(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            print("Database created successfully")
        except Error as err:
            print(f"Error: '{err}'")

    #データベースに接続する関数
    def create_db_connection(self, host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection
    
    #queryに入力されている命令を実行する関数
    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit() #データの変更に必要な呼び出し
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")

    #データを読み取る命令を実行する関数
    def read_query(self, connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall() #クエリの結果をタプルとして返す
            return result
        except Error as err:
            print(f"Error: '{err}'")


    def execute_list_query(self, connection, sql, val):
        cursor = connection.cursor()
        try:
            cursor.executemany(sql, val)
            connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")
