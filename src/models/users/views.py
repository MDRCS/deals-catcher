from flask import Blueprint, request, session, url_for, render_template, make_response
from werkzeug.utils import redirect
from .errors import UserError
from src.models.users.user import User
from src.models.alerts.alert import Alert
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route("/login")
def login_page():
    return render_template("users/login.html")

@user_blueprint.route("/register")
def register_page():
    return render_template("users/register.html")

@user_blueprint.route('/auth/login',methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for("users.getUserAlerts"))
        except UserError as e:
            return e.message

    return render_template("users/login.html")

@user_blueprint.route('/auth/register',methods=['POST','GET'])
def user_register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for("users.getUserAlerts"))
        except UserError as e:
            return e.message

    return render_template("users/register.html")

@user_blueprint.route('/logout')
def user_logout():
    session['email'] = None
    return redirect(url_for('home'))

@user_blueprint.route('/alters')
@user_decorators.requires_login
def getUserAlerts():
    user = User.getByEmail(session['email'])
    alerts = user.getAlerts()

    return render_template('users/alerts.html', alerts=alerts)

@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass
