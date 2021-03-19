from flask import Blueprint, render_template

errors = Blueprint("errors", __name__, template_folder='./templates')


# Error Pages
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('404.html')


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('500.html')
