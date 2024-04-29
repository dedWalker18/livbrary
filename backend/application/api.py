from flask_restx import Resource, reqparse, marshal_with, marshal
from flask import session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
import datetime, os
from .sec import user_datastore
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .parsers import *
from .validations import *
from .timestamps import *
from .graphs import plotGraph
from .resourceFields import *

def load_user(username):
    result = abort_if_key_error_users(username)
    return result

def get_bookshelf(userId):
    result = user_books.query.filter_by(user_id=userId).all()
    return result

def DashboardData(un):
    user = load_user(un)
    fetchedbooks = get_bookshelf(user.id)
    fetchednotes = Notes.query.filter_by(user_id = user.id)
    streak = Streak.query.filter_by(username=un).first()
    dashboard = {
        'books' : marshal([fetchedbook.books for fetchedbook in fetchedbooks],book_resource_fields),
        "streak" : streak.count,
        "avatar" : user.avatar,
        "notes" : marshal([Note for Note in fetchednotes], notes_resource_fields)
        }

    return dashboard

class loginApi(Resource):
    def post(self):
        args = login_parse.parse_args()
        un = args.get('username')
        ps = args.get("password")
        user = Users.query.filter_by(username=un).first()
        if user and check_password_hash(user.password, ps):
                session['username'] = un
                user_streak = Streak.query.filter_by(username=un).first()
                if user_streak:
                    today_date = datetime.date.today()
                    last_activity_date = datetime.datetime.strptime(user_streak.date, '%Y-%m-%d').date()
                    date_difference = today_date - last_activity_date
                    if date_difference.days == 1:
                        user_streak.count += 1
                        
                    elif date_difference.days == 0:
                        pass
                    
                    else:
                        user_streak.count = 1
                        
                    user_streak.date = today_date
                    db.session.commit()
                else:
                    pass
                
                access_token = create_access_token(identity=un, expires_delta=datetime.timedelta(hours=6))
                user.last_logged = datetime.datetime.now()
                text = "Logged In On"
                activity = UserActivity(activity=text, timestamp=datetime.datetime.now(), user_id=user.id)
                db.session.add(activity)
                db.session.commit()
                return {"token": access_token, "role": user.roles[0].name}
        else:
            return {"token":"Failed"}

        
class addRoleApi(Resource):
    def post(self, role):
        try:
            role = user_datastore.create_role(name=role)
            db.session.commit()
            return f"{role} added"
        except:
            return f"Error Occured!! The role {role.name} already exists"
        
class signUpApi(Resource):
    def post(self):
        args = users_parse.parse_args()
        nm = args.get('name').lower()
        un = args.get('username').lower()
        ps = args.get("password")
        em = args.get("email")
        rl = args.get('roles')
        avid = args.get("avatarid")
        
        admin_exists = RolesUsers.query.all()
        if (not admin_exists and rl == "admin") or rl == "users":
            if un.strip() == "" or em.strip() == "" or ps.strip() == "":
                return {"message":"Empty Fields Found"}
            elif user_datastore.find_user(username=un) is not None:
                return {"message":"Usernname already taken"}
            else:
                new_streak = Streak(username=un, date=datetime.date.today(), count=1)
                user = user_datastore.create_user(name=nm, 
                                                  username=un, 
                                                  email=em, 
                                                  avatar=avid, 
                                                  password=generate_password_hash(ps)
                                                  )
                role = Role.query.filter_by(name=rl).first()
                user.roles.append(role)
                db.session.add(new_streak)
                db.session.commit()
                return f'User {un} Added Successfully!!'
        else:
            return "Admin Already Exists!!"
        
class dashboardApi(Resource):
    @jwt_required()
    def get(self):
        un = get_jwt_identity()
        result = DashboardData(un)
        return result

class booksAll(Resource):
    def get(self):
        result = Books.query.all()
        return marshal(result, book_resource_fields)
    
