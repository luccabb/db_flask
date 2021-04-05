from flask.cli import with_appcontext
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from .models import db, Agent, User, Office, AgentOffice, House, Sale, Commission
import datetime

# new application blueprint for auth related tasks
bp_seed = Blueprint('seed', __name__, cli_group='other')

def insert_db(table, columns, data):
    for r in range(len(data)):
        row = {}
        for c in range(len(columns)):
            row[columns[c]] = data[r][c]
        db_object = table(**row)
        db.session.add(db_object)
    
    db.session.commit()

def get_commission(price):
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

# adding seed command. This command seeds the database based on file seed.py
@bp_seed.cli.command('seed')
def seed_command():
    """Seed the database."""

    # populating agent model
    agent_columns = ['id', 'username', 'email', 'password']
    agent_data = [
        [1, 'agent_1', 'agent_1@gmail.com', '123'],
        [2, 'agent_2', 'agent_2@gmail.com', '1234'],
        [3, 'agent_3', 'agent_3@gmail.com', '12345'],
        [4, 'agent_4', 'agent_4@gmail.com', '123456'],
        [5, 'agent_5', 'agent_5@gmail.com', '123'],
        [6, 'agent_6', 'agent_6@gmail.com', '1234'],
        [7, 'agent_7', 'agent_7@gmail.com', '12345'],
        [8, 'agent_8', 'agent_8@gmail.com', '123456'],
    ]
    insert_db(Agent, agent_columns, agent_data)

    # populating user model // buyers and sellers are registered as users
    user_columns = ['id', 'username', 'email', 'password']
    user_data = [
        [1, 'buyer_seller_1', 'buyer_seller_1@gmail.com', '123'],
        [2, 'buyer_seller_2', 'buyer_seller_2@gmail.com', '1234'],
        [3, 'buyer_seller_3', 'buyer_seller_3@gmail.com', '12345'],
        [4, 'buyer_seller_4', 'buyer_seller_4@gmail.com', '123456'],
        [5, 'buyer_seller_5', 'buyer_seller_5@gmail.com', '123'],
        [6, 'buyer_seller_6', 'buyer_seller_6@gmail.com', '1234'],
        [7, 'buyer_seller_7', 'buyer_seller_7@gmail.com', '12345'],
        [8, 'buyer_seller_8', 'buyer_seller_8@gmail.com', '123456'],
    ]
    insert_db(User, user_columns, user_data)

    # populating office model // each office has their own row
    office_columns = ['id', 'name', 'email', 'city', 'state', 'country']
    office_data = [
        [1, 'office_1', 'office_1@gmail.com', 'city_1', 'state_1', 'country_1'],
        [2, 'office_2', 'office_2@gmail.com', 'city_2', 'state_2', 'country_2'],
        [3, 'office_3', 'office_3@gmail.com', 'city_3', 'state_3', 'country_3'],
        [4, 'office_4', 'office_4@gmail.com', 'city_4', 'state_4', 'country_4'],
    ]
    insert_db(Office, office_columns, office_data)

    # populating agentoffice model // each agent can be associated with a given office
    # they may be associated to multiple offices
    agent_office_columns = ['id', 'agent_id', 'office_id']
    agent_office_data = [
        # adding 2 agents to each office 
        [1, 1, 1],
        [2, 2, 1],
        [3, 3, 2],
        [4, 4, 2],
        [5, 5, 3],
        [6, 6, 3],
        [7, 7, 4],
        [8, 8, 4],
        # adding a few agents to multiple offices
        [9 , 1, 2],
        [10, 3, 3],
        [11, 5, 4],
        [12, 7, 1],
        # agents 1 2 7 -> office 1
        # agents 3 4 1 -> office 2
        # agents 5 6 3 -> office 3
        # agents 7 8 4 -> office 4
    ]
    insert_db(AgentOffice, agent_office_columns, agent_office_data)

    # populating house model
    house_columns = ['id', 'number_of_bedrooms', 'number_of_bathrooms', 'price', 'zip_code', 'listing_date', 'seller_id', 'agent_id', 'sold']
    house_data = [
        [ 1, 3, 4,   90000.00, 94101, datetime.datetime(2014,  7, 12), 2, 1, True],
        [ 2, 2, 2,  170300.00, 94102, datetime.datetime(2012,  3, 15), 1, 4, True],
        [ 3, 1, 3,  345000.00, 94103, datetime.datetime(2017,  2,  5), 2, 6, True],
        [ 4, 2, 4,  999999.99, 94104, datetime.datetime(2015, 12,  2), 3, 8, True],
        [ 5, 2, 4, 1400379.50, 94105, datetime.datetime(2013, 10, 26), 4, 7, True],
        [ 6, 1, 2,   70000.00, 94100, datetime.datetime(2007,  7, 12), 2, 1, True],
        [ 7, 1, 1,  175300.00, 94102, datetime.datetime(2008,  3, 15), 1, 1, True],
        [ 8, 1, 2,  232000.00, 94101, datetime.datetime(2004,  2,  5), 2, 1, True],
        [ 9, 2, 2,  940000.99, 94101, datetime.datetime(2005, 12,  2), 3, 4, True],
        [10, 2, 2, 2700000.50, 94102, datetime.datetime(2009, 10, 26), 4, 4, True],
        [11, 3, 4,   45000.00, 94103, datetime.datetime(2000,  7, 12), 2, 6, True],
        [12, 2, 2,  130500.00, 94103, datetime.datetime(2003,  3, 15), 1, 6, True],
        [13, 1, 1,  505000.00, 94104, datetime.datetime(2002,  2,  5), 2, 8, True],
        [14, 2, 1,  750000.99, 94104, datetime.datetime(2001, 12,  2), 3, 8, True],
        [15, 3, 4, 1700300.50, 94104, datetime.datetime(2004, 10, 26), 4, 7, True],
        [16, 4, 3,  125000.00, 94104, datetime.datetime(2006,  3, 15), 1, 7, True],
        [17, 4, 3,  440000.00, 94104, datetime.datetime(2007,  2,  5), 2, 5, True],
        [18, 3, 2,  680000.99, 94104, datetime.datetime(2009, 12,  2), 3, 3, True],
        [19, 1, 2, 1560000.50, 94102, datetime.datetime(2005, 10, 26), 4, 5, True],
    ]
    insert_db(House, house_columns, house_data)

    # populating sale model // each sale has a row for it
    sale_columns = ['id', 'buyer_id', 'house_id', 'price', 'sale_date']
    sale_data = [
        [ 1, 5,  1,   90000.00, datetime.datetime(2019,  3, 12)],
        [ 2, 6,  2,  170300.00, datetime.datetime(2014,  4, 15)],
        [ 3, 6,  3,  345000.00, datetime.datetime(2019,  3,  5)],
        [ 4, 8,  4,  999999.99, datetime.datetime(2019,  3,  2)],
        [ 5, 7,  5, 1400379.50, datetime.datetime(2019,  3, 26)],
        [ 6, 5,  6,   70000.00, datetime.datetime(2019,  3, 12)],
        [ 7, 5,  7,  175300.00, datetime.datetime(2019,  3,  6)],
        [ 8, 6,  8,  232000.00, datetime.datetime(2019,  3,  2)],
        [ 9, 7,  9,  940000.99, datetime.datetime(2019,  3,  1)],
        [10, 7, 10, 2700000.50, datetime.datetime(2019,  3, 25)],
        [11, 7, 11,   45000.00, datetime.datetime(2019,  3, 23)],
        [12, 8, 12,  130500.00, datetime.datetime(2019,  3, 13)],
        [13, 8, 13,  505000.00, datetime.datetime(2019,  3,  7)],
        [14, 8, 14,  750000.99, datetime.datetime(2019,  3,  7)],
        [15, 6, 15, 1700300.50, datetime.datetime(2019,  3, 10)],
        [16, 7, 16,  125000.00, datetime.datetime(2019,  3, 11)],
        [17, 8, 17,  440000.00, datetime.datetime(2019,  3, 16)],
        [18, 5, 18,  680000.99, datetime.datetime(2019,  3, 20)],
        [19, 5, 19, 1560000.50, datetime.datetime(2019,  3, 22)],
    ]
    insert_db(Sale, sale_columns, sale_data)

    # populating commissions model // each commission has a row for it linking it to a specific agent
    commission_columns = ['id', 'commission', 'sale_id', 'agent_id']
    agents = [1, 4, 6, 7, 8, 1, 1, 1, 4, 4, 6, 6, 8, 8, 7, 7, 5, 3, 5]
    lambda_filter = lambda x: [x[0], get_commission(x[3]), x[0]]
    commission_data = list(map(lambda_filter, sale_data))
    i=0
    for commission in commission_data:
        commission.append(agents[i])
        i+=1

    insert_db(Commission, commission_columns, commission_data)



