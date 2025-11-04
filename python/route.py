from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,send_from_directory
from app import app, db
from textblob import TextBlob
from db import Comment , User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import io
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from collections import Counter
import time
import logging
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
    
    # Wider neutral threshold
    if sentiment_score > 0.3:
        sentiment_label = 'Positive'
    elif sentiment_score < -0.3:
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

    # Retrieve comments based on user role
    if current_user.role == 'admin':
        comments = Comment.query.all()
        return render_template('index.html', comments=comments)
    else:
        comments = Comment.query.all()
        return render_template('user.html', comments=comments)
    
    

@app.route('/get_counts', methods=['GET'])
@login_required
def get_counts():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date and end_date:
        comments = Comment.query.filter(Comment.date.between(start_date, end_date)).with_entities(Comment.sentiment_label).all()
    else:
        comments = Comment.query.with_entities(Comment.sentiment_label).all()
    
    positive = sum(1 for c in comments if c[0] == "Positive")
    negative = sum(1 for c in comments if c[0] == "Negative")
    neutral = sum(1 for c in comments if c[0] == "Neutral")
    
    return jsonify(positive=positive, negative=negative, neutral=neutral, total_comment=len(comments))

    
@app.route('/get_comments', methods=['GET'])
@login_required
def get_comments():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date and end_date:
        comments = Comment.query.filter(Comment.date.between(start_date, end_date)).all()
    else:
        comments = Comment.query.all()
    
    return [{
        "user": c.user,
        "comment": c.text,
        "sentiment_label": c.sentiment_label
    } for c in comments]

@app.route('/positive', methods=['GET'])
@login_required
def get_positive():
    comments = Comment.query.filter_by(sentiment_label='Positive').all()
    return render_template('sentiment_view.html', comments=comments, sentiment_type='positive')

@app.route('/negative', methods=['GET'])
@login_required
def get_negative():
    comments = Comment.query.filter_by(sentiment_label='Negative').all()
    return render_template('sentiment_view.html', comments=comments, sentiment_type='negative')

@app.route('/neutral', methods=['GET'])
@login_required
def get_neutral():
    comments = Comment.query.filter_by(sentiment_label='Neutral').all()
    return render_template('sentiment_view.html', comments=comments, sentiment_type='neutral')

@app.route('/csv_pie_chart', methods=['GET'])
@login_required
def csv_pie_chart():
    start_time = time.time()
    app.logger.info(f"CSV pie chart request received from user: {current_user.username}")
    
    try:
        csv_path = os.path.join(os.path.dirname(__file__), 'testdata.csv')
        df = pd.read_csv(csv_path)
        
        predictions = []
        for _, row in df.iterrows():
            _, predicted_label, _ = analyze_comment(str(row['A']))
            predictions.append(predicted_label)
        
        counts = Counter(predictions)
        labels = list(counts.keys())
        sizes = list(counts.values())
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('Sentiment Analysis Predictions')
        
        chart_path = os.path.join(os.path.dirname(__file__), 'static', 'csv_pie_chart.png')
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.savefig(chart_path)
        plt.close()
        
        generation_time = round((time.time() - start_time) * 1000, 2)
        app.logger.info(f"CSV pie chart generated in {generation_time}ms for user: {current_user.username}")
        return send_from_directory('static', 'csv_pie_chart.png')
    
    except Exception as e:
        app.logger.error(f"CSV pie chart error for user {current_user.username}: {str(e)}")
        return jsonify({'error': f'Error generating chart: {str(e)}'}), 500

@app.route('/comparison_chart', methods=['GET'])
@login_required
def comparison_chart():
    start_time = time.time()
    app.logger.info(f"Comparison chart request received from user: {current_user.username}")
    
    try:
        csv_path = os.path.join(os.path.dirname(__file__), 'testdata.csv')
        df = pd.read_csv(csv_path)
        
        if 'B' not in df.columns:
            return jsonify({'error': 'Column B (actual values) not found'}), 400
        
        actual = []
        predicted = []
        
        for _, row in df.iterrows():
            _, predicted_label, _ = analyze_comment(str(row['A']))
            actual.append(str(row['B']))
            predicted.append(predicted_label)
        
        actual_counts = Counter(actual)
        predicted_counts = Counter(predicted)
        
        labels = ['Positive', 'Negative', 'Neutral']
        actual_values = [actual_counts.get(label, 0) for label in labels]
        predicted_values = [predicted_counts.get(label, 0) for label in labels]
        
        x = range(len(labels))
        width = 0.35
        
        plt.figure(figsize=(10, 6))
        plt.bar([i - width/2 for i in x], actual_values, width, label='Actual', color='#ff9999')
        plt.bar([i + width/2 for i in x], predicted_values, width, label='Predicted', color='#66b3ff')
        
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.title('Actual vs Predicted Sentiment Analysis')
        plt.xticks(x, labels)
        plt.legend()
        
        chart_path = os.path.join(os.path.dirname(__file__), 'static', 'comparison_chart.png')
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.savefig(chart_path)
        plt.close()
        
        generation_time = round((time.time() - start_time) * 1000, 2)
        app.logger.info(f"Comparison chart generated in {generation_time}ms for user: {current_user.username}")
        return send_from_directory('static', 'comparison_chart.png')
    
    except Exception as e:
        app.logger.error(f"Comparison chart error for user {current_user.username}: {str(e)}")
        return jsonify({'error': f'Error generating comparison chart: {str(e)}'}), 500

@app.route('/model_accuracy', methods=['GET'])
@login_required
def model_accuracy():
    start_time = time.time()
    app.logger.info(f"Model accuracy request received from user: {current_user.username}")
    
    try:
        csv_path = os.path.join(os.path.dirname(__file__), 'testdata.csv')
        df = pd.read_csv(csv_path)
        
        if 'B' not in df.columns:
            return jsonify({'error': 'Column B (actual values) not found'}), 400
        
        actual = []
        predicted = []
        correct_predictions = 0
        
        for _, row in df.iterrows():
            _, predicted_label, _ = analyze_comment(str(row['A']))
            actual_label = str(row['B'])
            
            actual.append(actual_label)
            predicted.append(predicted_label)
            
            if actual_label == predicted_label:
                correct_predictions += 1
        
        total_samples = len(actual)
        overall_accuracy = (correct_predictions / total_samples) * 100
        
        # Count actual labels
        actual_counts = Counter(actual)
        
        # Calculate per-label accuracy
        label_accuracy = {}
        for label in ['Positive', 'Negative', 'Neutral']:
            label_correct = sum(1 for a, p in zip(actual, predicted) if a == label and a == p)
            label_total = actual_counts.get(label, 0)
            label_accuracy[label] = {
                'actual_count': label_total,
                'correct_predictions': label_correct,
                'accuracy_percentage': (label_correct / label_total * 100) if label_total > 0 else 0
            }
        
        prediction_time = round((time.time() - start_time) * 1000, 2)
        app.logger.info(f"Model accuracy calculated in {prediction_time}ms for user: {current_user.username} - Overall: {round(overall_accuracy, 2)}%")
        
        return jsonify({
            'total_samples': total_samples,
            'overall_accuracy': round(overall_accuracy, 2),
            'correct_predictions': correct_predictions,
            'incorrect_predictions': total_samples - correct_predictions,
            'label_performance': label_accuracy,
            'prediction_time_ms': prediction_time
        })
    
    except Exception as e:
        app.logger.error(f"Model accuracy error for user {current_user.username}: {str(e)}")
        return jsonify({'error': f'Error calculating accuracy: {str(e)}'}), 500