class bookApi(Resource):
    @jwt_required()
    def get(self, book_id):
        result = abort_if_key_error_books(book_id)
        user = load_user(get_jwt_identity())
        return marshal(result, book_resource_fields)
                    
    @jwt_required()
    def post(self):
        user = load_user(get_jwt_identity())
        if isAdmin(user):
            args= books_parse.parse_args()
            nm = args.get("name")
            au = args.get("author")
            gnr = args.get("genre")
            lc = args.get("location")
            cv = args.get("cover")
            genre = Genre.query.filter_by(name=gnr).first()
            new_book = Books(name=nm, 
                             author=au, 
                             genre_name=gnr, 
                             location=lc, 
                             cover_photo=cv)
            book_exists = Books.query.filter_by(name=nm).first()
            
            if book_exists:
                return "Book with this name already exists!!"
            elif not genre:
                new_genre = Genre(name=gnr)
                db.session.add(new_genre)
                db.session.add(new_book)
                db.session.commit()
            else:
                db.session.add(new_book)
                db.session.commit()
                return "Book Added Sccessfully!!"
        else:
            return "Only Admin can add Books!!"

    @jwt_required()
    def delete(self, book_id):
        user = load_user(get_jwt_identity())
        if isAdmin(user):
            result = abort_if_key_error_books(book_id)
            revoke_books = user_books.query.filter_by(book_id=book_id).all()
            db.session.delete(result)
            for each_book in revoke_books:
                db.session.delete(each_book)
            db.session.commit()
            return f'Book with Id {book_id} Deleted Successfully'
        else:
            return "Only Admin can delete Books!!"
        
    @jwt_required()
    def patch(self, book_id):
        user = load_user(get_jwt_identity())
        if isAdmin(user):
            args = book_patch.parse_args()
            book = abort_if_key_error_books(book_id)
            name = args["name"]
            author = args["author"]
            genre = args["genre"]
            if name.strip() != "" and name is not None:
                book.name = name
            if author.strip() != "" and author is not None:
                book.author = author
            if genre.strip() != "" and genre is not None:
                genre_exits = Genre.query.filter_by(name=genre).first()
                if genre_exits:
                    book.genre_name = genre
                else:
                    new_genre = Genre(name=genre)
                    db.session.add(new_genre)
                    book.genre_name = genre
            db.session.commit()
            return "Update SuccesFull!!"
        else:
            return 'Unathorized!!!'

class usersAll(Resource):
    @jwt_required()
    def get(self):
        user = load_user(get_jwt_identity())
        if isAdmin(user):
            result = Users.query.all()
            return marshal(result, user_resource_fields)
        else:
            return "Unathorised !!!"
        
class userApi(Resource):
    @jwt_required()
    @marshal_with(user_resource_fields)
    def get(self):
        result = load_user(get_jwt_identity())
        return result
    
    @jwt_required()
    @marshal_with(user_resource_fields)
    def get(self, username):
        result = abort_if_key_error_users(username)
        return result
       
    @jwt_required()
    def patch(self):
        try:
            args = user_patch.parse_args()
            new_name = args.get("name")
            new_avatar = args.get("avatarid")
            new_email = args.get("email")
            user = load_user(get_jwt_identity())
            email = user.email
            if new_name is not None and new_name.strip() != "":
                user.name = new_name
            else:
                user.name = user.name
            if new_email is not None and new_email.strip() != "":
                user.email = new_email
            else:
                user.email = email 
            if new_avatar is not None:
                user.avatar = new_avatar
            else:
                user.avatar = user.avatar
            db.session.commit()
            return "User Details updated Successfully!!"
        except:
            return "Error Occured!!"
        
    @jwt_required()
    def delete(self):
        user = load_user(get_jwt_identity())
        un = user.username
        uid = user.id
        user_streak = Streak.query.filter_by(username=un).first()
        bookshelf = get_bookshelf(uid)
        activity = UserActivity.query.filter_by(user_id=uid).all()
        user_notes = Notes.query.filter_by(user_id=uid).all()
        [db.session.delete(books) for books in bookshelf]
        [db.session.delete(each) for each in activity]
        [db.session.delete(each) for each in user_notes]
        db.session.delete(user_streak)
        db.session.delete(user)
        db.session.commit()
        session['username'] = None
        return f'User {un} Deleted Successfully'
        
