from flask import render_template

from app import app, nav
from app.models import BlogPost

@app.route('/')
def index():
    return render_template('public/index.html', is_fullpage=True)

@app.route('/about')
def about():
    return render_template('public/about.html')

@app.route('/contact')
def contact():
    return render_template('public/contact.html')

@app.route('/client')
def client():
    return render_template('public/client.html', posts=posts)

@app.route('/client_faq')
def client_faq():
    return render_template('public/client_faq.html')

@app.route('/developer')
def developer():
    return render_template('public/developer.html')

@app.route('/developer_faq')
def developer_faq():
    return render_template('public/developer_faq.html')

@app.route('/login2')
def login2():
    return render_template('login2.html')

@app.route('/blog')
def blog():
    # Get blog posts from db
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.date_created.desc()).all()
    return render_template('public/blog.html', posts=posts)

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('public/privacy_policy.html')
