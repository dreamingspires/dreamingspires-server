import pdb
# Import flask dependencies
from flask import Blueprint, request, render_template, render_template_string, \
                  flash, g, session, redirect, url_for
from flask_navigation import Navigation

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_projects = Blueprint('projects', __name__, url_prefix='/')

sidebar = Navigation()
sidebar.Bar('sidebar', [
    sidebar.Item('Dashboard', '')
])


class MenuElement():
    def render(self):
        return ''

class MenuLabel(MenuElement):
    def __init__(self, label):
        self.label = label

    def render(self):
        return """
            <p class="menu-label">
                {}
            </p>
            """.format(self.label)

class MenuLink(MenuElement):
    def __init__(self, label, href=""):
        self.label = label
        self.href = href

    def render(self):
        return """
        <a href={}>
            {}
        </a>
        """.format(self.href, self.label)

class MenuList(MenuElement):
    def __init__(self, head=None, children=[]):
        self.head = head
        self.children = children

    def render(self):
        lines = [self.head.render()] if self.head is not None else []
        lines.append('<ul class="menu-list">')
        for child in self.children:
            lines.append('<li>')
            lines.append(child.render())
            lines.append('</li>')
        lines.append('</ul>')
        return '\n'.join(lines)

# TODO: technically this could be formatted better, if this was ever to be
# expanded fully into a flask plugin
# This makes use of the bulma-collapsible extension
class MenuCollapsibleList(MenuElement):
    def __init__(self, collapsible_id, label, href, children):
        self.collapsible_id = collapsible_id
        self.label = label
        self.href = href
        self.children = children

    def render(self):
        name = f'collapsible-div-{self.collapsible_id}'
        print(name)

        lines = [f'<a href="#{name}" data-action="collapse">{self.label}</a>']
        lines.append(f'<div id="{name}" class="is-collapsible">')
        lines.append('<ul>')
        for child in self.children:
            lines.append('<li>')
            lines.append(child.render())
            lines.append('</li>')
        lines.append('</ul>')
        lines.append('</div>')
        print(lines)
        return '\n'.join(lines)

class Menu(MenuElement):
    def __init__(self, children=[]):
        self.children = children

    def render(self):
        lines = ['<aside class="menu">']
        for child in self.children:
            lines.append(child.render())
        lines.append('</aside>')
        return '\n'.join(lines)

# TODO: think about how to tell if a link is active or not
def generate_sidebar():
    menu = Menu([
        MenuLabel('General'),
        MenuList(None, [
            MenuLink('Dashboard', 'dashboard'), # TODO: resolve URLs properly
            MenuLink('Marketplace', 'marketplace'),
        ]),
        MenuLabel('Developer'),
        MenuList(None, [
            MenuCollapsibleList(0, 'Current Assignments', '', [
                MenuLink('Assignment 1', ''),
                MenuLink('Assignment 2', '')
            ]),
            MenuLink('Past Assignments'),
            MenuLink('Payroll')
        ]),
        MenuLabel('Organisations'),
        MenuList(None, [
            MenuCollapsibleList(1, 'University of Oxford', '', [
		MenuList(MenuLink('Dept. of Computer Science', ''), [
		    MenuLink('Test 1', ''),
		    MenuLink('Test 2', '')
		])
	    ])
	])
    ])
    return menu.render()


@mod_projects.route('/projects', methods=['GET', 'POST'])
def projects():
    # Ensure the user is logged in

    # Generate the appropriate sidebar

    sidebar = generate_sidebar()
    return render_template('projects/projects.html', sidebar=sidebar)