class genreApi(Resource):
    @marshal_with(genre_resource_fields)
    def get(self):
        result = Genre.query.all()
        return result

    @jwt_required()
    def post(self):
        user = load_user(get_jwt_identity())
        if isAdmin(user):
            args = genre_parse.parse_args()
            gnr = Genre(name=args["genre_name"])
            genre_exists = Genre.query.filter_by(name=args['genre_name']).first()
            if genre_exists:
                return "Genre Exists"
            db.session.add(gnr)
            db.session.commit()
            return "Genre Added Successfully"
        else:
            return "Only Admin can add Genres!!"
        
    @jwt_required()
    def delete(self):
        user = load_user(get_jwt_identity())
        if isAdmin(user):
            args = genre_parse.parse_args()
            gnr = args["genre_name"]
            result = abort_if_key_error_genres(gnr)
            if not result.books:
                db.session.delete(result)
                db.session.commit()
                return f'Genre {gnr} Deleted Successfully'
            else:
                return f"Remove Books"
        else:
            return "Only Admin can delete Genres!!"
            
class genreBooks(Resource):    
    @marshal_with(book_resource_fields)
    def get(self, genre_name):
        genre = Genre.query.filter_by(name=genre_name).first()
        return genre.books
    
class userBooks(Resource):
    @jwt_required()
    def post(self):
        user = load_user(get_jwt_identity())
        if isAdmin(user):
            par = reqparse.RequestParser()
            par.add_argument("book_id",
                             type=int, 
                             required=True, 
                             help="Book Id Is Required")
            
            par.add_argument("user_id", 
                             type=int, 
                             required=True, 
                             help="User Id Is Required")
            
            args = par.parse_args()
            iss_to_user = args["user_id"]

            bookshelf = get_bookshelf(iss_to_user)
            if len(bookshelf) >= 5:
                requests = Request.query.filter_by(user_id = iss_to_user).all()
                [db.session.delete(request) for request in requests]
                db.session.commit()                
                return "User has 5 books. All their requests are deleted!!"
            
            book = abort_if_key_error_books(args["book_id"])
            book_exists = user_books.query.filter_by(user_id=iss_to_user, 
                                                     book_id=book.id).first()

            if book_exists:
                requests = Request.query.filter_by(user_id = iss_to_user, 
                                                   book_id=book.id).first()
                db.session.delete(requests)
                db.session.commit()
                return "Book Already in user's bookshelf!!"
            
            user_book = user_books(book_id = book.id, user_id= iss_to_user)
            requests = Request.query.filter_by(user_id = iss_to_user, 
                                               book_id=book.id).first()
            db.session.add(user_book)
            db.session.delete(requests)
            db.session.commit()
            return f"Book added to bookshelf succesfully"
        else:
            return "Only Admin can issue books to users!!"
        
class userNotes(Resource):
    @jwt_required()
    @marshal_with(notes_resource_fields)
    def get(self):
        user = load_user(get_jwt_identity())
        ns = Notes.query.filter_by(user_id=user.id).all()
        return ns
    
    @jwt_required()
    @marshal_with(notes_resource_fields)
    def get(self,id):
        user = load_user(get_jwt_identity())
        if type(id) != int:
            return []
        else:
            notes = Notes.query.filter_by(user_id=user.id, 
                                          book_id=id).all()
            return notes

    @jwt_required()
    def delete(self, id):
        if type(id) != int:
            return "Invalid Note Id"
        else:
            notes = Notes.query.filter_by(id=id).first()
            db.session.delete(notes)
            db.session.commit()
            return "Note  Deleted Succesfully!!!"

    @jwt_required()
    def post(self):
        args = notes_parse.parse_args()
        user = load_user(get_jwt_identity())
        if args["content"].strip() == "" or args["pg_number"] <= 0 or not args["book_id"]:
            return "Empty Note"
        else:
            note = Notes(user_id=user.id,
                         content=args["content"], 
                         book_id=args["book_id"],  
                         page_number=args['pg_number']
                         )
            
            db.session.add(note)
            db.session.commit()
            return f"Note added Successfully!!"
    
