from PRMS.add_Prior_Research import Add_Prior_Research
from PRMS.main_System import Main_System

def main():
    print("--Welcome!")

    #起動時以外は，続けるかどうかをユーザーに尋ねる．
    input_corq = "c"
    while(input_corq == "c"):
        MS = Main_System()
        input_corq = input("--Press c to continue or q to stop: ")
        if input_corq == "q":
            print("--PRMS ended.")
        elif input_corq != "c":
            print("--Undefined alphabet. PRMS ended.")


if __name__ == '__main__':
    main()