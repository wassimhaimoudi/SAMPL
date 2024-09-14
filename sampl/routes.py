"""This module contains the specific routes for the sampl flask app
"""
import datetime
import secrets
import os
from PIL import Image
from flask import (render_template, url_for, flash,
        redirect, request, abort)
from flask_login import (login_user, current_user,
        logout_user, login_required)
from sampl import app, db, bcrypt, mail, cache, timeout
from sampl.models import User, Lesson, Comment
from sampl.forms import (CommentForm, RegistrationForm, LoginForm,
        UpdateAccountForm)

@app.route("/")
@app.route("/home/")
def home():
    """ Home page route
    """
    return render_template('home.html', title="Home")

@app.route("/about/")
def about():
    """ About page route
    """
    return render_template('about.html', title="About")

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one_or_none()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You have been Logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for("home"))
            flash(f'Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title="Login", form=form)

@app.route("/register/", methods=['GET', 'POST'])
def register():
    """ Registeration route
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
                username=form.username.data,
                email=form.email.data,
                date_of_birth=form.date_of_birth.data,
                password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for("login"))
    return render_template('register.html', title="Register", form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # filename is an attribute of form.picture.data
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/media/images', picture_filename)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename


@app.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    """ Account route
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            new_image_file = save_picture(form.picture.data)
            current_user.image_file = new_image_file # set user's image to a new one
            db.session.commit()
        if User.query.filter(
                User.username == form.new_username.data,
                User.id != current_user.id
                ).first():
            flash('Username already taken. Please choose a diferrent one', "danger")
            return redirect(url_for('account'))
        current_user.username = form.new_username.data
        current_user.email = form.new_email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.new_username.data = current_user.username
        form.new_email.data = current_user.email
    image_file = url_for(
            'static',
            filename='media/images/' + current_user.image_file)
    return render_template(
            'account.html',
            title="Account",
            image_file=image_file,
            form=form)

@app.route("/home/lessons/")
@app.route("/lessons/")
def lessons():
    return render_template(
            "lessons.html",
            title="Introduction to Sound Waves and Oscillators")

@app.route('/home/lessons/quiz/', methods=['GET', 'POST'])
@app.route('/lessons/quiz/', methods=['GET', 'POST'])
def quiz():
    """Quiz route
    """
    if request.method == 'POST':
        total = 3
        score = 0

        if request.form.get('q1') == 'b':
            score += 1
        checked_answers = [
                request.form.get('q2_a'),
                request.form.get('q2_c'),
                request.form.get('q2_e')
                ]
        print(checked_answers) # debgging: print the list of answers
        if all(checked_answers):
            score += 1
        else:
            for answer in checked_answers:
                if answer:
                    score += 0.33
        if request.form.get('q3') == 'b':
            score += 1
        if score > 2 and score < 3:
            flash(f'Your score is {score:.2f}/{total}. Good job!', 'success')
        elif score == 3:
            flash(f'Excelent! You have answered all {score}/{total} questions correctly', 'success')
        else:
            flash(f"Your score is too low. But it's ok, you can catch on and retake the quiz!", 'danger')
        return redirect(url_for('quiz'))
    return render_template('quiz.html', title='Quiz Time')

@login_required
@app.route('/home/lessons/add_comment', methods=['GET', 'POST'])
def add_comments():
    ''' Comments route
    - Make a comments page
    - Make a link in the lessons page for the comments page and make this the route for it
    '''
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added', 'success')
        return redirect(url_for('add_comments'))

    # Queries all the comments available since we only have one lesson for now
    comments = Comment.query.order_by(Comment.id.desc()).all()

    # Corrected User query: Fetch users who have made comments
    users = User.query.join(Comment).filter(Comment.user_id.isnot(None)).all()

    if not comments:
        flash('No comments available', 'info')

    return render_template('comments.html', title='Add Comment', form=form, comments=comments, users=users)


@app.route("/logout", methods=['GET', 'POST'])
@cache.memoize(timeout=timeout)
@login_required
def logout():
    """ Logout route
    """
    if request.method == 'POST':
        logout_user()
        flash("You have been successfully logged out.", "success")
        return redirect(url_for('login'))
    return render_template('logout.html', title="Logout")
