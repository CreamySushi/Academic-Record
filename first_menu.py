def firstMenu():
    print("\nMenu test:")
    print("Press 1 to log in")
    print("Press 2 to exit\n")
    option = input("Select an option: ")
    checkOption1(option)

def checkOption1(option):
    if option == "1":
        from main import login
        login()
    elif option == "2":
        exit()
    else:
        print("Invalid option. Please select a valid option.")
        firstMenu()
