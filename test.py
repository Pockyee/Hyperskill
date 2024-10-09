import csv
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

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


engine = create_engine("sqlite:///investor.db", echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

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

session.close
print("Database created successfully!")
