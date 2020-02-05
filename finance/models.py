from finance import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True, nullable=False)
    hash = db.Column(db.String(128), nullable=False)
    cash = db.Column(db.Integer, default=5000.00, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)
