from flask import Blueprint, render_template, url_for, abort, redirect, flash, session

base = Blueprint('base', __name__, template_folder='./templates')


@base.route('/')
def home():
    return render_template('home.html', title="Home")

