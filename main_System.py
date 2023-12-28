from PRMS.add_Prior_Research import Add_Prior_Research
from PRMS.search_Prior_Research import Search_Prior_Research
from PRMS.show_Prior_Research import Show_Prior_Research

#システムの基本的な動作を担う
class Main_System():
    def __init__(self):
        print("--What do you do?")
        print("1: add research, 2: search research(title), 3: search research(author), 4: show research")
        user_input = input()

        if user_input == "1":
            self.ar()
        elif user_input == "2":
            self.srt()
        elif user_input == "3":
            self.sra()
        elif user_input == "4":
            self.shr()
        else:
            print("Undefined number.")

    def ar(self):
        PRList = []
        APR = Add_Prior_Research()
        #論文の基本情報を入力
        APR.add_basic_info(PRList)
        #ファイルに書き込み
        APR.write_basic_info(PRList)

    def srt(self):
        path = "PRMS/Research_Data.csv"
        SPR = Search_Prior_Research()
        SPR.search_title(path)

    def sra(self):
        path = "PRMS/Research_Data.csv"
        SPR = Search_Prior_Research()
        SPR.search_author(path)

    def shr(self):
        path = "PRMS/Research_Data.csv"
        SHPR = Show_Prior_Research()
        SHPR.show_research(path)
