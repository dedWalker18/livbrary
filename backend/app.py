from flask import Flask, render_template
# from flask_restful import Api
from application.database import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from application.api import *
from application.celery_tasks import *
from application.graphs import plotGraph
from celery import Celery
from flask_restx import Api, Swagger
import yaml

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livbrary.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['broker_url'] = 'redis://localhost:6379/1'
app.config['result_backend'] = 'redis://localhost:6379/1'
app.config['timezone'] = 'Asia/Kolkata'

app.secret_key = "86bf649c99e24582bd8e4fe8edcbd8b2"
app.config['JWT_SECRET_KEY'] = '432546565744234234436565464234'

app.config['SWAGGER'] = {
    'title': 'Library Management API',
    'description': 'API for managing library resources and user accounts.',
    'version': '1.0.0',
    'uiversion': 3,
    'openapi': '3.0.0'
}

app.config['SWAGGER_URL'] = '/apidocs/'

with app.app_context():
    db.init_app(app)
    db.create_all()


api = Api(app)
CORS(app)
jwt = JWTManager(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],
        broker=app.config['broker_url'],
        timezone=app.config['timezone']
    )
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                print("------------------------")
                print("Starting New Task!!")
                print("------------------------")
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=14, minute=15),
        send_reminder.s(),
        name='send_reminder_daily'
    )
    sender.add_periodic_task(
        crontab(hour="*/3"),
        daily_news.s(),
        name='daily_news_report'
    )
    sender.add_periodic_task(
        crontab(hour=14, minute=35, day_of_month=29),
        monthly_report.s(),
        name='send_reminder_monthly'
    )


with open("openapi3.0_livbrary_docs.yaml", "r") as f:
    swagger_ui_doc = yaml.safe_load(f)

api.doc = swagger_ui_doc

api.add_resource(loginApi, "/loginuser")
api.add_resource(signUpApi, "/signup")
api.add_resource(dashboardApi, "/dashboard")
api.add_resource(usersAll, "/users/all")
api.add_resource(userApi, "/users",
                 "/users/<string:username>")
api.add_resource(userNotes, "/user/notes",
                 "/user/notes/<int:id>")

api.add_resource(booksAll, "/books/all")
api.add_resource(bookApi, "/books/<int:book_id>",
                            "/books")

api.add_resource(genreApi, "/genre")
api.add_resource(genreBooks, "/genre/<string:genre_name>")

api.add_resource(userBooks, "/user/books")
api.add_resource(addRoleApi, "/role/<string:role>")
api.add_resource(requestsApi, "/requests",
                 "/requests/<int:request_id>")
api.add_resource(cartApi, "/cart")
api.add_resource(dueBooks, '/duebooks')
api.add_resource(Analytics, "/analytics/<int:id>")
api.add_resource(Logout, "/logout")
api.add_resource(News, "/news")


@app.route("/")
def main():
    return render_template("apiLandingPage.html")
            

    
if __name__ == '__main__':
    app.run(debug=True)
