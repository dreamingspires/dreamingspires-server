# Import flask dependencies
from flask import Blueprint, request, render_template, render_template_string, \
                  flash, g, session, redirect, url_for
from flask_navigation import Navigation
from flask_login import login_required, current_user
from flask_socketio import send, emit, join_room, leave_room
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, all_

import app.extensions.sidebar as sb
import app.extensions.chat as chat

# Import the database object from the main app module
from app import db, socketio

# Import module models (i.e. Projects)
from app.models import User, Developer, Organisation, Department
from app.mod_mail.models import MailGroup, MailMessage, MailUserRole, \
    ReadReceipt
from app.mod_mail.forms import ReplyForm

# Import extensions
from app.extensions.socketio_helpers import authenticated_only


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

def generate_chat(mail_group):
    return [chat.ChatComment(msg.user.display_name, msg.user.display_image, 
                msg.date_created, msg.body, str(i), is_sub_comment=True)
            for i, msg in enumerate(mail_group.messages)]

from werkzeug.security import generate_password_hash # TEMP
import time
from datetime import datetime

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

        # Generate some organisations
        oxford_cs = Department(display_name='Computer Science', description='''
            Oxford CS description
        ''', users=[edd])
        oxford_anthro = Department(display_name='Anthropology', description='''
            Oxford Anthropology description
        ''', users=[edd])
        oxford = Organisation(display_name='University of Oxford', description='''
            This is the description of the Universty of Oxford
        ''', departments=[oxford_cs, oxford_anthro])

        cambridge_anthro = Department(display_name='Anthropology', description='''
            Cambridge Anthropology description
        ''', users=[edd])
        cambridge = Organisation(display_name='University of Cambridge', description='''
            This is the description of the Universty of Cambridge 
        ''', departments=[cambridge_anthro])

        db.session.add(oxford)
        db.session.add(cambridge)

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
    def __init__(self, icons, text, href, group_id, person_list, bold):
        self.icons = icons
        self.text = text
        self.href = href
        self.group_id = group_id
        self.person_list = person_list
        self.bold = bold

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

def read_latest_message_yet(current_user, group):
    # Get the current read receipt for the user
    rr = ReadReceipt.query.filter_by(user=current_user).filter_by(group=group).first()
    return (len(group.messages) == 0) \
        or (rr is not None and rr.date_modified >= group.messages[-1].date_created)

def generate_inbox(current_user, tab_list, current_tab, groups, request_args):
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
            ['fa-envelope-open'] if read_latest_message_yet(current_user, group)
                else ['fa-envelope'],
            group.display_name if read_latest_message_yet(current_user, group)
                else f'{group.display_name}',
            url_for('mail.inbox', **{**request_args, **{'group_id': group.id}}),
            group.id,
            [],  # TODO: dynamically join to create InboxPerson as required
#            [InboxPerson(user.id, user.display_image) \
#                for user in group.user_roles.user]
            not read_latest_message_yet(current_user, group)
        ) for group in groups]

    return Inbox(tabs, current_tab, inbox_entries)

def update_read_receipt(current_user, group):
    rr = ReadReceipt.query.filter_by(user=current_user).filter_by(group=group).first()
    if rr is not None:
        rr.date_modified = db.func.current_timestamp()
    else:
        rr = ReadReceipt(user=current_user)
        group.read_receipts.append(rr)
    db.session.add(rr)
    db.session.add(group)
    db.session.commit()

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


    group_id = request.args.get('group_id')
    if group_id is None:
        # Try to get the first message
        group_id = None # TODO

    # Render the chat
    discussion = ''
    group = None
    form = ReplyForm()
    profile_image = current_user.display_image.thumb_url \
        if current_user.display_image is not None \
        else 'https://bulma.io/images/placeholders/128x128.png'

    if group_id is not None:
        group = MailGroup.query.filter_by(id=group_id).first()
        if form.validate_on_submit():
            # Add the new message into the database
            # TODO: deduplication
            message = MailMessage(user=current_user, body=form.body.data)
            group.messages.append(message)

            # Save and send a 'message changed' event to all relevant clients
            db.session.commit()

            update_read_receipt(current_user, group)

            # Notify clients of the new message
            socketio.emit('new_message', 
                {
                    'profile_image': profile_image,
                    'profile_name': current_user.display_name,
                    'comment_text': form.body.data,
                    'comment_time': message.date_created.strftime('%Y-%M-%d'),
                    'group_id': group.id
                },
                room=group_id)

            return redirect(url_for('mail.inbox', 
                **{**request.args, **{'group_id': group.id}}))
            # TODO: return redirect to page anchor at bottom of messages

        update_read_receipt(current_user, group)
        discussion=generate_chat(group)

    inbox = generate_inbox(current_user, tab_list, current_tab, groups, request.args)
    chat_comments = generate_chat(group) if group is not None else []
    display_name = group.display_name if group is not None else ''
    return render_template('mail/inbox.html', inbox=inbox,
            chat_name = display_name,
            group_ids=[group.id for group in groups],
            chat_comments=chat_comments, reply_form=form,
            profile_image=profile_image,
            current_group_id=group_id)

#@mod_mail.route('/group/<group_id>', methods=['GET', 'POST'])
@login_required
def group(group_id):
    # TODO: ensure the user is in this particular group
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
        group=group, chat_comments=generate_chat(group), reply_form=form,
        profile_image='https://bulma.io/images/placeholders/128x128.png')


## socketio
@mod_mail.route('/send_broadcast', methods=['GET', 'POST'])
def send_broadcast():
    socketio.emit('test_broadcast', {'data': 42})
    return 'Broadcast triggered'
#    room=session['socketio_sid']

@socketio.on('join')
@authenticated_only
def on_join(data):
    print('joining ' + str(type(data['group_id'])))
    group_id = data['group_id']
    group = MailGroup.query.filter_by(id=group_id).first()

    # Ensure that the user is allowed in this room
    if current_user not in [role.user for role in group.user_roles]:
        return False

    join_room(group_id)

@socketio.on('leave')
@authenticated_only
def on_leave(data):
    room = data['room']
    leave_room(room)
