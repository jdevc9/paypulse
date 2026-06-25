from flask import Flask
from database import db
from flask_login import LoginManager


login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'paypulse-demo-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paypulse.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from models.user import User
    from models.transaction import Transaction
    from models.contact import Contact

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.transactions import transactions_bp
    from routes.contacts import contacts_bp
    from routes.profile import profile_bp, help_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(help_bp)

    with app.app_context():
        db.create_all()
        seed_data()

    return app


def seed_data():
    from models.user import User, db as _db
    from models.transaction import Transaction
    from models.contact import Contact
    from werkzeug.security import generate_password_hash
    from datetime import datetime, timedelta
    import random

    if User.query.count() > 0:
        return

    rows = [
        ('Joao Paulo',  'joao@demo.com',  'joaopaulo',   5000.0, 'JP'),
        ('Ana Lima',    'ana@demo.com',   'analima',     2500.0, 'AL'),
        ('Bruno Souza', 'bruno@demo.com', 'brunosouza',  1800.5, 'BS'),
        ('Carla Mendes','carla@demo.com', 'carlamendes', 3200.75,'CM'),
        ('Diego Costa', 'diego@demo.com', 'diegocosta',   950.0, 'DC'),
        ('Elena Rocha', 'elena@demo.com', 'elenarocha',  4100.2, 'ER'),
    ]

    users = []
    for name, email, uname, bal, av in rows:
        u = User(name=name, email=email, username=uname,
                 password_hash=generate_password_hash('demo123'),
                 balance=bal, avatar_initials=av)
        db.session.add(u)
        users.append(u)
    db.session.commit()

    for i, u in enumerate(users[:-1]):
        for v in users[i+1:]:
            db.session.add(Contact(user_id=u.id, contact_id=v.id))
            db.session.add(Contact(user_id=v.id, contact_id=u.id))
    db.session.commit()

    descs = ['Almoco','Cinema','Uber','Supermercado','Happy Hour',
             'Divisao conta','Presente','Academia','Netflix','Restaurante']
    for _ in range(40):
        s = random.choice(users)
        r = random.choice([x for x in users if x.id != s.id])
        db.session.add(Transaction(
            sender_id=s.id, receiver_id=r.id,
            amount=round(random.uniform(10, 500), 2),
            description=random.choice(descs), status='completed',
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 90))
        ))
    db.session.commit()
    print('[PayPulse] Demo data seeded OK')


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
