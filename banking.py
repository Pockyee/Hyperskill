import random
import string
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

# Create a 'card' table if it doesn't already exist
cur.execute("""CREATE TABLE IF NOT EXISTS card (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  number TEXT,
  pin TEXT,
  balance INT DEFAULT 0
);""")
conn.commit()

# Menu options for account creation/login and actions after login
menu = [
    "1. Create an account\n" "2. Log into account\n" "0. Exit\n",
    "1. Balance\n" "2. Add income\n" "3. Do transfer\n" "4. Close account\n" "5. Log out\n" "0. Exit\n",
]

# Global variable to store logged-in card information
card = None

class Card:
    def __init__(self):
        # Initialize a card with default BIN, null account identifier, checksum, pin, and balance
        self.bin = 400000
        self.account_identifier = None
        self.checksum = 0
        self.pin = None
        self.balance = 0

    # Generate a random 9-digit account identifier for the card
    def gen_account_identifier(self):
        self.account_identifier = "".join(random.choices(string.digits, k=9))

    # Generate a random 4-digit pin for the card
    def gen_pin(self):
        self.pin = "".join(random.choices(string.digits, k=4))


# Calculate the checksum for a card number using the Luhn algorithm
def calculate_checksum(card_number):
    digits = [int(d) for d in str(card_number)]
    checksum = 0
    reverse_digits = digits[::-1]  # Reverse the digits to apply the algorithm
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 0:  # Double every second digit
            doubled = digit * 2
            if doubled > 9:
                doubled -= 9  # Subtract 9 from any results greater than 9
            checksum += doubled
        else:
            checksum += digit
    # Return the checksum that makes the entire number divisible by 10
    return (10 - (checksum % 10)) % 10


# Function to create a new account and store it in the database
def create_account():
    card1 = Card()
    Card.gen_account_identifier(card1)
    Card.gen_pin(card1)
    card1.checksum = calculate_checksum(f"{card1.bin}{card1.account_identifier}")
    full_card_number = f"{card1.bin}{card1.account_identifier}{card1.checksum}"
    # Insert the card data into the 'card' table
    cur.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)",
                (full_card_number, card1.pin, card1.balance))
    conn.commit()
    # Display the new card details
    print(
        "Your card has been created\n"
        "Your card number:\n"
        f"{card1.bin}{card1.account_identifier}{card1.checksum}\n"
        "Your card PIN:\n"
        f"{card1.pin}\n"
    )


# Function to log into an account by checking the card number and pin
def login():
    global card
    input_id = input("Enter your card number:")
    input_pin = input("Enter your PIN:")
    # Query the database for matching card number and pin
    cur.execute("SELECT * FROM card WHERE number = ? AND pin = ?", (input_id, input_pin))
    card = cur.fetchone()
    if card:
        print("You have successfully logged in!")
        return True
    else:
        print("Wrong card number or PIN!")
        return False


# Function to check and display the balance of the logged-in account
def balance():
    cur.execute("SELECT * FROM card WHERE number = ?", (card[1],))
    balance = cur.fetchone()
    print(f"Balance: {balance[3]}\n")


# Function to add income to the logged-in account
def add_income():
    income = input("Enter income:\n")
    # Update the balance in the database
    cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?;", (income, card[1]))
    conn.commit()


# Function to transfer money to another account
def do_transfer():
    receiver = input("Transfer\nEnter card number:\n")
    # Ensure the receiver's card isn't the same as the sender's card
    if receiver == card[1]:
        print("You can't transfer money to the same account!")
    # Validate the card number using the checksum
    elif int(receiver[15]) != calculate_checksum(receiver[:15]):
        print("Probably you made a mistake in the card number. Please try again!")
    else:
        # Check if the receiver's card exists in the database
        cur.execute("SELECT * FROM card WHERE number = ?", (receiver,))
        re_card = cur.fetchone()
        if re_card:
            tran_amout = input("Enter how much money you want to transfer:\n")
            # Check if the sender has enough balance to transfer
            cur.execute("SELECT * FROM card WHERE number = ?", (card[1],))
            balance = cur.fetchone()
            if float(balance[3]) >= float(tran_amout):
                # Perform the transfer by subtracting from sender and adding to receiver
                cur.execute("UPDATE card SET balance = balance - ? WHERE number = ?;", (tran_amout, card[1]))
                cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?;", (tran_amout, re_card[1]))
                conn.commit()
                print("Success!")
            else:
                print("Not enough money!\n")
        else:
            print("Such a card does not exist.")


# Function to close the logged-in account
def close_account():
    cur.execute("DELETE FROM card WHERE number = ?", (card[1],))
    conn.commit()
    print("The account has been closed!\n")


# Function to handle actions for a logged-in user
def loggedin():
    while True:
        print(menu[1])
        sub_choice = int(input())
        if sub_choice == 1:
            balance()
        elif sub_choice == 2:
            add_income()
        elif sub_choice == 3:
            do_transfer()
        elif sub_choice == 4:
            close_account()
            break
        elif sub_choice == 5:
            print("You have successfully logged out!")
            break
        elif sub_choice == 0:
            exit()


# Main loop to handle account creation, login, and exit
while True:
    print(menu[0])
    choice = int(input())
    if choice == 1:
        create_account()
    elif choice == 2:
        if login():
            loggedin()
    elif choice == 0:
        exit()