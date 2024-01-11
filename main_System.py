from PRMS.add_Prior_Research import Add_Prior_Research
from PRMS.search_Prior_Research import Search_Prior_Research
from PRMS.show_Prior_Research import Show_Prior_Research
from PRMS.functions_Mysql import Functions_MySQL

#テーブルの作成について
#prior_research内のテーブルmineはあらかじめ作成してある．(最終的にはユーザを増やせるようにする)
#↓がテーブルの内容
# """
# CREATE TABLE mine (
#   research_id INT AUTO_INCREMENT,
#   PR_title VARCHAR(100) NOT NULL,
#   PR_author VARCHAR(100) NOT NULL,
#   PR_conference VARCHAR(100) NOT NULL,
#   PR_date VARCHAR(4),
#   PRIMARY KEY (research_id)
#   );
# """

#システムの基本的な動作を担う
class Main_System():
    def __init__(self):
        PASS = "" #任意のパスワード(MySQL)
        #MySQLへのコネクションの確立．
        FM = Functions_MySQL()
        connection = FM.create_db_connection("localhost", "root", PASS, "prior_research")
        
        print("--What do you do?")
        print("1: add research, 2: search research(title), 3: search research(author), 4: show research")
        user_input = input()

        if user_input == "1":
            self.ar(connection)
        elif user_input == "2":
            self.srt(connection)
        elif user_input == "3":
            self.sra(connection)
        elif user_input == "4":
            self.shr(connection)
        else:
            print("Undefined number.")

    def ar(self, connection):
        PRList = []

        APR = Add_Prior_Research()
        # #論文の基本情報を入力
        # APR.add_basic_info(PRList)
        # #ファイルに書き込み
        # APR.write_basic_info(PRList)

        #以下，MySQLを使った実装
        APR.add_basic_info_to_mysql(PRList)
        APR.write_basic_info_to_mysql(PRList, connection)


    def srt(self, connection):
        # path = "PRMS/Research_Data.csv"
        SPR = Search_Prior_Research()
        # SPR.search_title(path)

        #以下，MySQLを使った実装
        SPR.search_wMySQL(connection, "PR_title")

    def sra(self, connection):
        # path = "PRMS/Research_Data.csv"
        SPR = Search_Prior_Research()
        # SPR.search_author(path)

        #以下，MySQLを使った実装
        SPR.search_wMySQL(connection, "PR_author")

    def shr(self, connection):
        # path = "PRMS/Research_Data.csv"
        SHPR = Show_Prior_Research()
        # SHPR.show_research(path)

        #以下，MySQLを使った実装
        SHPR.show_research_from_MySQL(connection)
