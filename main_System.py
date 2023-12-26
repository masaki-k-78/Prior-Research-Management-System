from PRMS.add_Prior_Research import Add_Prior_Research
from PRMS.search_Prior_Research import Search_Prior_Research

#システムの基本的な動作を担う
class Main_System():
    def __init__(self):
        print("--What do you do?")
        print("1: add research, 2: search research", "3: coming soon...")
        user_input = input()

        if user_input == "1":
            self.ar()
        elif user_input == "2":
            self.sr()
        else:
            print("Undefined number.")

    def ar(self):
        PRList = []
        APR = Add_Prior_Research()
        #論文の基本情報を入力
        APR.add_basic_info(PRList)
        #ファイルに書き込み
        APR.write_basic_info(PRList)

    def sr(self):
        path = "PRMS/Research_Data.csv"
        SPR = Search_Prior_Research()
        SPR.search_title(path)
