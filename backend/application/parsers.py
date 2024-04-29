from flask_restx import reqparse

books_parse = reqparse.RequestParser()
books_parse.add_argument("name", type=str, required=True, help="name of the book required")
books_parse.add_argument("author", type=str, required=True, help="author of the book required")
books_parse.add_argument("genre", type=str, required=True, help="genre of the book required")
books_parse.add_argument("location", type=str, required=True, help="location of the book required")
books_parse.add_argument("cover", type=str, required=True, help="cover location of the book required")

book_patch = reqparse.RequestParser()
book_patch.add_argument("name", type=str, required=False, help="name of the book optional")
book_patch.add_argument("author", type=str, required=False, help="autjor of the book optional")
book_patch.add_argument("genre", type=str, required=False, help="genre of the book optional")

users_parse = reqparse.RequestParser()
users_parse.add_argument("name", type=str, required=True, help="name of the user required")
users_parse.add_argument("username", type=str, required=True, help="name of the user required")
users_parse.add_argument("email", type=str, required=True, help="email of the user required")
users_parse.add_argument("password", type=str, required=True, help="password of the user required")
users_parse.add_argument("roles", type=str, required=True, help="role required")
users_parse.add_argument("avatarid", type=str, required=False, help="avatar id of the user optional")

user_patch = reqparse.RequestParser()
user_patch.add_argument("name", type=str, required=False)
user_patch.add_argument("email", type=str, required=False)
user_patch.add_argument("avatarid", type=str, required=False)

login_parse = reqparse.RequestParser()
login_parse.add_argument("username", type=str, required=True, help="name of the user required")
login_parse.add_argument("password", type=str, required=True, help="password required")

genre_parse = reqparse.RequestParser()
genre_parse.add_argument("genre_name", type=str, required=True, help="name of the genre required")

role_parse = reqparse.RequestParser()
role_parse.add_argument("name", type=str, required=True, help="name of the role required")

notes_parse = reqparse.RequestParser()
notes_parse.add_argument("content", type=str, required=True, help="Content Required")
notes_parse.add_argument("pg_number", type=int, required=True, help="Page Number Required")
notes_parse.add_argument("book_id", type=int, required=True, help="book id required")

request_parsers = reqparse.RequestParser()
request_parsers.add_argument('book_id', type=int, required=True, help="book id required" )
request_parsers.add_argument('request_id', type=int, required=False)

cart_parsers = reqparse.RequestParser()
cart_parsers.add_argument('book_id', type=int, required=True, help="Book Id required")
