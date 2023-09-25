from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,send_from_directory
from app import app, db
from textblob import TextBlob
from db import Comment , User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Create a new user and add it to the database
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

"""
This function to validate the analyes from the comment 
"""
def analyze_comment(comment):
    analysis = TextBlob(comment)
    analysis = analysis.correct()
    sentiment_score = analysis.sentiment.polarity
    if sentiment_score > 0:
        sentiment_label = 'Positive'
    elif sentiment_score < 0:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'
    return sentiment_score, sentiment_label , str(analysis)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST' and current_user.role != 'admin':
        user_comment = request.form['user_comment']
        sentiment, sentiment_label ,user_input= analyze_comment(user_comment)

        # Create a new Comment object and add it to the database
        new_comment = Comment(user=current_user.username, text=user_input, sentiment=sentiment, sentiment_label=sentiment_label)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('home'))  # Redirect to clear the form

    # Retrieve all comments from the database
    if current_user.role == 'admin':
        comments = Comment.query.all()
        return render_template('index.html', comments=comments)
    else:
        comments = Comment.query.all()
        return render_template('user.html', comments=comments)
    
    

@app.route('/get_counts', methods=['GET'])
@login_required
def get_counts():
    # Calculate the counts of positive, negative, and neutral comments
    start_date =request.args.get('start_date')
    end_date = request.args.get('end_date')
    positive = 0
    negative = 0
    neutral = 0
    if start_date != "undefined" and end_date != "undefined":
       comments = Comment.query.filter(Comment.date.between(start_date, end_date)).with_entities(Comment.sentiment_label).all()
       if len(comments) != 0:
         for comment in comments:
            if comment[0] == "Positive":
                positive += 1
            elif comment[0] == "Negative":
                negative += 1
            else:
                neutral += 1
       else:
          print("There are no comments")
        # Return the counts as JSON
       return jsonify(positive=positive, negative=negative, neutral=neutral,total_comment=len(comments))
    else:
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
            print("There are no comments")
        # Return the counts as JSON
        return jsonify(positive=positive, negative=negative, neutral=neutral,total_comment=len(comments))

    
@app.route('/get_comments', methods=['GET', 'POST'])
@login_required
def get_comments():
    # Calculate the counts of positive, negative, and neutral comments
    print(request.args.get('start_date'))
    start_date =request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date != "undefined" and end_date != "undefined":
        print("inside if") 
        comments = Comment.query.filter(Comment.date.between(start_date, end_date)).all()
        print(len(comments))
        total_comment=[]
        for i in range(len(comments)):
            comment={}
            comment["user"]=comments[i].user
            comment["comment"]=comments[i].text
            comment["sentiment_label"]=comments[i].sentiment_label
            total_comment.append(comment)
        return total_comment  
    else:
        comments = Comment.query.all()
        total_comment=[]
        my_tuple=[]
        for i in range(len(comments)):
            comment={}
            comment["user"]=comments[i].user
            comment["comment"]=comments[i].text
            comment["sentiment_label"]=comments[i].sentiment_label
            total_comment.append(comment)
        # Return the counts as JSON
        return total_comment

@app.route('/positive', methods=['GET'])
@login_required
def get_positive():
    comments = Comment.query.all()
    total_comment=[]
    my_tuple=[]
    for i in range(len(comments)):
        if comments[i].sentiment_label == "Positive":
            comment={}
            comment["user"]=comments[i].user
            comment["comment"]=comments[i].text
            comment["sentiment_label"]=comments[i].sentiment_label
            total_comment.append(comment)
    return render_template('positive.html', comments=total_comment)

@app.route('/negative', methods=['GET'])
@login_required
def get_negative():
    comments = Comment.query.all()
    total_comment=[]
    my_tuple=[]
    for i in range(len(comments)):
        if comments[i].sentiment_label == "Negative":
            comment={}
            comment["user"]=comments[i].user
            comment["comment"]=comments[i].text
            comment["sentiment_label"]=comments[i].sentiment_label
            total_comment.append(comment)
    return render_template('negative.html', comments=total_comment)


@app.route('/neutral', methods=['GET'])
@login_required
def get_neutral():
    comments = Comment.query.all()
    total_comment=[]
    my_tuple=[]
    for i in range(len(comments)):
        if comments[i].sentiment_label == "Neutral":
            comment={}
            comment["user"]=comments[i].user
            comment["comment"]=comments[i].text
            comment["sentiment_label"]=comments[i].sentiment_label
            total_comment.append(comment)
    return render_template('neutral.html', comments=total_comment)

