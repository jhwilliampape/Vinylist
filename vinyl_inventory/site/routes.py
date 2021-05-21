from flask import Blueprint, render_template
from flask_login import login_required

site = Blueprint('site', __name__, template_folder='site_templates')

"""
In the above code, some arguments are specified creating a blueprint object.
The first argument 'site' is the Blueprint's name.
This will be used by flaskes routing mechanism.
The second parameter __name__ is the BP's import name,
which flask uses to locate resources
"""

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')