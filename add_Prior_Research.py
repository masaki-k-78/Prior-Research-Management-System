import csv
from PRMS.functions_Mysql import Functions_MySQL

#論文の基本情報を追加するための機能を担う
class Add_Prior_Research():

    def __init__(self):
        print("--OK")

    def add_basic_info(self, PRList):
        PRList.append(input("Title: "))
        PRList.append(input("Author: "))
        PRList.append(input("Conference: "))
        PRList.append(input("Date: "))

    def write_basic_info(self, PRList):
        csv_path = "PRMS/Research_Data.csv"

        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(PRList)
        f.close()

        print("--Finished add basic info.")

    #以下，MySQLを用いた実装

    def add_basic_info_to_mysql(self, PRList):
        pr_title = input("Title: ")
        pr_author = input("Author: ")
        pr_conference = input("Conferene: ")
        pr_date = input("Date: ")
        PRList.append((pr_title, pr_author, pr_conference, pr_date))
        print(PRList)

    def write_basic_info_to_mysql(self, PRList, connection):
        sql = '''
        INSERT INTO mine (PR_title, PR_author, PR_conference, PR_date) 
        VALUES (%s, %s, %s, %s)
        '''

        FM = Functions_MySQL()
        FM.execute_list_query(connection, sql, PRList)
