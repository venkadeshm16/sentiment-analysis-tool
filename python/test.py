from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

app = Flask(__name__)
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    sentiment = db.Column(db.Float)
    sentiment_label = db.Column(db.String(10))
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/filter', methods=['GET', 'POST'])
def filter_data():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        # Perform a database query based on the start_date and end_date
        results = Comment.query.filter(Comment.date.between(start_date, end_date)).all()
        
        # You can render a template to display the results
        return render_template('results.html', results=results)
    
    return render_template('filter.html')
if __name__ == '__main__':
    app.run(debug=True)
