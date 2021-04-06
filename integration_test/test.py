import requests, json
import os
import tempfile
import unittest
import pymysql
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import extract, func, text, cast, Date

connStr = "mysql://root:test_password@0.0.0.0:3306/main"
dbengine = create_engine(connStr)

Base = declarative_base()
metadata = MetaData()

Session = sessionmaker(bind=dbengine)
session = Session()

# Instantiating tables
Agent = Table("agent", metadata, autoload=True, autoload_with=dbengine)
User = Table("user", metadata, autoload=True, autoload_with=dbengine)
Office = Table("office", metadata, autoload=True, autoload_with=dbengine)
AgentOffice = Table("agent_office", metadata, autoload=True, autoload_with=dbengine)
House = Table("house", metadata, autoload=True, autoload_with=dbengine)
Sale = Table("sale", metadata, autoload=True, autoload_with=dbengine)
Commission = Table("commission", metadata, autoload=True, autoload_with=dbengine)

URL = "http://0.0.0.0:5000"

class TestCreateSale(unittest.TestCase):
    def test_office_route(self):
        req = requests.get(URL + "/office_sales", json={
            "month": 3,
            "year": 2019
        })
        # asserting that our request went through
        assert(req.status_code == 200)
    
    def test_agent_route(self):
        req = requests.get(URL + "/agents_sales", json={
            "month": 3,
            "year": 2019
        })
        # asserting that our request went through
        assert(req.status_code == 200)
    
    def test_create_route(self):
        req = requests.post(URL + "/create_sale", json={
            "buyer_id": 4,
            "house_id": 20,
            "agent_id": 3,
            "price": 1230000.00,
            "sale_date": "02/04/2021"
        })
        # asserting that our request went through
        assert(req.status_code == 200)

        sale = session.query(Sale).filter_by(
            buyer_id=4,
            house_id=20,
            price=1230000.00
        ).first()
        # checking whether or not our sale was created
        assert(sale is not None)

        commission = session.query(Commission).filter_by(
            agent_id=3,
            sale_id=sale.id
        ).first()

        # checking whether or not commission was created
        assert(commission is not None)
    
    def test_avgdays_route(self):
        req = requests.get(URL + "/average_days", json={
            "month": 3,
            "year": 2019
        })
        # asserting that our request went through
        assert(req.status_code == 200)
    
    def test_avgprice_route(self):
        req = requests.get(URL + "/average_price", json={
            "month": 3,
            "year": 2019
        })
        # asserting that our request went through
        assert(req.status_code == 200)

    def test_avgpricezipcode_route(self):
        req = requests.get(URL + "/average_price_zipcode", json={
            "month": 3,
            "year": 2019
        })
        # asserting that our request went through
        assert(req.status_code == 200)


if __name__ == '__main__':
    unittest.main()