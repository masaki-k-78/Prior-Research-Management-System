import csv

class Search_Prior_Research():

    def __init__(self):
        print("ok")

    #タイトルの部分一致検索を行う
    def search_title(self, path):
        result_list = []
        query = input("input query: ")
        with open(path) as f:
            title_list = csv.reader(f)

            for n in title_list:
                if query in n[0]:
                    result_list.append(n[0])

            f.close()

        if len(result_list) == 0:
            print("Not found.")
        else:
            for n in result_list:
                print(n)
