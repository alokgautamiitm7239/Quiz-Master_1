from flask import Flask
from backend.models import db

app=None
def setup_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///ticket_show.sqlite3"
    db.init_app(app)
    app.app_context().push()
    app.debug=True
    print("Quiz master app is starting.....")

setup_app()


from backend.controller import *

if __name__ == "__main__":
    app.run()