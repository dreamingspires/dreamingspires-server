from flask import render_template, redirect, url_for

from app import app, nav, db
from app.models import BlogPost
from app.temp_models import InterestedClient, InterestedDeveloper
from app.public_forms import RegisterClientInterest
from app.extensions.email import send_email
from app.mod_auth.forms import LoginForm, RegisterDeveloperForm

def client_signup(template_path, *args, **kwargs):
    form = RegisterClientInterest()
    if form.validate_on_submit():
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

def developer_signup(template_path, *args, **kwargs):
    form = RegisterDeveloperForm()
    if form.validate_on_submit():
        # TODO: rate limiting
        developer = InterestedDeveloper(name=form.user_name.data, email=form.email.data, \
            phone=form.phone_number.data, speciality=form.speciality.data)
        db.session.add(developer)
        db.session.commit()

        # Send confirmation email
        html = render_template('email/developer_signup_registered.html')
        subject = 'Dreaming Spires Registration Confirmation'
        send_email(developer.email, subject, html)

        return redirect(url_for('auth.thanks_for_registering_developer'))
    return render_template(template_path, *args, form=form, **kwargs)


@app.route('/', methods=['GET', 'POST'])
def index():
    return client_signup('public/index.html', login_form=LoginForm(), is_fullpage=True)

@app.route('/our_services', methods=['GET', 'POST'])
def our_services():
    return client_signup('public/our_services.html', login_form=LoginForm(), is_fullpage=False)

@app.route('/develop_with_us', methods=['GET', 'POST'])
def develop_with_us():
    return developer_signup('public/develop_with_us.html', login_form=LoginForm(), is_fullpage=False)

@app.route('/about')
def about():
    return render_template('public/about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('public/contact.html', login_form=LoginForm())

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
    return render_template('public/register_developer.html', login_form=LoginForm())

@app.route('/developer_faq')
def developer_faq():
    return render_template('public/developer_faq.html')

@app.route('/portfolio')
def portfolio():
    # Get blog posts from db
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.date_created.desc()).all()
    return render_template('public/portfolio.html', login_form=LoginForm(), posts=posts)

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('public/privacy_policy.html')

