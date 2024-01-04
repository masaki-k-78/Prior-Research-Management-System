import csv
from PRMS.functions_Mysql import Functions_MySQL

class Show_Prior_Research():

    def __init__(self):
        print("ok")

    def show_research(self, path):

        with open(path) as f:
            title_list = csv.reader(f)

            for n in title_list:
                print(n[0], n[1], sep=", ")

            f.close()

    def show_research_from_MySQL(self, connection):
        FM = Functions_MySQL()
        q1 = """
        SELECT *
        FROM mine
        """
        results = FM.read_query(connection, q1)
        for n in results:
            print(n)