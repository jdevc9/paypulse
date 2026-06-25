from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.user import User
from models.transaction import Transaction
from sqlalchemy import or_

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def home():
    recent_txns = current_user.get_recent_transactions(8)
    sent_total = sum(t.amount for t in Transaction.query.filter_by(sender_id=current_user.id, status='completed').all())
    received_total = sum(t.amount for t in Transaction.query.filter_by(receiver_id=current_user.id, status='completed').all())

    contacts = [c.contact_user for c in current_user.contacts.limit(5).all()]

    return render_template('dashboard.html',
        transactions=recent_txns,
        sent_total=sent_total,
        received_total=received_total,
        contacts=contacts
    )

@dashboard_bp.route('/search')
@login_required
def search():
    q = request.args.get('q', '').strip()
    results = []
    txn_results = []

    if q:
        results = User.query.filter(
            or_(
                User.name.ilike(f'%{q}%'),
                User.email.ilike(f'%{q}%'),
                User.username.ilike(f'%{q}%')
            ),
            User.id != current_user.id
        ).limit(10).all()

        txn_results = Transaction.query.filter(
            or_(Transaction.sender_id == current_user.id, Transaction.receiver_id == current_user.id),
            Transaction.description.ilike(f'%{q}%')
        ).order_by(Transaction.created_at.desc()).limit(10).all()

    return render_template('search.html', users=results, transactions=txn_results, query=q)

@dashboard_bp.route('/api/quick-stats')
@login_required
def quick_stats():
    txns = current_user.get_all_transactions()
    return jsonify({
        'balance': current_user.balance,
        'total_transactions': len(txns),
        'this_month': len([t for t in txns if t.created_at.month == __import__('datetime').datetime.utcnow().month])
    })
