from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__ ,static_url_path='/static', static_folder='static')
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

from route import *

if __name__ == '__main__':
    app.run(debug=True)
