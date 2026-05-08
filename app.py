from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'spk-ahp-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from routes import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    