from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from budgetapp import db, login_manager, app
from flask_login import UserMixin

#pylint: disable=E1101

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# MODELS.PY
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transactions', backref="user")

    def get_reset_token(self, expires_sec=300):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}' , '{self.email}' , '{self.date_created}')"

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Text, nullable=False)
    month = db.Column(db.Text, nullable=False)
    year = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    expense = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    input_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Transaction('{self.day}' , '{self.month}' , '{self.year}' , '{self.type}' , '{self.expense}' , '{self.input_date}')"
