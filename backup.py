from flask import Flask, render_template, request, redirect, url_for , jsonify
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'  # SQLite database
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    sentiment = db.Column(db.Float)
    sentiment_label = db.Column(db.String(10))

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_comment = request.form['user_comment']
        sentiment, sentiment_label = analyze_comment(user_comment)

        # Create a new Comment object and add it to the database
        new_comment = Comment(text=user_comment, sentiment=sentiment, sentiment_label=sentiment_label)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('index'))  # Redirect to clear the form

    # Retrieve all comments from the database
    comments = Comment.query.all()
    return render_template('index.html', comments=comments)

def analyze_comment(comment):
    analysis = TextBlob(comment)
    sentiment_score = analysis.sentiment.polarity
    if sentiment_score > 0:
        sentiment_label = 'Positive'
    elif sentiment_score < 0:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'
    return sentiment_score, sentiment_label

@app.route('/get_counts', methods=['GET'])
def get_counts():
    # Calculate the counts of positive, negative, and neutral comments
    positive = 0
    negative = 0
    neutral = 0
    comments = Comment.query.with_entities(Comment.sentiment_label).all()
    if len(comments) != 0:
        for comment in comments:
            if comment[0] == "Positive":
                positive += 1
            elif comment[0] == "Negative":
                negative += 1
            else:
                neutral += 1
    else:
        print("There is no comments")
    # Calculate the counts based on your Comment model or database queries

    # Return the counts as JSON
    return jsonify(positive=positive, negative=negative, neutral=neutral)

if __name__ == '__main__':
    app.run(debug=True)
