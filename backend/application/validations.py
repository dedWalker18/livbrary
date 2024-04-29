from application.models import Books, Users, Genre
from flask_restx import abort

def abort_if_key_error_books(book_id):
    result = Books.query.filter_by(id=book_id).first()    
    if not result:
        abort(422, message="Book Id is Invalid")
    else:
        return result    
    
def abort_if_key_error_users(username):
    result = Users.query.filter_by(username=username).first()    
    if not result:
        abort(422, message="User is Invalid!!")
    else:
        return result    
    
def abort_if_key_error_genres(genre_name):
    result = Genre.query.filter_by(name=genre_name).first()    
    if not result:
        abort(422, message="Genre is Invalid")
    else:
        return result    

def isAdmin(user):
    if user.roles[0].name == "admin":
        return True
    return False