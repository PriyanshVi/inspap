from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin,RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db=SQLAlchemy()

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))  


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120),  
 nullable=False)
    type = db.Column(db.String(20),  
 nullable=False)  # 'influencer' or 'brand'
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))  
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    auth_token = db.Column(db.String(255), unique=True, nullable=True)
    
    
    def get_token_from_storage(self):
        return self.auth_token
    def __repr__(self):
        return '<User %r>' % self.username

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User',  
 backref=db.backref('influencer', uselist=False))
    bio = db.Column(db.Text)
    niche = db.Column(db.String(100))
    followers = db.Column(db.Integer)
    profile_image = db.Column(db.String(200))
    date_of_birth = db.Column(db.DateTime)
    facebook_link = db.Column(db.String(200))
    instagram_link = db.Column(db.String(200))
    twitter_link = db.Column(db.String(200))
    youtube_link = db.Column(db.String(200))

    def __repr__(self):
        return '<Influencer %r>' % self.user.username

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User',
                           backref=db.backref('brand', uselist=False))
    name = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(200))
    contact_email = db.Column(db.String(120))
    profile_image = db.Column(db.String(200))
    company_description = db.Column(db.Text)
    industry = db.Column(db.String(100))
    
    
    verified = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<Brand %r>' % self.name

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand',  
                            backref='campaigns')
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    budget = db.Column(db.Float)
    status = db.Column(db.String(50))
    campaign_goals = db.Column(db.Text)
    target_audience = db.Column(db.Text)
    private = db.Column(db.Boolean, default=False)
    proposals = db.relationship('Proposal', backref='campaign', cascade="all, delete-orphan") 


    def __repr__(self):
        return '<Campaign %r>' % self.title

class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)  


    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    influencer = db.relationship('Influencer', backref='proposals')
    status = db.Column(db.String(50))
    proposal_details = db.Column(db.Text)
    bid_amount = db.Column(db.Float)
    proposed_by = db.Column(db.String(50))
    chat_messages = db.relationship('ChatMessage', backref='proposal', cascade="all, delete-orphan")



class Niche(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Niche {self.name}>"


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  

    sender = db.relationship('User', foreign_keys=[sender_id],  
 backref='sent_messages')
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient = db.relationship('User', foreign_keys=[recipient_id],  
 backref='received_messages')
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal.id'), nullable=False)
    #proposal = db.relationship('Proposal', backref='chat_messages')
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<ChatMessage {self.id}>'

