from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_app import db, login_manager
from flask_login import UserMixin



# boiler plate for login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    # All the children relationships to the user
    about_post = db.relationship('About_Post', backref='author', lazy=True)
    blog_posts = db.relationship('Blog_Post', backref='author', lazy=True)
    portfolio_posts = db.relationship('Portfolio_Post', backref="author", lazy=True)
    home_post = db.relationship('Home_Post', backref='author', lazy=True)
    gallery_posts = db.relationship('Gallery_Post', backref='author', lazy=True)

# GETTING RESET TOKEN

    # get locked out? password reset?
    def get_reset_token(self, expires_sec=1800):
        # THIS MIGHT NEED TO BE CHANGED TO LOCAL VARIABLE IF IT DOESN'T WORK
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id' : self.id}).decode('utf-8')

    # verifying the token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Home_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False, default="Home")
    content = db.Column(db.Text, nullable=False, default="mi bezonas suoj")
    main_photo = db.Column(db.String(30), nullable=False, default="default.jpg")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Home_Post('{self.title}', '{self.content}')"

class About_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False, default="About")
    content = db.Column(db.Text, nullable=False, default="mi bezonas suoj")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"About_Post('{self.title}', '{self.content}')"

class Blog_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Blog_Post('{self.title}', '{self.date_posted}')"

class Portfolio_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=True)
    portfolio_picture = db.Column(db.String(30), nullable=False, default="default.jpg")
    content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Portfolio_Post('{self.title}', '{self.portfolio_picture}', '{self.date_posted}')"


class Customer_Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.String(12), unique=False, nullable=True)
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Customer_Message('{self.name}', '{self.email}','{self.phone}',\nUTC-{self.date_sent}\n'{self.message}')"



class Gallery_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=True)
    gallery_picture = db.Column(db.String(30), nullable=False, default="default.jpg")
    content = db.Column(db.Text, nullable=True)
    price = db.Column(db.String(30), default="Email for info")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Portfolio_Post('{self.title}', '{self.portfolio_picture}', '{self.date_posted}')"
