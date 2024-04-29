from flask_restx import fields

book_resource_fields = {
    'id' : fields.Integer,
    'name': fields.String,
    'author': fields.String,
    'genre_name' : fields.String,
    'location' : fields.String,
    'cover_photo' : fields.String
}

book_resource_fields_view = {
    'id' : fields.Integer,
    'name': fields.String,
    'author': fields.String,
    'genre_name' : fields.String,
    'cover_photo' : fields.String
}

user_book_resource_fields = {
    'id' : fields.Integer,
    'user_id': fields.Integer,
    'book_id': fields.Integer,
    'time_of_issue' : fields.DateTime
}

user_resource_fields = {
    'id' : fields.Integer,
    "name" : fields.String,
    "username" : fields.String,
    "email" : fields.String,
}

notes_resource_fields = {
    "id" : fields.Integer,
    "book_id" : fields.String,
    "content" : fields.String,
    "page_number" : fields.Integer,
}

genre_resource_fields = {
    'id' : fields.Integer,
    "name" : fields.String
}

activity_resource_fields = {
    "id" : fields.Integer,
    "activity" : fields.String,
    "timestamp" : fields.DateTime
}

request_resource_fields = {
    "id" : fields.Integer,
    "book_id" : fields.Integer,
    "user_id" : fields.Integer
}