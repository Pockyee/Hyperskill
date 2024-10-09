menu = {
    "main": "MAIN MENU\n0 Exit\n1 CRUD operations\n2 Show top ten companies by criteria\n\nEnter an option:",
    "crud": "CRUD MENU\n0 Back\n1 Create a company\n2 Read a company\n3 Update a company\n4 Delete a company\n5 List all companies\n\nEnter an option:",
    "topten": "TOP TEN MENU\n0 Back\n1 List by ND/EBITDA\n2 List by ROE\n3 List by ROA\n\nEnter an option:",
}


def crud():
    print(menu["crud"])
    choice = input()
    if choice == "0":
        pass
    elif choice in ["1", "2", "3", "4", "5"]:
        print("Not implemented!")
    else:
        print("Invalid option!")


def topten():
    print(menu["topten"])
    choice = input()
    if choice == "0":
        pass
    elif choice in ["1", "2", "3"]:
        print("Not implemented!")
    else:
        print("Invalid option!")


while True:
    print(menu["main"])
    choice = input()
    if choice == "0":
        print("Have a nice day!")
        exit()
    elif choice == "1":
        crud()
    elif choice == "2":
        topten()
    else:
        print("Invalid option!")
