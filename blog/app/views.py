# -*- coding:utf-8 -*-

import datetime
import HTMLParser
from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask_login import logout_user, login_user, current_user, login_required
from app import forms
from forms import SignUpForm, LoginForm, BlogForm, AboutMeForm
from models import User, Blog
from app import app, db, lm


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.login_check(request.form.get('UserEmail'), request.form.get('PassWord'))
        if user:
            login_user(user)
            return redirect(url_for('userpage', page_id=current_user.id))
        else:
            flash(u'账号错误或者密码错误', 'flash-message lime')
            return redirect('/login')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    user = User()
    if form.validate_on_submit():
        useremail = request.form.get('UserEmail')
        username = request.form.get('UserName')
        password = request.form.get('PassWord')
        checkUser = User.query.filter(db.or_(User.username == username, User.email == useremail)).first()
        if checkUser:
            flash(u'该账号或昵称已经存在', 'flash-message lime')
            redirect('/signup')
        user.email = useremail
        user.password = password
        user.username = username
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash(u'数据库异常', 'flash-message lime')
            return redirect('/signup')
        else:
            flash(u'注册成功', 'flash-message green')
            return redirect('/login')

    return render_template('signup.html', form=form)


@app.route('/write/<int:user_id>', methods=['POST', 'GET'])
@login_required
def write(user_id):
    blogs = Blog()
    print request.form.get('BlogTitle')
    if request.form.get('BlogTitle') and request.form.get('BlogContent'):
        blogs.blogtitle = request.form.get('BlogTitle')
        blogs.blogcontent = request.form.get('BlogContent')
        blogs.author_name = current_user.username
        blogs.timestamp = datetime.datetime.now()
        try:
            db.session.add(blogs)
            db.session.commit()
        except:
            flash(u'数据库异常', 'flash-message lime')
            redirect(url_for('write', user_id=user_id))
        flash(u'发表成功', 'flash-message green')
        redirect(url_for('write', user_id=user_id))
    print url_for('write', user_id=user_id)
    return render_template('write.html')


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def users(user_id):
    form = AboutMeForm()
    if user_id != current_user.id:
        redirect('url_for')
    return render_template('user.html')


@app.route('/userpage/<int:page_id>')
def userpage(page_id):
    user = User.query.filter(User.id == page_id).first()
    if user is None:
        abort(404)
    blogs = user.blogs.order_by(Blog.timestamp.desc()).all()
    return render_template('userpage.html', user=user, blogs=blogs)


@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    blogcontent = Blog.query.get_or_404(blog_id)
    return render_template('blog.html', blog=blogcontent)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", http=404), 404


@app.errorhandler(401)
def page_not_found(e):
    return render_template('404.html', http=401), 401

