# Import flask dependencies
from flask import Blueprint, request, render_template, render_template_string, \
                  flash, g, session, redirect, url_for
from flask_navigation import Navigation
from flask_login import login_required, current_user

import app.extensions.sidebar as sb
import app.extensions.timeline as tl
import app.extensions.jobs as jobs
import app.extensions.chat as chat
import app.types as t
from app.extensions.decorators import verified_user_required

# Import the database object from the main app module
from app import db

# Import module models (i.e. Projects)
from app.models import Project, Developer, DeveloperProjectsMap

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_marketplace = Blueprint('marketplace', __name__, url_prefix='/')

def generate_sidebar():
    menu = sb.Menu([
        sb.MenuLabel('Developer'),
        sb.MenuList(None, [
            sb.MenuCollapsibleList(0, '<span class="icon is-small"><i class="fa fa-clipboard-list"></i></span> Current Assignments', '', [
                sb.MenuLink('Assignment 1', ''),
                sb.MenuLink('Assignment 2', '')
            ], mouseover=True),
            sb.MenuLink('<span class="icon is-small"><i class="fa fa-clipboard-check"></i></span> Past Assignments'),
            sb.MenuLink('<span class="icon is-small"><i class="fa fa-money-check-alt"></i></span> Payroll')
        ]),
    ])
    return menu.render()

# TODO: think about how to tell if a link is active or not
def generate_sidebar_old():
    menu = sb.Menu([
        sb.MenuLabel('General'),
        sb.MenuList(None, [
            sb.MenuLink('<span class="icon is-small"><i class="fa fa-tachometer"></i></span> Dashboard', url_for('marketplace.dashboard')),
            sb.MenuLink('<span class="icon is-small"><i class="fa fa-store-alt"></i></span> Marketplace', url_for('marketplace.marketplace')),
        ]),
        sb.MenuLabel('Developer'),
        sb.MenuList(None, [
            sb.MenuCollapsibleList(0, '<span class="icon is-small"><i class="fa fa-clipboard-list"></i></span> Current Assignments', '', [
                sb.MenuLink('Assignment 1', ''),
                sb.MenuLink('Assignment 2', '')
            ], mouseover=True),
            sb.MenuLink('<span class="icon is-small"><i class="fa fa-clipboard-check"></i></span> Past Assignments'),
            sb.MenuLink('<span class="icon is-small"><i class="fa fa-money-check-alt"></i></span> Payroll')
        ]),
        sb.MenuLabel('Organisations'),
        sb.MenuList(None, [
            sb.MenuCollapsibleList(1, '<span class="icon is-small"><i class="fa fa-university"></i></span> University of Oxford', '', [
		sb.MenuList(sb.MenuLink('<span class="icon is-small"><i class="fa fa-desktop"></i></span> Dept. of Computer Science', ''), [
		    sb.MenuLink('Test 1', ''),
		    sb.MenuLink('Test 2', '')
		])
	    ], mouseover=True)
	])
    ])
    return menu.render()

def generate_searchbar():
    menu = sb.Menu([
        sb.MenuLabel('Organisation'),
        sb.MenuList(None, [
            sb.MenuCollapsibleList(0, sb.MenuCheckbox('>', 'University of Oxford', 'checkbox_university-of-oxford'), '', [
                sb.MenuCheckbox('', 'Dept. of Computer Science', 'checkbox_university-of-oxford_department-of-computer-science'),
                sb.MenuCheckbox('', 'Dept. of Engineering', 'checkbox_university-of-oxford_department-of-engineering'),
                sb.MenuCheckbox('', 'Dept. of Anthropology', 'checkbox_university-of-oxford_department-of-anthropology'),
            ], mouseover=True)
        ]),
        sb.MenuLabel('Pay'),
        sb.MenuList(None, [
            sb.MenuNumericRange('£', ' to £', 'Go!')
        ]),
        sb.MenuLabel('Language'),
        sb.MenuList(None, [
            sb.MenuCheckbox('', '<span class="icon is-small"><i class="devicon-python-plain"></i></span> Python', 'checkbox_language_python'),
            sb.MenuCheckbox('', '<span class="icon is-small"><i class="devicon-c-plain"></i></span> C', 'checkbox_language_c'),
            sb.MenuCheckbox('', '<span class="icon is-small"><i class="devicon-java-plain"></i></span> Java', 'checkbox_language_java'),
            sb.MenuCheckbox('', '<span class="icon is-small"><i class="devicon-javascript-plain"></i></span> Javascript', 'checkbox_language_javascript')
        ]),
        sb.MenuLabel('Experience level'),
        sb.MenuList(None, [
            sb.MenuCheckbox('', 'Beginner', 'checkbox_experience_beginner'),
            sb.MenuCheckbox('', 'Intermediate', 'checkbox_experience_intermediate'),
            sb.MenuCheckbox('', 'Advanced', 'checkbox_experience_advanced')
        ]),
        sb.MenuLabel('Estimated duration'),
        sb.MenuList(None, [
            sb.MenuCheckbox('', '< 1 day', 'checkbox_duration_1d'),
            sb.MenuCheckbox('', 'A few days', 'checkbox_duration_few-days'),
            sb.MenuCheckbox('', 'A week', 'checkbox_duration_week'),
            sb.MenuCheckbox('', 'A few weeks', 'checkbox_duration_few-weeks'),
            sb.MenuCheckbox('', 'Several months', 'checkbox_duration_months'),
            sb.MenuCheckbox('', 'Long term', 'checkbox_duration_long-term')
        ]),
        #sb.MenuLabel('Tags'),   # TODO: textbox with dropdown options
        #sb.MenuList(None, [
        #    sb.MenuCheckbox('', '< 1 day', 'checkbox_duration_1d'),
        #])

        
    ])
    return menu.render()

