from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

app = Flask(__name__)

db = SQLAlchemy()
bcrypt = Bcrypt(app)

class User(db.Model, UserMixin):
  __tablename__ = 'members'
  id = db.Column(db.Integer(), primary_key=True)
  unique_id = db.Column(db.Integer(), nullable=False, unique=True)
  first_name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String(30), nullable=False)
  age = db.Column(db.Integer(), nullable=False)
  phone_number = db.Column(db.String(10), nullable=False)
  email = db.Column(db.String(50), nullable=False)
  password = db.Column(db.String(100), nullable=False)
  vote= db.relationship("Vote", backref="my-vote", lazy=True)

  @property
  def passwords(self):
    return self.passwords

  @passwords.setter
  def passwords(self, plain_text_password):
    self.password = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password, attempted_password)

class Election(db.Model):
  __tablename__ = 'election'
  id = db.Column(db.Integer(), primary_key=True)
  election_id = db.Column(db.Integer(), unique=True, nullable=False)
  start_date = db.Column(db.DateTime(), nullable=False)
  end_date = db.Column(db.DateTime(), nullable=False)
  status = db.Column(db.String(10), nullable=False)
  candidates = db.relationship("Candidates", backref="candidates", lazy=True)
  votes = db.relationship("Vote", backref="all-votes", lazy=True)

class Candidates(db.Model):
  __tablename__ = 'candidates'
  id = db.Column(db.Integer(), primary_key=True)
  candidate_id = db.Column(db.Integer(), unique=True, nullable=False)
  full_name = db.Column(db.String(60), nullable=False)
  party = db.Column(db.String(40), nullable=False)
  election = db.Column(db.Integer(), db.ForeignKey('election.id'))
  votes = db.relationship("Vote", backref="my-votes", lazy=True)

class Vote(db.Model):
  __tablename__ = 'vote'
  id = db.Column(db.Integer(), primary_key=True)
  vote_id = db.Column(db.Integer(), unique=True, nullable=False)
  private_key = db.Column(db.String(15), nullable=False, unique=True)
  public_key = db.Column(db.String(15), nullable=False, unique=True)
  date = db.Column(db.DateTime(), nullable=False)
  candidate = db.Column(db.Integer(), db.ForeignKey('candidates.id'))
  election = db.Column(db.Integer(), db.ForeignKey('election.id'))
  user = db.Column(db.Integer(), db.ForeignKey('members.id'))
