import csv

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
        csv_path = "Research_Data.csv"

        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(PRList)
        f.close()

        print("--Finished add basic info.")