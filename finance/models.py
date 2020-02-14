import datetime
from finance import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True, nullable=False)
    hash = db.Column(db.String(128), nullable=False)
    cash = db.Column(db.Integer, default=10000.00, nullable=False)

    transactions = db.relationship("Transaction", back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    
    # Many to one relationship
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=False)
    user = db.relationship("User", back_populates="transactions")

    company_name = db.Column(db.String(128), index=True)
    company_symbol = db.Column(db.String(128), index=True, nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    trans_type = db.Column(db.String(128), index=True, nullable=False)
    transacted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
