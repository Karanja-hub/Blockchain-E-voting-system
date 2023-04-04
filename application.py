from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_login import current_user, login_required, login_manager, LoginManager, login_user, logout_user
import random, datetime, os, string, json
from datetime import date, timedelta
from models import *
from form import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] ="hachenovour"

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = '/user-authentication'
login_manager.login_message_category = "danger"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  try:
    return User.query.filter_by(id=user_id).first()
  except:
    flash(f"Failed to login the user", category="danger")

@app.route("/user-registration", methods=["POST", "GET"])
def registration():
  form = Registration()
  if form.validate_on_submit():
    new_member = User(
      unique_id = random.randint(10000000, 99999999),
      first_name = form.first_name.data,
      last_name = form.last_name.data,
      age = form.age.data,
      phone_number = form.phone_number.data,
      email = form.email_address.data,
      passwords = form.password.data
    )
    db.session.add(new_member)
    db.session.commit()
    flash(f"Registration successfull", category="success")
    return redirect(url_for('login'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")
    return redirect(url_for('registration'))

  return render_template("register.html", form=form)

@app.route("/user-authentication", methods=["POST", "GET"])
def login():
  form = Login()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email_address.data).first()
    if user and user.check_password_correction(attempted_password=form.password.data):
      login_user(user, remember=True)
      flash(f"Login successfull", category="success")
      next = request.args.get("next")
      return redirect(next or url_for('home'))
    elif user is None:
      flash(f"No user with that email address", category="danger")
      return redirect(url_for('login'))
    else:
      flash(f"Invalid credentials", category="danger")
      return redirect(url_for('login'))

  return render_template("login.html", form=form)

@app.route("/logout")
def logout():
  logout_user()
  flash(f"Logout successfull", category="success")
  return redirect(url_for('login'))

@app.route("/")
@app.route("/home")
def home():
  election = Election.query.filter_by(status="Active").first()
  if current_user.is_authenticated:
    if election:
      if election.end_date < datetime.datetime.now():
        election.status = "Closed"
        db.session.commit()
      voted_users = []
      votes = Vote.query.filter_by(election=election.id).all()
      for vote in votes:
        voted_users.append(vote.user)
      if current_user.id not in voted_users:
        flash(f"You have an active election that requires your vote #yourvotecounts", category="info")
        return redirect(url_for('generate_key'))

  return render_template("home.html", election=election)

@app.route("/preparing-election")
@login_required
def preparing_election():
  return render_template("animate.html"), {"Refresh": f"15; url=http://127.0.0.1:5000/generating-key"}

@app.route("/generating-key", methods=["POST", "GET"])
@login_required
def generate_key():
  form = Verification()
  if request.method == "GET":
    secret_key = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    session["secret_key"] = secret_key
    flash(f"your secret key is {secret_key}",category="info")
    return render_template("verify.html", form=form)
  if request.method == "POST":
    if form.validate_on_submit():
      user_secret_key = form.secret_key.data
      secret_key = session["secret_key"]
      print(secret_key, user_secret_key)
      if user_secret_key == secret_key:
        flash(f"Your identity has been verified successfully", category="success")
        session.pop("secret_key", None)
        return redirect(url_for('setting_election'))
      else:
        flash(f"Identity verification process has failed. Try again", category="danger")
        return redirect(url_for('home'))

@app.route("/setting-election")
@login_required
def setting_election():
  candidates = Candidates.query.all()
  election = Election.query.filter_by(status="Active").first()
  if election:
    flash(f"There's another election ongoing", category="info")
    return redirect(url_for('election', election_id=election.id))
  new_election = Election(
    election_id = random.randint(10000000,99999999),
    start_date = datetime.datetime.now(),
    end_date = datetime.datetime.now() + timedelta(days=1),
    status = "Active"
  )
  db.session.add(new_election)
  db.session.commit()
  selected_candidates = []
  random_candidates = random.sample(candidates, 3)
  selected_candidates.extend(random_candidates)
  for candidates in selected_candidates:
    candidates.election = new_election.id
    db.session.commit()
  
  return redirect(url_for('election', election_id=new_election.id))

@app.route("/election-time/<int:election_id>")
@login_required
def election(election_id):
  try:
    election = Election.query.get(election_id)
    votes = Vote.query.filter_by(election=election.id).all()
    if current_user.vote and current_user.vote[-1] in votes:
      flash(f"You have already casted your vote", category="danger")
      return redirect(url_for('home'))
    candidates = Candidates.query.filter_by(election=election.id).all()
  except:
    flash(f"Invalid URL", category="danger")
    return redirect(url_for('home'))
  
  return render_template("election.html", candidates=candidates, election=election)

@app.route("/my-vote/<int:election_id>", methods=["POST", "GET"])
def vote(election_id):
  if request.method == "GET":
    flash(f"Invalid URL", category="danger")
    return redirect(url_for('home'))
  try:
    json_data = request.get_json()
    candidate_id = json.loads(json_data)
    election = Election.query.get(election_id)
    votes = Vote.query.filter_by(election=election.id).all()
    my_vote = Vote(
      vote_id = random.randint(10000000,99999999),
      private_key = "".join(random.choices(string.ascii_uppercase + string.digits, k=15)),
      public_key = "".join(random.choices(string.ascii_uppercase + string.digits, k=15)),
      date = datetime.datetime.now(),
      candidate = candidate_id,
      election = election.id,
      user = current_user.id
    )
    db.session.add(my_vote)
    db.session.commit()
    flash(f"Your vote has been recorded, thankyou for participating", category="success")
    return redirect(url_for('vote_casted', election_id=election.id))
  except:
    flash(f"Invalid URL", category="danger")
    return redirect(url_for('home'))

@app.route("/vote-casted/<int:election_id>")
def vote_casted(election_id):
  try:
    election = Election.query.get(election_id)
    vote = Vote.query.filter_by(election=election.id, user=current_user.id).first()
  except:
    flash(f"Invalid URL", category="danger")
    return redirect(url_for('home'))

  return render_template("vote.html"), {"Refresh": f"6; url=http://127.0.0.1:5000/home"}

@app.route("/private-key/<int:election_id>", methods=["POST", "GET"])
def private_key(election_id):
  try:
    form = I_voted()
    election = Election.query.get(election_id)
    vote = Vote.query.filter_by(election=election.id, user=current_user.id).first()
    if form.validate_on_submit():
      user_private_key = form.private_key.data
      if user_private_key == vote.private_key:
        flash(f"We've sent you a secret key in your email address", category="success")
        secret_key = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        session["secret_key_result"] = secret_key
        return redirect(url_for('i_voted', election_id=election.id))
      else:
        flash(f"Invalid private key", category="danger")
        return redirect(url_for('private_key', election_id=election.id))
  except:
    flash(f"Invalid URL", category="danger")
    return redirect(url_for('home'))
    
  return render_template("i-voted.html",form=form)

@app.route("/my-vote-results/<int:election_id>", methods=["POST", "GET"])
def i_voted(election_id):
  try:
    form1 = Verification()
    election = Election.query.get(election_id)
    vote = Vote.query.filter_by(election=election.id, user=current_user.id).first()
    candidate = Candidates.query.filter_by(id=vote.candidate).first()
    if form1.validate_on_submit():
      user_secret_key = form1.secret_key.data
      secret_key = session["secret_key_result"]
      if user_secret_key == secret_key:
        flash(f"We've sent you your election vote result in your email address", category="success")
        session.pop("secret_key_result", None)
        return redirect(url_for('home'))
      else:
        session.pop("secret_key_result", None)
        flash(f"Invalid secret key", category="danger")
        return redirect(url_for('private_key', election_id=election.id))
  except:
    flash(f"Invalid URL", category="danger")
    return redirect(url_for('home'))
    
  return render_template("i-voted.html",form1=form1)

if __name__ == '__main__':
  app.run(debug=True)
