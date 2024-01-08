from functions_Mysql import Functions_MySQL
from dotenv import load_dotenv
import os

#userにあるテーブル
# normal_users (
#   user_id INT AUTO_INCREMENT,
#   user_name VARCHAR(40) NOT NULL,
#   user_pass VARCHAR(40) NOT NULL,
#   user_age VARCHAR(3) NOT NULL,
#   PRIMARY KEY (user_id)
#   );

class Get_UsersData():
    def __init__(self):
        ...

    def get_data(self):
        #MySQLに接続するためのパスワードを環境変数として.envに保存して使用する．
        load_dotenv()
        PASS = os.getenv("MYSQL_PASS") 

        #MySQLへのコネクションの確立．
        FM = Functions_MySQL()
        connection_users = FM.create_db_connection("localhost", "root", PASS, "users")

        users_dict = dict()
        usr = "normal_users"
        q1 = f"""
        SELECT user_name, user_pass
        FROM {usr};
        """

        results = FM.read_query(connection_users, q1)
        for n in results:
            users_dict[n[0]] = n[1]
        
        return users_dict