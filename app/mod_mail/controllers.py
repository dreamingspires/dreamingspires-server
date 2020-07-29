# Import flask dependencies
from flask import Blueprint, request, render_template, render_template_string, \
                  flash, g, session, redirect, url_for
from flask_navigation import Navigation
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, all_

import app.extensions.sidebar as sb
import app.extensions.chat as chat

# Import the database object from the main app module
from app import db

# Import module models (i.e. Projects)
from app.models import User, Developer
from app.mod_mail.models import MailGroup, MailMessage, MailUserRole
from app.mod_mail.forms import ReplyForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_mail = Blueprint('mail', __name__, url_prefix='/mail/')

def generate_sidebar():
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

import lorem
#def generate_test_chat():
#    return chat.Chat([
#        chat.ChatComment('Edd Salkield', '/static/assets/images/testimonials/edd.jpg', '3h', lorem.paragraph(), '0', children=[
#            chat.ChatComment('Rogan Clark', '/static/assets/images/testimonials/rogan.jpg', '2h', 'Ummm.', '0.0', is_sub_comment=True),
#            chat.ChatComment('Mark Todd', '/static/assets/images/testimonials/mark.jpg', '2h', 'This is my reply.', '0.1', is_sub_comment=True),
#            chat.ChatComment('Calum White', None, '2h', 'This is my reply.', '0.2', is_sub_comment=True)
#        ]),
#        chat.ChatComment('Edd Salkield', '/static/assets/images/testimonials/edd.jpg', '3h', 'This is my comment. I am typing it now.', '0', children=[
#            chat.ChatComment('Rogan Clark', '/static/assets/images/testimonials/rogan.jpg', '2h', 'Ummm.', '0.0', is_sub_comment=True),
#            chat.ChatComment('Mark Todd', '/static/assets/images/testimonials/mark.jpg', '2h', 'This is my reply.', '0.1', is_sub_comment=True),
#            chat.ChatComment('Calum White', None, '2h', 'This is my reply.', '0.2', is_sub_comment=True)
#        ]),
#        chat.ChatReply('base', is_reply=False)
#    ]).render()


def generate_chat(mail_group, reply_form):
    return chat.Chat(
        [chat.ChatComment(msg.user.display_name, msg.user.display_image, 
                msg.date_created, msg.body, str(i), reply_form, is_sub_comment=True)
            for i, msg in enumerate(mail_group.messages)]
        + [chat.ChatReply('base', reply_form, is_reply=False)]).render()

from werkzeug.security import generate_password_hash # TEMP
import time
from datetime import datetime
@mod_mail.route('/generate', methods=['GET', 'POST'])
def generate():
    # Generate a few users
    try:
        edd = User(id='edd',
            password=generate_password_hash('e'),
            display_name='Edd Salkield', description='My description',
            primary_email='edd@example.com', developer=Developer())
        edd_role = MailUserRole(user=edd, creator=True, relationship='Interested')
        edd_role_c = MailUserRole(user=edd, creator=True, relationship='Current')
        edd_role_p = MailUserRole(user=edd, creator=True, relationship='Past')
        edd_role_o = MailUserRole(user=edd, creator=True, relationship='Other')
        db.session.add(edd)
        db.session.add(edd_role)
        rogan = User(id='rogan',
            password=generate_password_hash('e'),
            display_name='Rogan Clark', description='My description',
            primary_email='rogan@example.com', developer=Developer())
        rogan_role = MailUserRole(user=rogan, creator=False, relationship='Current')
        db.session.add(rogan)
        db.session.add(rogan_role)
        mark = User(id='mark',
            password=generate_password_hash('e'),
            display_name='Mark Todd', description='My description',
            primary_email='mark@example.com', developer=Developer())
        mark_role = MailUserRole(user=mark, creator=False, relationship='Past')
        db.session.add(mark)
        db.session.add(mark_role)
        josh = User(id='josh',
            password=generate_password_hash('e'),
            display_name='Josh Smailes', description='My description',
            primary_email='josh@example.com', developer=Developer())
        josh_role = MailUserRole(user=josh, creator=False, relationship='Other')
        db.session.add(josh)
        db.session.add(josh_role)

        # Generate a group chat
        user_roles = [edd_role, rogan_role, mark_role, josh_role]
        empty_group = MailGroup(display_name='The empty chat', user_roles=user_roles)
        db.session.add(empty_group)

        group = MailGroup(display_name='The friend chat', user_roles=user_roles)
        db.session.add(group)
        group = MailGroup(display_name='The current chat', user_roles=[edd_role_c])
        db.session.add(group)
        group = MailGroup(display_name='The past chat', user_roles=[edd_role_p])
        db.session.add(group)
        group = MailGroup(display_name='The other chat', user_roles=[edd_role_o])
        db.session.add(group)
        db.session.commit()

        # Create some messages
        messages = []
        message = MailMessage(user=edd, body='yo wassup', date_created=datetime.utcnow())
        db.session.add(message)
        messages.append(message)
        time.sleep(2)
        message = MailMessage(user=josh, body='nm', date_created=datetime.utcnow())
        db.session.add(message)
        messages.append(message)
        time.sleep(2)
        message = MailMessage(user=mark, body='nm 2', date_created=datetime.utcnow())
        db.session.add(message)
        messages.append(message)
        db.session.commit()
        group.messages = messages

        # Save changes
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        group = MailGroup.query.filter_by(display_name='The friend chat').first()
        return f'messages already generated. Group id: {group.id}'
    else:
        return 'messages generated'
    
