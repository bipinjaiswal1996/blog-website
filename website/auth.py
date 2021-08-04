from flask import Blueprint, render_template,redirect,url_for,request
from flask.helpers import flash
from . import db
from .models import User
from flask_login import login_user, logout_user,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash

auth=Blueprint("auth",__name__)

@auth.route("/login/",methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        email=request.form['email']
        passwd=request.form['passwd']
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,passwd):
                flash('Logged In!',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong Password!',category='error')
        else:
            flash('Email does not exist!',category='error')            

    return render_template("login.html",user=current_user)

@auth.route("/sign_up/",methods=['GET','POST'])
def sign_up():
    if(request.method=="POST"):
        email=request.form['email']
        username=request.form['username']
        passwd1=request.form['passwd1']
        passwd2=request.form['passwd2']
        email_exists=User.query.filter_by(email=email).first()
        user=User.query.filter_by(username=username).first()
        if(email_exists):
            flash('Email already in use.',category='error')
        elif(user):
            flash('Username already in use.',category='error')
        elif(passwd1!=passwd2):
            flash('Password don\'t match',category='error')
        else:
            new_user=User(email=email,username=username,password=generate_password_hash(passwd1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User Created')
            login_user(new_user,remember=True)
            return redirect(url_for('views.home'))    
    return render_template("sign_up.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out!',category='success')
    return redirect(url_for('views.home'))
