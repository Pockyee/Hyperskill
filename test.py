import csv
import os
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError



menu = {
    "main": "MAIN MENU\n0 Exit\n1 CRUD operations\n2 Show top ten companies by criteria\n\nEnter an option:",
    "crud": "CRUD MENU\n0 Back\n1 Create a company\n2 Read a company\n3 Update a company\n4 Delete a company\n5 List all companies\n\nEnter an option:",
    "topten": "TOP TEN MENU\n0 Back\n1 List by ND/EBITDA\n2 List by ROE\n3 List by ROA\n\nEnter an option:",
}
Base = declarative_base()


class Companies(Base):
    __tablename__ = "companies"

    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)


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


def replace_empty_with_none(dict):
    for key, value in dict.items():
        if value == "":
            dict[key] = None
    return dict

def set_engine():
    global session
    engine = create_engine("sqlite:///investor.db", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

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


def create_a_company():
    try:
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
        session.commit
        print("Company created successfully!")
    except IntegrityError:
        session.rollback()

def read_company():
    x = input("Enter company name:\n")
    results = session.query(Companies).filter(Companies.name.like(f"%{x}%"))
    if results:
        i = 0
        for company in results:
            print(f"{i} {company.name}")
            i += 1
    else:
        print("Company not found!")
    j = int(input("Enter company number:\n"))
    return results[j]


def financial_data(ticker):
    finance = session.query(Financial).filter(Financial.ticker == ticker).first()
    pe_ratio = round(finance.market_price / finance.net_profit, 2) if finance.net_profit else None
    ps_ratio = round(finance.market_price / finance.sales, 2) if finance.sales else None
    pb_ratio = round(finance.market_price / finance.assets, 2) if finance.assets else None
    nd_ebitda = round(finance.net_debt / finance.ebitda, 2) if finance.ebitda else None
    roe = round(finance.net_profit / finance.equity, 2) if finance.equity else None
    roa = round(finance.net_profit / finance.assets, 2) if finance.assets else None
    la_ratio = round(finance.liabilities / finance.assets, 2) if finance.assets else None
    print(
        f"""P/E = {pe_ratio}\nP/S = {ps_ratio}\nP/B = {pb_ratio}\nND/EBITDA = {nd_ebitda}\nROE = {roe}\nROA = {roa}\nL/A = {la_ratio}\n""")


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
    finance.update({
        "ebitda": ebitda_,
        "sales": sales_,
        "net_profit": net_profit_,
        "market_price": market_price_,
        "net_debt": net_debt_,
        "assets": assets_,
        "equity": equity_,
        "cash_equivalents": cash_equivalents_,
        "liabilities": liabilities_
    })
    session.commit
    print("Company updated successfully!")


def delete_company(ticker):
    session.query(Companies).filter(Companies.ticker == ticker).delete()
    session.query(Financial).filter(Financial.ticker == ticker).delete()
    session.commit
    print("Company deleted successfully!")


def list_company():
    results = session.query(Companies)
    results.sort()
    for company in results:
        print(f"{company.ticker} {company.name}")


def crud():
    print(menu["crud"])
    choice = input()
    if choice == "0":
        pass
    elif choice == "1":
        create_a_company()
    elif choice == "2":
        x = read_company()
        print(x.name)
        financial_data(x.ticker)
    elif choice == "3":
        x = read_company()
        update_company(x.ticker)
    elif choice == "4":
        x = read_company()
        delete_company(x.ticker)
    elif choice == "5":
        list_company()
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


print("Welcome to the Investor Program!")
if os.path.exists("investor.db"):
    set_engine()
else:
    set_engine()
    create_db()
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