class requestsApi(Resource):
    @jwt_required()
    def get(self):
        un = load_user(get_jwt_identity())
        if un.roles[0].name != "admin":
            return "Unauthorised for User"
        pending = Request.query.all()
        return marshal(pending, request_resource_fields)
        
    @jwt_required()
    def post(self):
        args = request_parsers.parse_args()
        book_id = args["book_id"]
        user = load_user(get_jwt_identity())
        book = Books.query.filter_by(id= book_id).first()
        name = book.name
        request = Request.query.filter_by(user_id=user.id, 
                                          book_id=book_id).first()
        if request is None:
            bookshelf = get_bookshelf(user.id)
            if len(bookshelf) >= 5:
                return "You got 5 or more books in your bookshelf. Wait some time!!"
            else: 
                new_request = Request(user_id=user.id, 
                                      book_id=book_id)
                db.session.add(new_request)
                text = f'Requested {name}'
                activty = UserActivity(activity= text, 
                                       user_id=user.id, 
                                       timestamp=datetime.datetime.now()
                                       )
                db.session.add(activty)
                db.session.commit()
                return "Await conformation from Admin!!!"
        else:
            return "Book Already Requested. Await Response!!"
    
    @jwt_required()
    def delete(self, request_id):
        un = load_user(get_jwt_identity())
        if un.roles[0].name != "admin":
            return "User Not Authorised!!!"
        else:
            request = Request.query.filter_by(id = request_id).first()
            db.session.delete(request)
            db.session.commit()
            return "Request Revoked!!!"
    
class cartApi(Resource):
    @jwt_required()
    @marshal_with(book_resource_fields)
    def get(self):
        user = load_user(get_jwt_identity())
        cart_items = Cart.query.filter_by(user_id=user.id).all()
        book_ids = [item.book_id for item in cart_items]
        books = [Books.query.filter_by(id=book_id) for book_id in book_ids]
        return books
    
    @jwt_required()
    def post(self):
        args = cart_parsers.parse_args()
        book_id = args["book_id"]
        user = load_user(get_jwt_identity())
        cart_item = Cart(user_id=user.id, book_id=book_id)
        db.session.add(cart_item)
        db.session.commit()
        return "Book Added to Cart Successfully"

class dueBooks(Resource):
    @jwt_required()
    def get(self):
        user = load_user(get_jwt_identity())
        if user.roles[0].name != "admin":
            return {'message': 'Unauthorized access'}
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        
        ## using greater than to show some books as all books are new
        issued_books = [user_books.query.filter(user_books.time_of_issue > seven_days_ago).all()] 
        return marshal(issued_books[0], user_book_resource_fields)
    
    @jwt_required()
    def delete(self):
        user = load_user(get_jwt_identity())
        if isAdmin(user):
            seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
            
            ## using greater than to show some books as all books are new
            issued_books = [user_books.query.filter(user_books.time_of_issue > seven_days_ago).all()]
            for book in issued_books[0]:
                db.session.delete(book)
            db.session.commit()
            return "Return Succesfull!!"
    
        elif user.roles[0].name == "users":
            parser = reqparse.RequestParser()
            parser.add_argument("bookId", 
                                type=str, 
                                required=True, 
                                help="Book Id Required")
            
            args = parser.parse_args()
            user_book = user_books.query.filter_by(user_id=user.id, 
                                                   book_id=args['bookId']
                                                   ).first()
            db.session.delete(user_book)
            book = abort_if_key_error_books(args["bookId"])
            name = book.name
            text = f"Returned Book {name}"
            activty = UserActivity(activity=text, 
                                   user_id=user.id, 
                                   timestamp=datetime.datetime.now()
                                   )
            db.session.add(activty)
            db.session.commit()
            return "Return Successfull"
        
        else:
            return "Invalid Role. Umathorised !!!"
        
class Analytics(Resource):
    def get(self,id):
        image_paths = plotGraph()
        if image_paths != "NOBOOKS":
            return send_file(image_paths[id], mimetype='image/png')
        return "No User has any book issued currently"
    
class News(Resource):
    def get(self):
        today = date_today().strftime("%Y-%m-%d")
        for filename in os.listdir("templates/rendered_examples"):
            if filename.endswith(today + ".pdf"):
                pdf_path = os.path.join("templates/rendered_examples", filename)
                return send_file(pdf_path, mimetype="application/pdf")
        
        return "Some Error Occured!!"
    
class Logout(Resource):
    @jwt_required()
    def get(self):
        if "username" in session:
            session.pop("username", None)
            return "Logout Succesfull"
        return "OK"