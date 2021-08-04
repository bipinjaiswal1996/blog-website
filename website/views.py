from flask import Blueprint, render_template,flash,request,redirect,url_for
from flask_login import login_required,current_user
from .models import Comment, Post, User
from . import db

views=Blueprint("views",__name__)

@views.route("/")
@views.route("/home/")
@login_required
def home():
    posts=Post.query.all()
    return render_template("home.html",user=current_user,posts=posts)

@views.route("/create_post",methods=['GET','POST'])
@login_required
def create_post():
    if request.method=="POST":
        text=request.form['text']
        if not text:
            flash('Post cannot be empty', category="error")
        else:
            post=Post(text=text,author=current_user.id) 
            db.session.add(post)
            db.session.commit()
            flash('Post Created!',category='success')
            return redirect(url_for('views.home'))

    return render_template("create_post.html",user=current_user) 

@views.route('/delete_post/<id>')
@login_required
def delete_post(id):
    post=Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist!",category='error')
    elif (current_user.id!=post.author):
        flash("You do not have permission to delete this post.",category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted Successfully.",category='success')
    return redirect(url_for('views.home'))        

@views.route('/posts/<username>')
@login_required
def view_post(username):
    user=User.query.filter_by(username=username).first()
    if not user:
        flash('User doesn\'t exists!' ,category='error')
        return redirect(url_for('views.home'))
    posts=user.post
    return render_template('posts.html',user=current_user,posts=posts,username=username)


@views.route('/create_comment/<postid>',methods=['POST'])
@login_required
def create_comment(postid):
    comment=request.form['comment']
    if not comment:
        flash('Comment cannot be empty',category='error')
    else:
        post=Post.query.filter_by(id=postid).first()
        if not post:
            flash('Post doesn\'t exists!', category='error')
        else:
            cmt=Comment(text=comment,author=current_user.id, post_id=post.id)
            db.session.add(cmt)
            db.session.commit()    
    return redirect(url_for('views.home'))    


@views.route('/delete_comment/<comm_id>')
@login_required
def delete_comment(comm_id):
    comment=Comment.query.filter_by(id=comm_id).first()
    if not comment:
        flash("Comment does not exist!",category='error')
    elif (current_user.id!=comment.author and comment.post.author!=current_user.id):
        flash("You do not have permission to delete this comment.",category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('views.home'))        
