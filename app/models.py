from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# ORM mapping
class Agent(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Office(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)

class AgentOffice(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    agent_id = db.Column(db.Integer(), ForeignKey(Agent.id), index=True)
    office_id = db.Column(db.Integer(), ForeignKey(Office.id), index=True)

    agent = relationship('Agent', foreign_keys='AgentOffice.agent_id')
    office = relationship('Office', foreign_keys='AgentOffice.office_id')

class House(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    number_of_bedrooms = db.Column(db.Integer(), nullable=False)
    number_of_bathrooms = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=False, index=True)
    zip_code = db.Column(db.Integer(), nullable=False, index=True)
    listing_date = db.Column(db.DateTime(), nullable=False, index=True)
    seller_id = db.Column(db.Integer(), ForeignKey(User.id))
    agent_id = db.Column(db.Integer(), ForeignKey(Agent.id), index=True)
    sold = db.Column(db.Boolean(), nullable=False)

    seller = relationship('User', foreign_keys='House.seller_id')
    agent = relationship('Agent', foreign_keys='House.agent_id')

class Sale(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    buyer_id = db.Column(db.Integer(), ForeignKey(User.id))
    house_id = db.Column(db.Integer(), ForeignKey(House.id), index=True)
    price = db.Column(db.Float(), nullable=False, index=True)
    sale_date = db.Column(db.DateTime(), index=True)

    buyer = relationship('User', foreign_keys='Sale.buyer_id')
    house = relationship('House', foreign_keys='Sale.house_id')

class Commission(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    commission = db.Column(db.Float(), nullable=False)
    agent_id = db.Column(db.Integer(), ForeignKey(Agent.id), index=True)
    sale_id = db.Column(db.Integer(), ForeignKey(Sale.id), index=True)

    agent = relationship('Agent', foreign_keys='Commission.agent_id')
    sale = relationship('Sale', foreign_keys='Commission.sale_id')

class Summary(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    total_sales = db.Column(db.Float(), nullable=False)
    total_commissions = db.Column(db.Float(), nullable=False)
