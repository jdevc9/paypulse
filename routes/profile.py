from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

profile_bp = Blueprint('profile', __name__)
help_bp = Blueprint('help', __name__)

@profile_bp.route('/profile')
@login_required
def profile():
    txns = current_user.get_all_transactions()
    sent = [t for t in txns if t.sender_id == current_user.id and t.status == 'completed']
    received = [t for t in txns if t.receiver_id == current_user.id and t.status == 'completed']
    return render_template('profile.html',
        sent_count=len(sent),
        received_count=len(received),
        sent_total=sum(t.amount for t in sent),
        received_total=sum(t.amount for t in received),
    )

@profile_bp.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    bio = request.form.get('bio', '').strip()

    if name:
        current_user.name = name
        current_user.avatar_initials = ''.join([n[0].upper() for n in name.split()[:2]])
    if phone:
        current_user.phone = phone
    current_user.bio = bio

    db.session.commit()
    flash('✅ Perfil atualizado com sucesso!', 'success')
    return redirect(url_for('profile.profile'))

@profile_bp.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    current_pass = request.form.get('current_password', '')
    new_pass = request.form.get('new_password', '')
    confirm = request.form.get('confirm_password', '')

    if not check_password_hash(current_user.password_hash, current_pass):
        flash('Senha atual incorreta.', 'error')
        return redirect(url_for('profile.profile'))
    if new_pass != confirm:
        flash('As senhas não coincidem.', 'error')
        return redirect(url_for('profile.profile'))
    if len(new_pass) < 6:
        flash('A nova senha deve ter pelo menos 6 caracteres.', 'error')
        return redirect(url_for('profile.profile'))

    current_user.password_hash = generate_password_hash(new_pass)
    db.session.commit()
    flash('✅ Senha alterada com sucesso!', 'success')
    return redirect(url_for('profile.profile'))

@help_bp.route('/help')
def help_page():
    topic = request.args.get('topic', '')
    return render_template('help.html', topic=topic)
