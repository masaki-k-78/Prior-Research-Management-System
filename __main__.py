from PRMS.add_Prior_Research import Add_Prior_Research
from PRMS.main_System import Main_System

def main():
    print("--Welcome!")
    input_corq = input("--Press c to continue or q to stop.: ")
    
    if input_corq == "c" or input_corq == "q":
        while(input_corq != "q"):
            MS = Main_System()
            input_corq = input("--Press c to continue or q to stop.: ")
        if input_corq == "q":
            print("--PRMS ended.")
    else:
        print("--Undefined alphabet. PRMS ended.")


if __name__ == '__main__':
    main()