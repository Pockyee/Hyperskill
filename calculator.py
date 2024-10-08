import csv
import os
from sqlalchemy import create_engine, Column, String, Float, desc
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Define main menu options
menu = {
    "main": "MAIN MENU\n0 Exit\n1 CRUD operations\n2 Show top ten companies by criteria\n\nEnter an option:",
    "crud": "CRUD MENU\n0 Back\n1 Create a company\n2 Read a company\n3 Update a company\n4 Delete a company\n5 List all companies\n\nEnter an option:",
    "topten": "TOP TEN MENU\n0 Back\n1 List by ND/EBITDA\n2 List by ROE\n3 List by ROA\n\nEnter an option:",
}

# Create the base class for SQLAlchemy ORM
Base = declarative_base()


# Define Companies table schema (holds basic company information)
class Companies(Base):
    __tablename__ = "companies"

    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)


# Define Financial table schema (holds financial data for companies)
class Financial(Base):
    __tablename__ = "financial"

    ticker = Column(String, primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


# Utility function to replace empty fields with None (used for data validation)
def replace_empty_with_none(dict):
    for key, value in dict.items():
        if value == "":
            dict[key] = None
    return dict


# Initialize the database engine and create a session
def set_engine():
    global session
    engine = create_engine("sqlite:///investor.db", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()


# Populate the database from CSV files if it doesn't exist
def create_db():
    with open("./test/companies.csv", "r") as companies:
        reader = csv.DictReader(companies)
        for row in reader:
            company = Companies(
                ticker=row["ticker"], name=row["name"], sector=row["sector"]
            )
            session.add(company)
            session.commit()

    with open("./test/financial.csv", "r") as financial:
        reader = csv.DictReader(financial)
        for row in reader:
            replace_empty_with_none(row)
            financial_data = Financial(
                ticker=row["ticker"],
                ebitda=row["ebitda"],
                sales=row["sales"],
                net_profit=row["net_profit"],
                market_price=row["market_price"],
                net_debt=row["net_debt"],
                assets=row["assets"],
                equity=row["equity"],
                cash_equivalents=row["cash_equivalents"],
                liabilities=row["liabilities"],
            )
            session.add(financial_data)
            session.commit()


# Function to create a new company and its financial data
def create_a_company():
    try:
        # Input for the new company data
        ticker_ = input("Enter ticker (in the format 'MOON'):")
        company_ = input("Enter company (in the format 'Moon Corp'):")
        industries_ = input("Enter industries (in the format 'Technology'):")
        ebitda_ = input("Enter ebitda (in the format '987654321'):")
        sales_ = input("Enter sales (in the format '987654321'):")
        net_profit_ = input("Enter net profit (in the format '987654321'):")
        market_price_ = input("Enter market price (in the format '987654321'):")
        net_debt_ = input("Enter net debt (in the format '987654321'):")
        assets_ = input("Enter assets (in the format '987654321'):")
        equity_ = input("Enter equity (in the format '987654321'):")
        cash_equivalents_ = input("Enter cash equivalents (in the format '987654321'):")
        liabilities_ = input("Enter liabilities (in the format '987654321'):")
        # Add company and financial data to the session and commit to the database
        session.add(Companies(ticker=ticker_, name=company_, sector=industries_))
        session.add(
            Financial(
                ticker=ticker_,
                ebitda=ebitda_,
                sales=sales_,
                net_profit=net_profit_,
                market_price=market_price_,
                net_debt=net_debt_,
                assets=assets_,
                equity=equity_,
                cash_equivalents=cash_equivalents_,
                liabilities=liabilities_,
            )
        )
        session.commit()
        print("Company created successfully!")
    except IntegrityError:
        session.rollback()


# Function to read and retrieve a company by name
def read_company():
    x = input("Enter company name:\n")
    results = session.query(Companies).filter(Companies.name.like(f"%{x}%")).all()
    if results:
        i = 0
        for company in results:
            print(f"{i} {company.name}")
            i += 1
    else:
        print("Company not found!")
        return None
    j = int(input("Enter company number:\n"))
    return results[j]


# Function to display financial data for a specific company
def financial_data(ticker):
    finance = session.query(Financial).filter(Financial.ticker == ticker).first()
    pe_ratio = (
        round(finance.market_price / finance.net_profit, 2)
        if finance.net_profit
        else None
    )
    ps_ratio = round(finance.market_price / finance.sales, 2) if finance.sales else None
    pb_ratio = (
        round(finance.market_price / finance.assets, 2) if finance.assets else None
    )
    nd_ebitda = round(finance.net_debt / finance.ebitda, 2) if finance.ebitda else None
    roe = round(finance.net_profit / finance.equity, 2) if finance.equity else None
    roa = round(finance.net_profit / finance.assets, 2) if finance.assets else None
    la_ratio = (
        round(finance.liabilities / finance.assets, 2) if finance.assets else None
    )
    print(
        f"""P/E = {pe_ratio}\nP/S = {ps_ratio}\nP/B = {pb_ratio}\nND/EBITDA = {nd_ebitda}\nROE = {roe}\nROA = {roa}\nL/A = {la_ratio}"""
    )


# Function to update financial data for a company
def update_company(ticker):
    finance = session.query(Financial).filter(Financial.ticker == ticker).first()
    ebitda_ = input("Enter ebitda (in the format '987654321'):")
    sales_ = input("Enter sales (in the format '987654321'):")
    net_profit_ = input("Enter net profit (in the format '987654321'):")
    market_price_ = input("Enter market price (in the format '987654321'):")
    net_debt_ = input("Enter net debt (in the format '987654321'):")
    assets_ = input("Enter assets (in the format '987654321'):")
    equity_ = input("Enter equity (in the format '987654321'):")
    cash_equivalents_ = input("Enter cash equivalents (in the format '987654321'):")
    liabilities_ = input("Enter liabilities (in the format '987654321'):")

    finance.ebitda = ebitda_
    finance.sales = sales_
    finance.net_profit = net_profit_
    finance.market_price = market_price_
    finance.net_debt = net_debt_
    finance.assets = assets_
    finance.equity = equity_
    finance.cash_equivalents = cash_equivalents_
    finance.liabilities = liabilities_

    session.commit()
    print("Company updated successfully!")


# Function to delete a company and its financial data from the database
def delete_company(ticker):
    session.query(Companies).filter(Companies.ticker == ticker).delete()
    session.query(Financial).filter(Financial.ticker == ticker).delete()
    session.commit()
    print("Company deleted successfully!")


# Function to list all companies in the database
def list_company():
    results = session.query(Companies).order_by(Companies.ticker).all()
    print("COMPANY LIST")
    for company in results:
        print(f"{company.ticker} {company.name} {company.sector}")


# Function to list the top 10 companies by different ratios
def top_nd_ebitda():
    results = (
        session.query(Financial)
        .filter(Financial.ebitda != 0)
        .order_by(desc(Financial.net_debt / Financial.ebitda))
        .limit(10)
        .all()
    )
    print("TICKER ND/EBITDA")
    for company in results:
        print(f"{company.ticker} {round(company.net_debt/company.ebitda, 2)}")


def top_roe():
    results = (
        session.query(Financial)
        .filter(Financial.equity != 0)
        .order_by(desc(Financial.net_profit / Financial.equity))
        .limit(10)
        .all()
    )
    print("TICKER ROE")
    for company in results:
        print(f"{company.ticker} {round(company.net_profit/company.equity, 2)}")


def top_roa():
    results = (
        session.query(Financial)
        .filter(Financial.assets != 0)
        .order_by(desc(Financial.net_profit / Financial.assets))
        .limit(10)
        .all()
    )
    print("TICKER ROA")
    for company in results:
        print(f"{company.ticker} {round(company.net_profit/company.assets, 2)}")


# Function to manage Create, Read, Update, and Delete (CRUD) operations
def crud():
    print(menu["crud"])  # Display CRUD menu
    choice = input()

    # Handle user selection for different CRUD operations
    if choice == "0":  # Go back to the main menu
        pass
    elif choice == "1":  # Create a new company
        create_a_company()
    elif choice == "2":  # Read and display details of a company
        x = read_company()
        if x:
            print(f"{x.ticker} {x.name}")
            financial_data(x.ticker)
        else:
            return None
    elif choice == "3":  # Update an existing company
        x = read_company()
        if x:
            update_company(x.ticker)
        else:
            return None
    elif choice == "4":  # Delete a company
        x = read_company()
        if x:
            delete_company(x.ticker)
        else:
            return None
    elif choice == "5":  # List all companies
        list_company()
    else:  # Invalid input handling
        print("Invalid option!")


# Function to manage displaying the top ten companies based on financial metrics
def topten():
    print(menu["topten"])  # Display top ten menu
    choice = input()

    # Handle user selection for different ranking criteria
    if choice == "0":  # Go back to the main menu
        pass
    elif choice == "1":  # Display top 10 companies by ND/EBITDA
        top_nd_ebitda()
    elif choice == "2":  # Display top 10 companies by ROE
        top_roe()
    elif choice == "3":  # Display top 10 companies by ROA
        top_roa()
    else:  # Invalid input handling
        print("Invalid option!")


# Entry point of the program
print("Welcome to the Investor Program!")

# Set up the database if it exists, or create it if it doesn't
if os.path.exists("investor.db"):
    set_engine()  # Initialize the database engine and session
else:
    set_engine()  # Initialize the engine
    create_db()  # Create the database from CSV files if it doesn't exist

# Main loop to keep the program running until the user chooses to exit
while True:
    print(menu["main"])  # Display main menu
    choice = input()

    # Handle user input to navigate the program
    if choice == "0":  # Exit the program
        print("Have a nice day!")
        exit()
    elif choice == "1":  # Navigate to CRUD operations
        crud()
    elif choice == "2":  # Navigate to Top Ten companies menu
        topten()
    else:  # Invalid input handling
        print("Invalid option!")
