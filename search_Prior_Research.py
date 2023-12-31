import csv
from PRMS.functions_Mysql import Functions_MySQL

class Search_Prior_Research():

    def __init__(self):
        print("ok")

    #検索機能．iに入れる数値で検索対象を決める
    def search(self, path, i):
        result_list = []
        query = input("input query: ")
        with open(path) as f:
            title_list = csv.reader(f)

            for n in title_list:
                if query in n[i]:
                    result_list.append(n[0])

            f.close()

        if len(result_list) == 0:
            print("Not found.")
        else:
            for n in result_list:
                print(n)

    def search_title(self, path):
        self.search(path, 0)

    def search_author(self, path):
        self.search(path, 1)

    def search_wMySQL(self, connection, category):
        query = input("input query: ")

        #部分一致を行うための処理
        q1 = f"""
        SELECT *
        FROM mine
        WHERE {category} LIKE "%{query}%";
        """

        FM = Functions_MySQL()
        results = FM.read_query(connection, q1)
        for n in results:
            print(n)

