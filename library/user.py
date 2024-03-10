from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import *

user = Blueprint("user", __name__)

@user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                session.permanent = True
                login_user(user, remember=True)
                flash("Logged in success!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Wrong password, please check again!", category="error")
        else:
            flash("User doesn't exist", category="error")
            
    return render_template("login.html", user=current_user)

@user.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.filter_by(email=email).first()
        
        if user:
            flash("User existed!", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        else:
            STR_ERROR_PASS = """
                A weak password needs to enter 
                more than 7 characters including: 
                uppercase letters, lowercase letters, 
                numbers and special characters.
            """

            def validate_password(password):
                if len(password) < 8:
                    return False
                
                is_digit = False
                is_upper_character = False
                is_lower_character = False
                is_special_character = False

                for c in password:
                    is_digit |= ('0' <= c <= '9')
                    is_upper_character |= ('A' <= c <= 'Z')
                    is_lower_character |= ('a' <= c <= 'z')
                    is_special_character |= not (('0' <= c <= '9') or ('A' <= c <= 'Z') or ('a' <= c <= 'z'))
                
                print(is_digit, is_upper_character, is_lower_character, is_special_character)
                
                return is_digit and is_upper_character and is_lower_character and is_special_character
            
            if not validate_password(password):
                flash(STR_ERROR_PASS, category="error")
            elif password != confirm_password:
                flash("Enter wrong password!", category="error")
            else:
                password = generate_password_hash(password, method="sha256")
                new_user = User(email, password, user_name)
                password = generate_password_hash(password, method="sha256")
                new_user = User(email, password, user_name)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash("User created!", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("views.home"))
                except:
                    "Error when create user!"
            
    return render_template("signup.html", user=current_user)

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))