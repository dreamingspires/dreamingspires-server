# Import flask dependencies
from flask import Blueprint, request, render_template, render_template_string, \
                  flash, g, session, redirect, url_for
from flask_navigation import Navigation

import app.extensions.sidebar as sb
import app.extensions.jobs as jobs

# Import the database object from the main app module
from app import db

# Import module models (i.e. Projects)
from app.models import Project

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_marketplace = Blueprint('marketplace', __name__, url_prefix='/')

# TODO: think about how to tell if a link is active or not
def generate_sidebar():
    menu = sb.Menu([
        sb.MenuLabel('General'),
        sb.MenuList(None, [
            sb.MenuLink('<span class="icon is-small"><i class="fa fa-tachometer"></i></span> Dashboard', 'dashboard'), # TODO: resolve URLs properly
            sb.MenuLink('<span class="icon is-small"><i class="fa fa-store-alt"></i></span> Marketplace', 'marketplace'),
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
    dep = project.department
    org = dep.organisation

    # Generate tags tuples
    tags = [(tag.display_name, tag.colour, 'broken_tag_link') for tag \
            in project.tags]

    return jobs.JobListing(
        job_link='broken_job_link',
        title=project.display_name,
        date=project.date_created.strftime('%Y-%M-%d'),
        ect=str(project.ect) if project.ect is not None else '',
        cost=str(project.price),
        organisation=org.display_name,
        organisation_link=url_for('organisations.organisation', 
            organisation_id=org.id),
        department=dep.display_name,
        department_link=url_for('organisations.department',
            organisation_id=org.id, department_id=dep.id),
        tags=tags,
        description=project.description,
        colour='#e0ffff',
        image_link=project.display_image
    )

@mod_marketplace.route('/marketplace', methods=['GET', 'POST'])
def marketplace():
    # Ensure the user is logged in

    # Generate the appropriate sidebar
    sidebar = generate_searchbar()

    # Get some job listings
    projects = Project.query.limit(5).all()
    job_listings = [create_job_listing(project).render() for project in projects]

    #sample_job_listing = jobs.JobListing(**sample_job)
    #sample_job_listing_2 = jobs.JobListing(**sample_job_2)
    return render_template('marketplace/marketplace.html', sidebar=sidebar, job_listings=job_listings)
