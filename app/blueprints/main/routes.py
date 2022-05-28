from .import bp as main
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import *
# from app.models import Post, User

# @main.route('/', methods = ['GET'])
# @login_required
# def index():
#     return render_template('index.html.j2')

@main.route('/', methods = ['GET'])
@login_required
def shop():
    types = Type.query.all()
    products = Product.query.all()
    return render_template('shop.html.j2', types = types, products =products)



@main.route('/types/<int:id>', methods = ['GET'])
@login_required
def types(id):
    types = Type.query.all()
    type = Type.query.get(id)
    products = type.products.all()
    return render_template('shop.html.j2', types = types, products =products)


@main.route('/cart')
@login_required
def cart():
    products = current_user.products.all()
    total = current_user.total_cart()
    return render_template('cart.html.j2', products = products, total =total)


@main.route('/add/<int:id>')
@login_required
def add(id):
    product = Product.query.get(id)
    current_user.add_to_cart(product)
    flash(f"{product.name} was added to your cart", 'info')
    return redirect(url_for('main.shop'))

@main.route('/delete/<int:id>')
@login_required
def delete(id):
    product = Product.query.get(id)
    current_user.del_from_cart(product)
    flash(f"{product.name} was removed from your cart", 'warning')
    return redirect(url_for('main.cart'))

@main.route('/pay')
@login_required
def pay():
    current_user.pay()
    flash('Enjoy ! Thank you for shopping with Trash 2 Treasure!', 'success')
    return redirect(url_for('main.cart'))

@main.route('/user_info')
@login_required
def user_info():
    products = current_user.products.all()
    total = current_user.total_cart()
    return render_template('user_info.html.j2', user = current_user, products = products, total = total)






