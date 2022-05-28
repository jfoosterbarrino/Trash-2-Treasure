from . import bp as auth
from app.models import Customer
from .forms import LoginForm, SignUpForm, EditInfoForm
from flask import request, redirect, render_template, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        customer = Customer.query.filter_by(email = email).first()
        if customer and customer.check_hashed_password(password):
            login_user(customer)
            flash('Successful Login! Welcome to Trash 2 Treasure!', 'success')
            return redirect(url_for('main.shop'))
        flash('Incorrect Email and/or Password. Try again.', 'danger')
        return render_template('login.html.j2', form =form)
    return render_template('login.html.j2', form = form)


@auth.route('/sign_up', methods =['GET','POST'])
def sign_up():
    form = SignUpForm()
    u = Customer.query.filter_by(email = form.email.data).first()
    if u:
        flash('Email already registered', "danger")
        return redirect(url_for('auth.sign_up'))
    else:

        if request.method == 'POST' and form.validate_on_submit():
            new_user_data={
                'first_name' : form.first_name.data.title(),
                'last_name' : form.last_name.data.title(),
                'email' : form.email.data.lower(),
                'password' : form.password.data,
                'icon' : f'https://avatars.dicebear.com/api/initials/{form.first_name.data[0]}{form.last_name.data[0]}.svg'
            }

            new_user_object = Customer()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()

            flash('Congratulations! You have successfully registered.','success')
            return redirect(url_for('auth.login'))

        elif request.method == 'GET':
            return render_template('sign_up.html.j2', form = form)

        else:
            flash('Unsuccessful Login, Please Try Again Later','danger')
            return render_template('sign_up.html.j2', form =form)


@auth.route('/edit_info', methods = ['GET','POST'])
def edit_info():
    form = EditInfoForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data,
                "icon": f'https://avatars.dicebear.com/api/initials/{form.first_name.data[0]}{form.last_name.data[0]}.svg'
            }
        customer = Customer.query.filter_by(email = new_user_data['email']).first()
        if customer and customer.email != current_user.email:
            flash('Email is already in use', 'danger')
            return redirect(url_for('auth.edit_info'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile Updated','success')
        except:
            flash('There was an unexpected error, please try again!','danger')
            return redirect(url_for('auth.edit_info'))
        return redirect(url_for('main.user_info'))
    return render_template('sign_up.html.j2', form = form)

    
@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have been logged out', 'info')
        return redirect(url_for('auth.login'))