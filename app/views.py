from flask import render_template, redirect, url_for

from app import app, nav, db
from app.models import BlogPost
from app.temp_models import InterestedClient
from app.public_forms import RegisterClientInterest
from app.extensions.email import send_email
from app.mod_auth.forms import LoginForm
def client_signup(template_path, *args, **kwargs):
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
    return render_template(template_path, *args, form=form, **kwargs)


@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    return client_signup('public/index.html', login_form=login_form, is_fullpage=True)

@app.route('/our_services', methods=['GET', 'POST'])
def our_services():
    login_form = LoginForm()
    return client_signup('public/our_services.html', login_form=login_form, is_fullpage=False)

@app.route('/about')
def about():
    return render_template('public/about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    login_form = LoginForm()
    return render_template('public/contact.html', login_form=login_form)

@app.route('/client')
def client():
    return render_template('public/client.html',  posts=posts)

@app.route('/client_faq')
def client_faq():
    return render_template('public/client_faq.html')

@app.route('/developer')
def developer():
    return render_template('public/developer.html')

@app.route('/register_developer', methods=['POST', 'GET'])
def register_developer():
    login_form = LoginForm()
    return render_template('public/register_developer.html', login_form=login_form)

@app.route('/developer_faq')
def developer_faq():
    return render_template('public/developer_faq.html')

@app.route('/login2')
def login2():
    return render_template('login2.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    return render_template('login.html', login_form=login_form)

@app.route('/portfolio')
def portfolio():
    login_form = LoginForm()
    # Get blog posts from db
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.date_created.desc()).all()
    return render_template('public/portfolio.html', login_form=login_form, posts=posts)

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('public/privacy_policy.html')

