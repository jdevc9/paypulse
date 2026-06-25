from database import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), default='')
    status = db.Column(db.String(20), default='completed')  # pending, completed, failed
    transaction_id = db.Column(db.String(36), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        import uuid
        super().__init__(**kwargs)
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4())[:8].upper()

    @property
    def formatted_amount(self):
        return f'R$ {self.amount:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    @property
    def formatted_date(self):
        return self.created_at.strftime('%d/%m/%Y %H:%M')

