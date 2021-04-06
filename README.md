# Sample DB application

This Backend was deployed on AWS, using:

- RDS for Database.
- API Gateway to allow communication via API with AWS resources.
- AWS Lambda to run serverless code that queries our RDS instance.

## Database Structure

Base tables: Agent, User, Office, AgentOffice, House, Sale, Commission, Summary.

Agent: Holds information of real estate agents.

User: Holds information of our users, they are the ones who buy and sell properties.

Office: Holds information of a given office.

AgentOffice: Holds information on what agents works for what office. This normalized table allow for agents to work for multiple offices.

House: Holds information of a given house that is either for sale or was already sold.

Sale: Holds information on what house was sold to what buyer. 'price' is repeated/denormalized here in case there was any change(discount) on the 'price' listed on the previous table (House).

Commission: Holds commission information for a given sale and for a given agent. Having this data normalized allow us to have multiple agents helping in a single house sale.

Summary: Holds information on total sales and total commissions, updated with every new sale. Allow quick lookup on those values. I.E: if this information is listed on the website's homepage we can get them from this table, to ensure that the data is up to date.

OBS: There are a few indexes on those tables that might help in the future to make queries faster, such as: agent_id on House table, price on House and Sale tables... They should be created/removed based on their tradeoffs (faster query vs additional storage) and how the scaling of the system is going.

## API

Main endpoint: `https://19xkrhb7j6.execute-api.us-east-1.amazonaws.com/prod`

### Resources:

1. Find the top 5 offices with the most sales for that month.
- `/office_sales`: accepts GET requests. You can use the following payload as a JSON to specify month and year:
```
{
    "month": 3,
	"year": 2019
}
```

2. Find the top 5 estate agents who have sold the most (include their contact details and their sales details so that it is easy contact them and congratulate them).
- `/create_sale`: accepts GET requests. You can use the following payload as a JSON to specify month and year:
```
{
    "month": 3,
	"year": 2019
}
```

3. Calculate the commission that each estate agent must receive and store the results in a separate table
- `/create_sale`: accepts POST requests. You can use the following payload as a JSON to specify data:
```
{
    "buyer_id": 4,
    "house_id": 20,
    "agent_id": 3,
    "price": 1230000.00,
    "sale_date": "02/04/2021"
}
```

4. For all houses that were sold that month, calculate the average number of days that the house was on the market.
- `/average_days`: accepts GET requests. You can use the following payload as a JSON to specify month and year:
```
{
    "month": 3,
	"year": 2019
}
```

5. For all houses that were sold that month, calculate the average selling price
- `/average_price`: accepts GET requests. You can use the following payload as a JSON to specify month and year:
```
{
    "month": 3,
	"year": 2019
}
```

6. Find the zip codes with the top 5 average sales prices
- `/average_price_zipcode`: accepts GET requests. You can use the following payload as a JSON to specify month and year:
```
{
    "month": 3,
	"year": 2019
}
```

All endpoints have the same respose structure as a JSON:
```
{
    'statusCode': Integer,
    'body': String
}
```

# Running project locally

## Virtual Environment
Creation of virtualenv:

    $ virtualenv -p python3 venv

If the above code does not work, you could also do

    $ python3 -m venv venv

To activate the virtualenv:

    $ source venv/bin/activate

Or, if you are **using Windows** - [reference source:](https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate)

    $ venv\Scripts\activate

To deactivate the virtualenv (after you finished working):

    $ deactivate

Install dependencies in virtual environment:

    $ pip3 install -r requirements.txt

## Environment Variables

`.env.example` is a file containing all the environment variables that you need to define in a `.env` file for this project to run.

## Integration tests

The environment has 2 containers: one for the web server and one for the database. Those tests exist to check whether the backend is doing the right thing.

    $ docker-compose up
    $ docker exec db_assignment_web_1 flask other seed # seeding the db
    $ python -m unittest integration_test/test.py # runnning tests

If all tests passed

    $ docker-compose down

Docker mysql DB URL when running locally: `mysql://root:test_password@host.docker.internal:3306/main`. This should be updated on .env to ensure that it points to our Docker Database.

## Run Application Locally

Start the server on a mac locally by running:

    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ flask run

## Seeding Database

Th following command will run the script on seed.py that populates the database with data:

    $ flask other seed

After seeding the database you can make the requests to the endpoints that are specified above (with the same payload), and you will receive the results based on the seed data.
