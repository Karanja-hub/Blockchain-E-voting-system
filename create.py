from flask import Flask
from models import *
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)

def main():
  db.create_all()

def candidate():
  new_candidate=Candidates(
    candidate_id=random.randint(100000,999999),
    full_name="HACHEN",
    party= "INDEPENDENT CANDIDATE"
  )
  db.session.add(new_candidate)
  db.session.commit()

if __name__ == '__main__':
  with app.app_context():
    # main()
    candidate()
