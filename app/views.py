from flask import render_template, redirect, url_for

from app import app, nav, db
from app.models import BlogPost
from app.temp_models import InterestedClient
from app.public_forms import RegisterClientInterest
from app.extensions.email import send_email

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterClientInterest()
    if form.validate_on_submit():
        # TODO: add information to database
        # TODO: rate limiting
        client = InterestedClient(name=form.name.data, email=form.email.data, \
            phone=None, organisation=form.organisation.data, \
            project_description = form.project_description.data,
            estimated_cost = None)
        db.session.add(client)
        db.session.commit()

        # Send confirmation email
        html = render_template('email/project_idea_registered.html', \
            project=client)
        subject = 'Dreaming Spires project confirmation'
        send_email(client.email, subject, html)

        return redirect(url_for('auth.thanks_for_registering_client'))
    return render_template('public/index.html', is_fullpage=True, form=form)

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

@app.route('/portfolio')
def portfolio():
    # Get blog posts from db
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.date_created.desc()).all()
    return render_template('public/portfolio.html', posts=posts)

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('public/privacy_policy.html')
