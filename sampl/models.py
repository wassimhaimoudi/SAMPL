from datetime import datetime
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sampl import db, app, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """ Defines a mapped User entity that repesents the user table in the database
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_of_birth = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return f'User("{self.username}, "{self.email}", "{self.image_file}")'
    '''def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token).get('user_id')
        except Exception:
            return None
        return User.query.get(user_id)
        '''

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
"""
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    parent_id = db.Column(db.Integer, ForeignKey('comment.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy="dynamic")
"""

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
"""
    content = db.Column(db.Text, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='lesson', lazy="dynamic")"""
