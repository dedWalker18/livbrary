from .database import db
from .timestamps import *
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_security import UserMixin, RoleMixin


class user_books(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    time_of_issue = db.Column(db.DateTime, default=datetime.datetime.now())

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('users.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    author = db.Column(db.VARCHAR(100), nullable=False)
    user_books = db.relationship("user_books", backref="books", lazy="joined")
    genre_name = db.Column(db.VARCHAR(255), db.ForeignKey('genre.name'))
    location = db.Column(db.VARCHAR(255), nullable=False)
    cover_photo = db.Column(db.VARCHAR(255), nullable=True)
    notes = relationship('Notes', backref='book')
    
    def repr(self):
        return f'Book(name={self.name}, author={self.author}, genre={self.genre})'
    
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(50), nullable=False, unique=True)
    books = db.relationship("Books", backref="genre", lazy="joined")

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(100), nullable=False)
    username = db.Column(db.VARCHAR(100), unique=True)
    email = db.Column(db.VARCHAR(255), nullable=False)
    password = db.Column(db.VARCHAR(255), nullable =False)
    password_salt = db.Column(db.VARCHAR(255))
    notes = relationship('Notes', backref='user', lazy="joined")
    bookshelf = db.relationship('user_books', backref='user', lazy="joined")
    avatar = db.Column(db.VARCHAR(255))
    last_logged = db.Column(db.DateTime, default=date_today())
    roles = db.relationship('Role', secondary='roles_users',
                            backref='users', lazy='joined')    
    
class Streak(db.Model):
    streak_id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    username = db.Column(db.String, db.ForeignKey(Users.username), nullable=False, unique=True)
    date = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, default=1)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, ForeignKey("books.id"))
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    content = db.Column(db.VARCHAR(255))
    page_number = db.Column(db.Integer)

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    activity = db.Column(db.VARCHAR(255))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return f"<UserActivity user_id: {self.user_id}, activity: {self.activity}>"

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    book_id = db.Column(db.Integer, ForeignKey('books.id'))
    status = db.Column(db.VARCHAR(50))

    def __repr__(self):
        return f"<Request user_id: {self.user_id}, book_id: {self.book_id}, status: {self.status}>"

class Cart(db.Model):
    user_id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)
    book_id = db.Column(db.Integer, ForeignKey('books.id'), primary_key=True)
