from flask import Flask, render_template, redirect, url_for, request, flash
import smtplib
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///portfolio.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# MY_GMAIl_DETAILS
MY_GMAIl_ID = "mearshadaman@gmail.com" 
MY_GMAIl_PASSOWRD = "ek baar baap bol" 

#Making User Table
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(250), nullable = False, unique=True)
    password = db.Column(db.String(250), nullable = False)
db.create_all()


# Making Project
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pname = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(250), nullable=False)
    technology = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)
db.create_all()



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=['GET','POST'])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["msg"]

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_GMAIl_ID, MY_GMAIl_PASSOWRD)
            connection.sendmail(from_addr=MY_GMAIl_ID, to_addrs="arshadaman202@gmail.com", msg=f"Subject:Mail from {name}!\n\nEmail:{email}\nPhone:{phone}\nHere is message: {message}")
        return f'<h1 style="text-align:center;">Thank You for your message. I will reach back to you ASAP</h1>'

    return render_template("contact.html")


@app.route("/project", methods=["GET","POST"])
def project():
    all_projects = Projects.query.order_by(Projects.id).all()

    return render_template("project.html", projects=all_projects)
    


@app.route("/delete")
def delete():
    project_id = request.args.get("id")
    project = Projects.query.get(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('project'))

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        project_name = request.form["pname"]
        description = request.form["desc"]
        technology = request.form["tech"]
        image_url = request.form["img_url"]

        # Adding to database
        new_project = Projects(
            pname = project_name,
            description = description,
            technology = technology,
            img_url = image_url,
        )
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for("project"))
    return render_template("add.html")

@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if Users.query.filter_by(email=email).first():
            #Send flash messsage
            flash("You've already signed up with that email, log in instead!")
            #Redirect to /login route.
            return redirect(url_for('login'))
        hash_and_salted_password = generate_password_hash(
            password,
            method= 'pbkdf2:sha256',
            salt_length= 8
        )

        new_user = Users(
            email = email,
            password = hash_and_salted_password,

        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for("home"))
    return render_template("register.html",current_user=current_user)


@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email_login = request.form["email_login"]
        password_login = request.form["password_login"]

        user = Users.query.filter_by(email= email_login).first()

        if not user:
            flash("That email does not exit")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password_login):
            flash("Password incorrect")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)