def generate_timeline():
    return tl.Timeline([
        tl.TimelineHeader('Start', 'is-medium is-primary'),
        tl.TimelineItem('', 'is-primary', 'January 2020', 'Project approved',
            '', 'is-primary'),
        tl.TimelineItem('', 'is-warning', 'Current date',
            'Assign developer to project', '', ''),
        tl.TimelineItem('<i class="fa fa-flag"></i>', 'is-icon', 'March 2020',
            'Project approved', '', ''),
        tl.TimelineItem('<i class="fa fa-file-alt"></i>', 'is-icon', 'June 2020',
            'Estimated project review', '', ''),
        tl.TimelineHeader('End', 'is-medium is-primary'),

    ]).render()

def generate_chat():
    return chat.Chat([
        chat.ChatComment('Edd Salkield', '/static/assets/images/testimonials/edd.jpg', '3h', 'This is my comment. I am typing it now.', '0', children=[
            chat.ChatComment('Rogan Clark', '/static/assets/images/testimonials/rogan.jpg', '2h', 'Ummm.', '0.0', is_sub_comment=True),
            chat.ChatComment('Mark Todd', '/static/assets/images/testimonials/mark.jpg', '2h', 'This is my reply.', '0.1', is_sub_comment=True),
            chat.ChatComment('Calum White', None, '2h', 'This is my reply.', '0.2', is_sub_comment=True)
        ]),
        chat.ChatComment('Edd Salkield', '/static/assets/images/testimonials/edd.jpg', '3h', 'This is my comment. I am typing it now.', '0', children=[
            chat.ChatComment('Rogan Clark', '/static/assets/images/testimonials/rogan.jpg', '2h', 'Ummm.', '0.0', is_sub_comment=True),
            chat.ChatComment('Mark Todd', '/static/assets/images/testimonials/mark.jpg', '2h', 'This is my reply.', '0.1', is_sub_comment=True),
            chat.ChatComment('Calum White', None, '2h', 'This is my reply.', '0.2', is_sub_comment=True)
        ]),
        chat.ChatReply('base', is_reply=False)
    ]).render()

sample_job = {
    'job_link': 'broken_job_link',
    'title': 'Do a thing (generated)',
    'date': '2020-07-03',
    'ect': '2 weeks',
    'cost': '£1000',
    'organisation': 'University of Oxford',
    'organisation_link': 'broken_organisation_link',
    'department': 'Dept. of Computer Science',
    'department_link': 'broken_department_link',
    'tags': [('Python', 'link', 'broken_tag_link'), ('Porting', None, 'broken_tag_link')],
    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ornare magna eros, eu pellentesque tortor vestibulum ut. Maecenas non massa sem. Etiam finibus odio quis feugiat facilisis.',
    'colour': None,
#    'image_link': None
    'image_link': 'https://i.ebayimg.com/images/i/400818616312-0-1/s-l1000.jpg'
}

