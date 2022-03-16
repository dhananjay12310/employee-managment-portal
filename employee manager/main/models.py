from main import db, login_manager
from main import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return emp_info.query.get(user_id)



class emp_info(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name= db.Column(db.String(length=30), nullable=False)
    last_name= db.Column(db.String(length=30), nullable=False)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    phone = db.Column(db.String(length=10), nullable=False, unique=True)
    dob = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(length=250), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    admin =  db.Column(db.String(), default=False , nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def check_admin(self):
        return self.admin == "True"

    def __repr__(self):
        return f'emp_info {self.email}'