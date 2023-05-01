from app.app import db
from flask_login import UserMixin
from datetime import datetime
import base64


class Post(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(100))
    caption = db.Column(db.String(100))
    imgpath  = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    no_of_likes = db.Column(db.Integer , default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    post_likes = db.relationship('Likes' , backref='Post', lazy='subquery')
    comments = db.relationship('Comments' , backref='Post', lazy='subquery')
    def __repr__(self):
        return str(self.id) + ' - ' + str(self.title)
    def save(self):
        db.session.add( self )
        db.session.commit()
        return self
    def get_by_id(self, id):
        return Post.query.filter_by(id=id).first()
    def to_json(self):
        json_user = {
            'id': self.id,
            'title': self.title,
            'caption': self.caption,
            'imgpath': self.imgpath,
            'timestamp': self.timestamp,
            'no_of_likes': self.no_of_likes,
            # 'user_id': self.user_id,
        }
        return json_user
    

    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return   str(self.follower_id) + ' - ' + str(self.followed_id)
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
    def to_json(self):
        following = User.query.filter_by(id=self.followed_id).first()
        follower = User.query.filter_by(id=self.follower_id).first()
        json_follow = {
            'follower_id': self.follower_id,
            'followed_id': self.followed_id,
            'timestamp': self.timestamp,
            'follower': follower.user,
            'following': following.user
        }
        return json_follow
class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(64),unique = True)
    email = db.Column(db.String(120),unique = True)
    password = db.Column(db.String(500))
    last_seen = db.Column(db.DateTime , default=datetime.now)
    email_verified = db.Column(db.Boolean, default=False)
    Profile = db.relationship('Profile' , backref='User', lazy='subquery' , uselist=False)
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='subquery'),
                               lazy='subquery',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                              foreign_keys=[Follow.followed_id],
                              backref=db.backref('followed', lazy='subquery'),
                              lazy='subquery',
                              cascade='all, delete-orphan')
    def get_by_id(self, id):
        return User.query.filter_by(id=id).first()
    def get_by_username(self, username):
        return User.query.filter_by(user=username).first()
    def get_all(self):
        return User.query.all()
    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user)
    def save(self):   
        db.session.add( self )
        db.session.commit()
        return self 
    def to_json(self):
        json_user = {
            'id': self.id,
        'user': self.user,
            'email': self.email,
            'last_seen': self.last_seen,
            'email_verified': self.email_verified,
        }
        return json_user
    def from_json(self, json_user):
        self.user = json_user.get('user')
        self.email = json_user.get('email')
        self.password = json_user.get('password')
        self.last_seen = datetime.now()
        return self
    def verify_password(self, password):
        return self.password == password
    
    def login(self, username, password):
        user = User.query.filter_by(user=username).first()
        if user and user.verify_password(password):
            user.last_seen = datetime.now()
            user.save()
            return user.to_json()
        return None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
    def update(self):
        db.session.commit()
        return self


class Profile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True , nullable=False)
    no_of_posts = db.Column(db.Integer)
    no_of_followers = db.Column(db.Integer)
    no_of_following = db.Column(db.Integer)
    image  = db.Column(db.BLOB)
    report_type = db.Column(db.String(100) , default='html')
    post = db.relationship('Post' , backref='Profile', lazy='subquery')
    post_likes = db.relationship('Likes' , backref='Profile', lazy='subquery')
    comments = db.relationship('Comments' , backref='Profile', lazy='subquery')
    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user_id)
    def save(self):   
        db.session.add( self )
        db.session.commit()
        return self
    def image_to_base64(self):
        return base64.b64encode(self.image).decode('utf-8')

    def to_json(self):
        json_user = {
            'user_id': self.user_id,
            'no_of_posts': self.no_of_posts,
            'no_of_followers': self.no_of_followers,
            'no_of_following': self.no_of_following,
            'report_type': self.report_type
        }
        return json_user
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
    def get_by_id(id):
        return Profile.query.filter_by(id=id).first()
    def update(self):
        db.session.commit()
        return self


class Likes(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id') , nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return str(self.id) + ' - ' + str(self.post_id) + ' - ' + str(self.user_id)
    def to_json(self):
        user = User.query.filter_by(id=self.user_id).first()
        json_user = {
            'id': self.id,
            'post_id': self.post_id,
            'username':user.user,
            'user_id': self.user_id,
            'timestamp': self.timestamp,
        }
        return json_user
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
class Comments(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    comment = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return str(self.id) + ' - ' + str(self.post_id) + ' - ' + str(self.user_id) + ' - ' + str(self.comment)
    def to_json(self):
        user = User.query.filter_by(id=self.user_id).first()
        json_user = {
            'id': self.id,
            'post_id': self.post_id,
            'username':user.user,
            'user_id': self.user_id,
            'comment': self.comment,
            'timestamp': self.timestamp,
        }
        return json_user
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
    def save(self):
        db.session.add(self)
        db.session.commit()