class InboxPerson():
    def __init__(self, user_id, display_image):
        self.display_image = display_image
        self.user_id = user_id

class InboxEntry():
    def __init__(self, icons, text, href, person_list):
        self.icons = icons
        self.text = text
        self.href = href
        self.person_list = person_list

class InboxTab():
    def __init__(self, text, href, is_current_tab):
        self.text = text
        self.href = href
        self.is_current_tab = is_current_tab

class Inbox():
    def __init__(self, tab_list, current_tab, inbox_entries):
        self.tab_list = tab_list
        self.current_tab = current_tab
        self.inbox_entries = inbox_entries


def generate_inbox(tab_list, current_tab, groups, request_args):
    if not current_tab in tab_list:
        current_tab = tab_list[0]

    tabs = [
        InboxTab(
            tab_name,
            url_for('mail.inbox', **{**request_args, **{'current_tab': tab_name}}),
            tab_name == current_tab)
        for tab_name in tab_list]

    inbox_entries = [
        InboxEntry(
            ['fa-envelope'],
            group.display_name,
            url_for('mail.inbox', **{**request_args, **{'group_id': group.id}}),
            []  # TODO: dynamically join to create InboxPerson as required
#            [InboxPerson(user.id, user.display_image) \
#                for user in group.user_roles.user]
        ) for group in groups]

    return Inbox(tabs, current_tab, inbox_entries)

@mod_mail.route('/inbox', methods=['GET', 'POST'])
@login_required
def inbox():

    # Generate the sidebar
    selectable_tabs = ['Interested', 'Current', 'Past']
    tab_list = ['All'] + selectable_tabs + ['Other']
    current_tab = request.args.get('current_tab') if \
        request.args.get('current_tab') is not None and \
            request.args.get('current_tab') in tab_list \
        else tab_list[0]

    user_roles = MailUserRole.query.filter(MailUserRole.user.has(id=current_user.id))
    if current_tab == 'All':
        pass
    elif current_tab == 'Other':
        user_roles = user_roles.filter(~MailUserRole.relationship.in_(selectable_tabs)).all()
    else:
        user_roles = user_roles.filter(MailUserRole.relationship==current_tab).all()

    user_role_ids = [role.id for role in user_roles]
    groups = MailGroup.query.filter(
        MailGroup.user_roles.any(MailUserRole.id.in_(user_role_ids))
    )

    inbox = generate_inbox(tab_list, current_tab, groups, request.args)
    print(inbox.inbox_entries)

    group_id = request.args.get('group_id')
    if group_id is None:
        # Try to get the first message
        group_id = None # TODO

    # Render the chat
    discussion = ''
    if group_id is not None:
        group = MailGroup.query.filter_by(id=group_id).first()
        form = ReplyForm()
        if form.validate_on_submit():
            message = MailMessage(user=current_user, body=form.body.data)
            group.messages.append(message)

            # Save and refresh the page
            db.session.commit()
            return redirect(url_for('mail.inbox', 
                **{**request_args, **{'group_id': group.id}}))

        discussion=generate_chat(group, ReplyForm())

    return render_template('mail/inbox.html', inbox=inbox,
            discussion=discussion)

@mod_mail.route('/group/<group_id>', methods=['GET', 'POST'])
@login_required
def group(group_id):
    # Ensure the user is logged in
    form = ReplyForm()
    group = MailGroup.query.filter_by(id=group_id).first()

    if form.validate_on_submit():
        # Construct the next message
        print("constructing message")
        message = MailMessage(user=current_user, body=form.body.data)
        group.messages.append(message)

        # Save and refresh the page
        print("saving")
        db.session.commit()
        return redirect(url_for('mail.group', group_id=group_id))

    return render_template('mail/group.html', sidebar=generate_sidebar(),
        group=group, discussion=generate_chat(group, form))
