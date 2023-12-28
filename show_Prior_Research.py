import csv

class Show_Prior_Research():

    def __init__(self):
        print("ok")

    def show_research(self, path):

        with open(path) as f:
            title_list = csv.reader(f)

            for n in title_list:
                print(n[0], n[1], sep=", ")

            f.close()