from .import bp as main
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
# from app.models import Post, User

@main.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')