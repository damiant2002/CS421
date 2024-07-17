import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["SQLALCHEMY_TRAC_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(120), primary_key=True)
    first = db.Column(db.String(80))
    last = db.Column(db.String(80))
    password = db.Column(db.String(120))

    def __init__(self, first, last, email, password):
        self.first = first
        self.last = last
        self.email = email
        self.password = password


@app.route("/")
def index():
    return render_template("signin.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(email=username).first()

        if user and user.password == password:
            return redirect(url_for("secretPage"))
        else:
            # incorrect username or password just redirects back to itself
            return redirect(url_for("signin"))
    else:  # GET (build and/or method error without this)
        return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first = request.form["first"]
        last = request.form["last"]
        email = request.form["email"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]

        # check if passwords match
        if password != confirmPassword:
            return render_template("signup.html")

        # check if email already exists and display message before SQL throws the Unique error as email is a primary key
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("thankyou.html", existing_user=existing_user)

        new_user = User(first=first, last=last, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("thankyou"))
    else:  # GET
        return render_template("signup.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


@app.route("/secretPage")
def secretPage():
    return render_template("secretPage.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
