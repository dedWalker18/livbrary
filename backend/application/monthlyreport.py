from .models import user_books, Streak, UserActivity
import datetime
from .timestamps import *
from .api import load_user
from flask_restx import marshal
from .resourceFields import book_resource_fields, activity_resource_fields
import json

def accountDetails(un):
    account_details = dict()
    account_details["Usersname"] = un
    account_details["Streak"] = Streak.query.filter_by(username=un).first().count
    user = load_user(un)
    bookshelf = user_books.query.filter_by(user_id = user.id).all()
    account_details["No. of Books in Bookshelf"] = len(bookshelf)
    return account_details

def BookDetails(un):
    user = load_user(un)
    fetchedbooks = user_books.query.filter_by(user_id = user.id).all()
    data = marshal([fetchedbook.books for fetchedbook in fetchedbooks],book_resource_fields)
    return data

def activities(un):
    user = load_user(un)
    one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    us_ac = UserActivity.query.filter(
        UserActivity.timestamp >= one_month_ago,
        UserActivity.user_id == user.id
        ).order_by(UserActivity.timestamp.desc()).all() 
    return marshal(us_ac, activity_resource_fields)
    
