from flask import render_template

from app import app, nav

@app.route('/')
def index():
    return render_template('public/index.html')

@app.route('/client')
def client():
    return render_template('public/client.html')

@app.route('/developer')
def developer():
    return render_template('public/developer.html')

@app.route('/login2')
def login2():
    return render_template('login2.html')

@app.route('/projects')
def projects():
    return render_template('projects/projects.html')
