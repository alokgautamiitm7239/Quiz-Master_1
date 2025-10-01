from flask import Flask
from backend.models import db

# Create Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ticket_show.sqlite3"

# Initialize DB
db.init_app(app)
app.app_context().push()

print("Quiz master app is starting.....")

# Import controllers after app is created
from backend.controller import *

# Vercel will look for `app`
if __name__ == "__main__":
    app.run()

