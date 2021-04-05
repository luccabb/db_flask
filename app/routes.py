from flask.cli import with_appcontext
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from .models import db, Agent, User, Office, AgentOffice, House, Sale, Commission
from datetime import datetime
from sqlalchemy import extract, func, text, cast, Date
import json

# new application blueprint for auth related tasks
routes = Blueprint('routes', __name__)

def get_commission(price):
    """ Calculating agent's commission based on price"""
    if price < 100000:
        return round(price*0.1,   2)
    elif price < 200000:
        return round(price*0.075, 2)
    elif price < 500000:
        return round(price*0.06,  2)
    elif price < 1000000:
        return round(price*0.05,  2)
    else:
        return round(price*0.04,  2)

# 1. Find the top 5 offices with the most sales for that month.
@routes.route("/office_sales", methods=['GET'])
def office_sales():
    try:
        # data = request.get_json()
        # month = data['month']
        # year = data['year']
        month = 3
        year = 2019

        offices = db.session.query(Office.id, Office.name, func.count(Commission.agent_id)).filter(
            Office.id == AgentOffice.office_id
        ).filter(
            AgentOffice.agent_id == Commission.agent_id
        ).filter(
            Commission.sale_id == Sale.id
        ).filter(
            extract('month', Sale.sale_date)==month, 
            extract( 'year', Sale.sale_date)==year
        ).group_by(Office.id).order_by(func.count(Commission.agent_id).desc()).limit(5).all()

        get_data = lambda x: {'office_id': x[0], 'office_name': x[1], 'sales': x[2]}
        offices = list(map(get_data, offices))

        return {
            'statusCode': 200,
            'body': json.dumps(offices)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# 2. Find the top 5 estate agents who have sold the most (include their contact details 
# and their sales details so that it is easy contact them and congratulate them).
@routes.route("/agents_sales", methods=['GET'])
def agents_sales():
    try:
        month = 3
        year = 2019

        agents = db.session.query(
            Agent.id, 
            Agent.username, 
            Agent.email, 
            func.count(Commission.agent_id)
        ).join(Agent).join(Sale).filter(
            extract('month', Sale.sale_date)==month, 
            extract( 'year', Sale.sale_date)==year
        ).group_by(Commission.agent_id).order_by(func.count(Commission.agent_id).desc()).limit(5).all()

        get_data = lambda x: {'agent_id': x[0], 'agent_username': x[1], 'agent_email': x[2], 'sales': x[3]}
        agents = list(map(get_data, agents))

        return {
            'statusCode': 200,
            'body': json.dumps(agents)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# route for creating new sale
# 3. Calculate the commission that each estate agent must receive and store the results in a separate table
@routes.route("/create_sale", methods=['POST'])
def create_sale():
    """ 
        This API call allows anyone to create a sale, it needs: buyer_id, house_id, agent_id, and price
        It stores commission's on a separate table.
    """
    try:
        data = request.get_json()

        buyer = User.query.filter_by(id=data['buyer_id']).first()
        house = House.query.filter_by(id=data['house_id']).first()
        agent = Agent.query.filter_by(id=data['agent_id']).first()
        summary = Summary.query.filter_by(id=1).first()

        if not house or not buyer or not agent:
            # returning generic error so we don't allow buyer/agent enumeration
            return {'error': "Can't create sale"}, 500
        
        agent_commission = get_commission(data['price'])
        
        # starting transaction
        sale = Sale(
            house=house,
            buyer=buyer,
            price=data['price'],
            commission=commission,
            sale_date=datetime.strptime(data['sale_date'], "%d/%m/%Y")
        )
        commission = Commission(
            commission=agent_commission,
            agent=agent,
            sale=sale
        )
        # changing original listing status
        house.sold = True

        # updating summary table
        summary.total_sales += data['price']
        summary.total_commissions += agent_commission

        # adding sale and commission object
        db.session.add(sale)
        db.session.add(commission)
        # committing changes
        db.session.commit()
        return {
            'statusCode': 200,
            'body': 'Sale created!'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# 4. For all houses that were sold that month, calculate the average number 
# of days that the house was on the market.
@routes.route("/average_days", methods=['GET'])
def average_days():
    try:
        month = 3
        year = 2019

        sales = db.session.query(
            Sale.house_id, Sale.sale_date, House.listing_date).join(House).filter(
            extract('month', Sale.sale_date)==month, 
            extract( 'year', Sale.sale_date)==year
        ).all()

        day_diff = lambda x: (x[1] - x[2]).days
        average_day = sum(list(map(day_diff, sales)))/len(sales)

        return {
            'statusCode': 200,
            'body': average_day
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# 5. For all houses that were sold that month, calculate the average selling price
@routes.route("/average_price", methods=['GET'])
def average_price():
    try:
        month = 3
        year = 2019

        sales = db.session.query(
            Sale.house_id, House.price).join(House).filter(
            extract('month', Sale.sale_date)==month, 
            extract( 'year', Sale.sale_date)==year
        ).all()

        get_price = lambda x: x[1]
        average_price = sum(list(map(get_price, sales)))/len(sales)

        return {
            'statusCode': 200,
            'body': average_price
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# 6. Find the zip codes with the top 5 average sales prices
@routes.route("/average_price_zipcode", methods=['GET'])
def average_price_zipcode():
    try:
        month = 3
        year = 2019

        sales = db.session.query(
            House.zip_code, 
            func.avg(House.price)
        ).join(Sale).filter(
            extract('month', Sale.sale_date)==month,
            extract( 'year', Sale.sale_date)==year,
            House.sold==True
        ).group_by(House.zip_code).order_by(func.avg(House.price).desc()).limit(5).all()

        get_data = lambda x: {'zipcode': x[0], 'average_price': x[1]}
        sales = list(map(get_data, sales))

        return {
            'statusCode': 200,
            'body': json.dumps(sales)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }