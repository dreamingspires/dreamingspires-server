# Import flask dependencies
from flask import Blueprint, request, render_template, render_template_string, \
                  flash, g, session, redirect, url_for
from flask_navigation import Navigation
from sqlalchemy.exc import IntegrityError

import app.extensions.sidebar as sb
import app.extensions.chat as chat

# Import the database object from the main app module
from app import db

# Import module models (i.e. Projects)
from app.models import User, Developer
from app.mod_mail.models import MailGroup, MailMessage

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
def generate_test_chat():
    return chat.Chat([
        chat.ChatComment('Edd Salkield', '/static/assets/images/testimonials/edd.jpg', '3h', lorem.paragraph(), '0', children=[
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


def generate_chat(mail_group):
    return chat.Chat(
        [chat.ChatComment(msg.user.display_name, msg.user.display_image, 
                msg.date_created, msg.body, str(i), is_sub_comment=True)
            for i, msg in enumerate(mail_group.messages)]
        + [chat.ChatReply('base', is_reply=False)]).render()

from werkzeug.security import generate_password_hash # TEMP
import time
from datetime import datetime
@mod_mail.route('/generate', methods=['GET', 'POST'])
def generate():
    # Generate a few users
    try:
        edd = User(id='edd',
            password=generate_password_hash(''),
            display_name='Edd Salkield', description='My description',
            primary_email='edd@example.com', developer=Developer())
        db.session.add(edd)
        rogan = User(id='rogan',
            password=generate_password_hash(''),
            display_name='Rogan Clark', description='My description',
            primary_email='rogan@example.com', developer=Developer())
        db.session.add(rogan)
        mark = User(id='mark',
            password=generate_password_hash(''),
            display_name='Mark Todd', description='My description',
            primary_email='mark@example.com', developer=Developer())
        db.session.add(mark)
        josh = User(id='josh',
            password=generate_password_hash(''),
            display_name='Josh Smailes', description='My description',
            primary_email='josh@example.com', developer=Developer())
        db.session.add(josh)

        # Generate a group chat
        empty_group = MailGroup(display_name='The empty chat', users=[edd, rogan, mark, josh])
        db.session.add(empty_group)

        group = MailGroup(display_name='The friend chat', users=[edd, rogan, mark, josh])
        db.session.add(group)
        db.session.commit()

        # Create some messages
        messages = []
        message = MailMessage(user=edd, body='yo wassup', date_created=datetime.now())
        db.session.add(message)
        messages.append(message)
        time.sleep(2)
        message = MailMessage(user=josh, body='nm', date_created=datetime.now())
        db.session.add(message)
        messages.append(message)
        time.sleep(2)
        message = MailMessage(user=mark, body='nm 2', date_created=datetime.now())
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
    
@mod_mail.route('/inbox', methods=['GET', 'POST'])
def inbox():
    # Ensure the user is logged in
    return render_template('mail/inbox.html', sidebar=generate_sidebar(),
            discussion=generate_test_chat())

@mod_mail.route('/group/<group_id>', methods=['GET', 'POST'])
def group(group_id):
    # Ensure the user is logged in

    # Get the group ID
    group = MailGroup.query.filter_by(display_name='The friend chat').first()
    return render_template('mail/group.html', sidebar=generate_sidebar(),
        group=group, discussion=generate_chat(group))
