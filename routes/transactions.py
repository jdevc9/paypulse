from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from database import db
from models.user import User
from models.transaction import Transaction

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/send', methods=['GET', 'POST'])
@login_required
def send():
    prefill_user = None
    prefill_id = request.args.get('to')
    if prefill_id:
        prefill_user = User.query.get(prefill_id)

    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        amount_str = request.form.get('amount', '0').replace(',', '.')
        description = request.form.get('description', '').strip()

        try:
            amount = float(amount_str)
        except ValueError:
            flash('Valor inválido.', 'error')
            return redirect(url_for('transactions.send'))

        if amount <= 0:
            flash('O valor deve ser maior que zero.', 'error')
            return redirect(url_for('transactions.send'))

        if amount > current_user.balance:
            flash(f'Saldo insuficiente. Seu saldo é R$ {current_user.balance:,.2f}.', 'error')
            return redirect(url_for('transactions.send'))

        recipient = User.query.get(recipient_id)
        if not recipient or recipient.id == current_user.id:
            flash('Destinatário inválido.', 'error')
            return redirect(url_for('transactions.send'))

        current_user.balance -= amount
        recipient.balance += amount

        txn = Transaction(
            sender_id=current_user.id,
            receiver_id=recipient.id,
            amount=amount,
            description=description or 'Transferência',
            status='completed'
        )
        db.session.add(txn)
        db.session.commit()

        flash(f'✅ R$ {amount:,.2f} enviado com sucesso para {recipient.name}!', 'success')
        return redirect(url_for('transactions.history'))

    users = User.query.filter(User.id != current_user.id).all()
    return render_template('send.html', users=users, prefill_user=prefill_user)

@transactions_bp.route('/request-money', methods=['GET', 'POST'])
@login_required
def request_money():
    prefill_user = None
    prefill_id = request.args.get('from')
    if prefill_id:
        prefill_user = User.query.get(prefill_id)

    if request.method == 'POST':
        from_id = request.form.get('from_id')
        amount_str = request.form.get('amount', '0').replace(',', '.')
        description = request.form.get('description', '').strip()

        try:
            amount = float(amount_str)
        except ValueError:
            flash('Valor inválido.', 'error')
            return redirect(url_for('transactions.request_money'))

        from_user = User.query.get(from_id)
        if not from_user or from_user.id == current_user.id:
            flash('Usuário inválido.', 'error')
            return redirect(url_for('transactions.request_money'))

        txn = Transaction(
            sender_id=from_user.id,
            receiver_id=current_user.id,
            amount=amount,
            description=f'[COBRANÇA] {description or "Solicitação de pagamento"}',
            status='pending'
        )
        db.session.add(txn)
        db.session.commit()

        flash(f'📨 Cobrança de R$ {amount:,.2f} enviada para {from_user.name}!', 'success')
        return redirect(url_for('transactions.history'))

    users = User.query.filter(User.id != current_user.id).all()
    return render_template('request_money.html', users=users, prefill_user=prefill_user)

@transactions_bp.route('/transactions')
@login_required
def history():
    filter_type = request.args.get('type', 'all')
    txns = current_user.get_all_transactions()

    if filter_type == 'sent':
        txns = [t for t in txns if t.sender_id == current_user.id]
    elif filter_type == 'received':
        txns = [t for t in txns if t.receiver_id == current_user.id]
    elif filter_type == 'pending':
        txns = [t for t in txns if t.status == 'pending']

    return render_template('transactions.html', transactions=txns, filter_type=filter_type)

@transactions_bp.route('/api/user-search')
@login_required
def user_search_api():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    from sqlalchemy import or_
    users = User.query.filter(
        or_(User.name.ilike(f'%{q}%'), User.email.ilike(f'%{q}%'), User.username.ilike(f'%{q}%')),
        User.id != current_user.id
    ).limit(5).all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email, 'avatar': u.avatar_initials, 'username': u.username} for u in users])
