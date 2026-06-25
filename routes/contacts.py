from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from database import db
from models.user import User
from models.contact import Contact
from sqlalchemy import or_

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('/contacts')
@login_required
def contacts():
    q = request.args.get('q', '').strip()
    my_contacts = [c.contact_user for c in current_user.contacts.all()]

    if q:
        my_contacts = [c for c in my_contacts if
            q.lower() in c.name.lower() or
            q.lower() in c.email.lower() or
            q.lower() in c.username.lower()
        ]

    return render_template('contacts.html', contacts=my_contacts, query=q)

@contacts_bp.route('/contacts/add', methods=['POST'])
@login_required
def add_contact():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    if not user or user.id == current_user.id:
        flash('Usuário inválido.', 'error')
        return redirect(url_for('contacts.contacts'))

    existing = Contact.query.filter_by(user_id=current_user.id, contact_id=user.id).first()
    if existing:
        flash(f'{user.name} já está em seus contatos.', 'info')
    else:
        contact = Contact(user_id=current_user.id, contact_id=user.id)
        db.session.add(contact)
        db.session.commit()
        flash(f'✅ {user.name} adicionado aos contatos!', 'success')

    return redirect(url_for('contacts.contacts'))

@contacts_bp.route('/contacts/remove/<int:contact_id>', methods=['POST'])
@login_required
def remove_contact(contact_id):
    contact = Contact.query.filter_by(user_id=current_user.id, contact_id=contact_id).first()
    if contact:
        db.session.delete(contact)
        db.session.commit()
        flash('Contato removido.', 'info')
    return redirect(url_for('contacts.contacts'))

@contacts_bp.route('/contacts/find')
@login_required
def find_people():
    q = request.args.get('q', '').strip()
    results = []
    my_contact_ids = [c.contact_id for c in current_user.contacts.all()]

    if q:
        results = User.query.filter(
            or_(User.name.ilike(f'%{q}%'), User.email.ilike(f'%{q}%'), User.username.ilike(f'%{q}%')),
            User.id != current_user.id
        ).limit(20).all()

    return render_template('find_people.html', results=results, query=q, my_contact_ids=my_contact_ids)
