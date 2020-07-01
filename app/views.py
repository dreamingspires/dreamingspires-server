from flask import render_template

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/developer')
def developer():
    return render_template('developer.html')
