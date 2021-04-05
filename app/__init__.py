from flask import Flask
from .models import db, User
from .seed import bp_seed
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from .routes import routes

app = Flask(__name__)

app.register_blueprint(bp_seed)
app.register_blueprint(routes)

# app.config.from_object(config[os.getenv('FLASK_ENV')])
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

migrate = Migrate()

# connecting DB, flask-migrate
db.init_app(app)
migrate.init_app(app, db, render_as_batch=True)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()