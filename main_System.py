from PRMS.add_Prior_Research import Add_Prior_Research

class Main_System():
    def __init__(self):
        print("What do you do?")
        print("1: add research, 2: coming soon...")
        user_input = input()

        if user_input == "1":
            APR = Add_Prior_Research()
            APR.add_title(input("Title: "))
        else:
            print("Undefined number.")
