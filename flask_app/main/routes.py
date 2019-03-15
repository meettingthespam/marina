from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_mail import Message
from flask_app import db, bcrypt, mail, googlemap
from flask_googlemaps import Map, icons
from flask_app.main.forms import HomePageForm, CustomerMessageForm, AboutPageForm
from flask_app.main.utils import save_home_photo
from flask_app.models import (User, Blog_Post,
                            Home_Post, About_Post,
                            Portfolio_Post, Gallery_Post,
                            Customer_Message)

from flask_login import current_user, login_required

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/")
@main_bp.route("/home")
def home():
    post = Home_Post.query.order_by(Home_Post.date_posted.desc()).first()
    return render_template('home.html', post=post)


@main_bp.route("/home/edit", methods=['GET', 'POST'])
@login_required
def update_home_page():
    post = Home_Post.query.order_by(Home_Post.date_posted.desc()).first()
    form = HomePageForm()
    if form.validate_on_submit():
        main_photo_saved = save_home_photo(form.main_photo.data)
        post = Home_Post(title=form.title.data,
                            content= form.content.data,
                            main_photo=main_photo_saved,
                            author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Home Page has been updated', 'success')
        return redirect(url_for('main_bp.home'))
    elif request.method == 'GET':
        if post:
            form.title.data = post.title
            form.content.data = post.content
            form.content.main_photo = post.main_photo
        else:
            form.title.data = "Home"
            form.content.data = "Lorem Ipsum"
            form.main_photo.data = "default.jpg"

    return render_template("home_edit.html",
                            title="Home Page Edit",
                            form=form,
                            legend='Home Page Edit')



@main_bp.route("/about")
def about():
    post = About_Post.query.order_by(About_Post.date_posted.desc()).first()
    return render_template('about.html', title='About', post=post)


### Edit About Page ###
@main_bp.route("/about/edit", methods=['GET', 'POST'])
@login_required
def update_about_page():
    post = About_Post.query.order_by(About_Post.date_posted.desc()).first()
    form = AboutPageForm()
    if form.validate_on_submit():
        post = About_Post(title=form.title.data,
                            content= form.content.data,
                            author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your About Page has been updated', 'success')
        return redirect(url_for('main_bp.about'))
    elif request.method == 'GET':
        if post:
            form.title.data = post.title
            form.content.data = post.content
        else:
            form.title.data = "About"
            form.content.data = "Lorem Ipsum"

    return render_template("about_edit.html",
                            title="About Page Edit",
                            form=form,
                            legend='About Page Edit')



### Map View ###
@main_bp.route("/maps")
def map():
    shop_map = Map(
        identifier="view-side",
        lat=37.744489,
        lng=-86.275832,
        markers=[(39.744489,-86.275832)]
    )
    return render_template('maps.html', shop_map=shop_map)




### CONTACT PAGE ###
@main_bp.route("/contact", methods=['GET', 'POST'])
def contact():
    form = CustomerMessageForm()
    if form.validate_on_submit():
        msg = Message('Customer inquisition from your website', sender='cycleincooperation@gmail.com', recipients=['cycleincooperation@gmail.com'])
        msg.body = f'''
From: \n\t{form.customer_name.data}
\nPhone: \n\t{form.customer_phone.data}
\nEmail: \n\t{form.customer_email.data}
\nMessage: \n\t{form.customer_message.data}
'''
        # sending the message
        mail.send(msg)

        # add all of this to the database:
        # time will be stored in UTC format and added automatically
        customer = Customer_Message(name=form.customer_name.data,
                                email=form.customer_email.data,
                                phone=form.customer_phone.data,
                                message=form.customer_message.data)
        db.session.add(customer)
        db.session.commit()
        flash('Message sent thank you. We will be in touch', 'success')
        return redirect(url_for('main_bp.home'))
    else:
        flash('All fields are required.', 'danger')
    return render_template('contact.html', form=form)
