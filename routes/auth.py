from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    return render_template('landing.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=request.form.get('remember'))
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.home'))
        flash('Email ou senha incorretos.', 'error')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not all([name, email, username, password]):
            flash('Preencha todos os campos.', 'error')
            return render_template('register.html')
        if password != confirm:
            flash('As senhas não coincidem.', 'error')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Este email já está em uso.', 'error')
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash('Este username já está em uso.', 'error')
            return render_template('register.html')

        initials = ''.join([n[0].upper() for n in name.split()[:2]])
        user = User(
            name=name,
            email=email,
            username=username,
            password_hash=generate_password_hash(password),
            balance=1000.00,
            avatar_initials=initials
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Conta criada com sucesso! Você recebeu R$ 1.000,00 de bônus de boas-vindas. 🎉', 'success')
        return redirect(url_for('dashboard.home'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))