sample_job = {
    'job_link': 'broken_job_link',
    'title': 'Do a thing (generated)',
    'date': '2020-07-03',
    'ect': '2 weeks',
    'cost': '£1000',
    'organisation': 'University of Oxford',
    'organisation_link': 'broken_organisation_link',
    'department': 'Dept. of Computer Science',
    'department_link': 'broken_department_link',
    'tags': [('Python', 'link', 'broken_tag_link'), ('Porting', None, 'broken_tag_link')],
    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ornare magna eros, eu pellentesque tortor vestibulum ut. Maecenas non massa sem. Etiam finibus odio quis feugiat facilisis.',
    'colour': None,
#    'image_link': None
    'image_link': 'https://i.ebayimg.com/images/i/400818616312-0-1/s-l1000.jpg'
}

sample_job_2 = {
    'job_link': 'broken_job_link',
    'title': 'Do a thing (generated)',
    'date': '2020-07-03',
    'ect': '2 weeks',
    'cost': '£1000',
    'organisation': 'University of Oxford',
    'organisation_link': 'broken_organisation_link',
    'department': 'Dept. of Computer Science',
    'department_link': 'broken_department_link',
    'tags': [('Python', 'link', 'broken_tag_link'), ('Porting', None, 'broken_tag_link')],
    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ornare magna eros, eu pellentesque tortor vestibulum ut. Maecenas non massa sem. Etiam finibus odio quis feugiat facilisis.',
    'colour': '#e0ffff',
#    'image_link': None
    'image_link': 'https://i.ebayimg.com/images/i/400818616312-0-1/s-l1000.jpg'
}

def create_job_listing(project):
    # Add the project back into the session, thus permitting lazy-loading
    # of its related classes
    db.session.add(project)
    dep = project.department
    org = dep.organisation

    # Generate tags tuples
    tags = [(tag.display_name, tag.colour, 'broken_tag_link') for tag \
            in project.tags]
    

    return jobs.JobListing(
        job_link=url_for('marketplace.projects', project_id=project.id),
        title=project.display_name,
        date=project.date_created.strftime('%Y-%M-%d'),
        ect=str(project.ect) if project.ect is not None else None,
        cost=str(project.price),
        organisation=org.display_name if org else '',
        organisation_link=url_for('organisations.organisation', 
            organisation_id=org.id) if org else '',
        department=dep.display_name,
        department_link=url_for('organisations.department',
            department_id=dep.id),
        tags=tags,
        description=project.description,
        colour='#e0ffff',
        image_link=project.display_image.url if project.display_image else 'https://bulma.io/images/placeholders/128x128.png'
    )

@mod_marketplace.route('/marketplace', methods=['GET', 'POST'])
@login_required
def marketplace():
    if not(current_user.developer and \
            current_user.developer.verification_status == t.VerificationStatus.accepted):
        return redirect(url_for('profile.landing_page'))

    # Generate the appropriate sidebar
    sidebar = generate_searchbar()

    # Get some job listings TODO: eventually limit results per page, paginate
    projects = Project.query.all()
    job_listings = [create_job_listing(project).render() for project in projects]

    return render_template('marketplace/marketplace.html', sidebar=sidebar, job_listings=job_listings)

@mod_marketplace.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Ensure the user is logged in

    # Generate the appropriate sidebar
    sidebar = generate_sidebar()

    # Get some job listings
    return render_template('marketplace/dashboard.html', sidebar=sidebar)

@mod_marketplace.route('/projects/<project_id>')
@login_required
def projects(project_id):
    # Look up the project ID
    [project] = Project.query.filter(Project.id == project_id).all()
    job_listing = create_job_listing(project).render()
    db.session.add(current_user)
    developer = current_user.developer

    # Build a table of the user's current assignments
    assignments = Developer.query.join(DeveloperProjectsMap).filter(DeveloperProjectsMap.developer_id == developer.id).all()

    assignments_dict = {e: [] for e in t.DeveloperProjectStatus}
    for assignment in assignments:
        assignments_dict[assignment.role].append(
            Project.query.filter(id=assignment.project_id))

    print('### Assignments:')
    print(assignments_dict)

    return render_template('marketplace/project.html', project=project, \
            job_listing=job_listing, timeline=generate_timeline())
            #, discussion=generate_chat()

@mod_marketplace.route('/projects/<project_id>/register_interest')
@login_required
def register_interest(project_id):
    # Ensure that the current user is a developer
    if not (developer := current_user.developer):
        return 'Forbidden'

    # Get the project
    project = Project.query.filter_by(id=project_id).first()

    # Mark user as interested
    a = DeveloperProjectsMap(role=t.DeveloperProjectStatus.interested)
    project.developers.append(a)
    developer.projects.append(a)
    
    # Save
    db.session.add(a)
    db.session.add(project)
    db.session.add(developer)
    db.session.commit()

    # Create a chat room with the user and Dreaming Spires
