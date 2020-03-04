from flask import Blueprint,render_template,request,session,redirect,url_for

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorators

alerts_blueprint = Blueprint('alerts', __name__)

@alerts_blueprint.route('/')
def index():
    return 'This is the alerts index'

@alerts_blueprint.route('/new', methods=['POST','GET'])
@user_decorators.requires_login
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])
        item = Item(name,url)
        item.save_database()

        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price() #Already Save to database
        return redirect(url_for('users.getUserAlerts'))
    return render_template('alerts/create_alert.html')

@alerts_blueprint.route('/update/<string:alert_id>', methods=['POST','GET'])
@user_decorators.requires_login
def update_alert(alert_id):
    alert = Alert.getById(alert_id)
    if request.method == 'POST':
        alert.price_limit = request.form['price_limit']
        alert.update_record({'_id': alert._id})
        return redirect(url_for('users.getUserAlerts'))

    return render_template('alerts/edit_alert.html', alert=alert)

@alerts_blueprint.route('/desactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    Alert.getById(alert_id).deactivate()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))

@alerts_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    Alert.getById(alert_id).activate()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))

@alerts_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete(alert_id):
    Alert.getById(alert_id).delete()
    return redirect(url_for('users.getUserAlerts'))

@alerts_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.getById(alert_id)
    return render_template('alerts/alert.html', alert=alert)

@alerts_blueprint.route('/check_price/<string:alert_id>')
@user_decorators.requires_login
def check_alert_price_for_update(alert_id):
    Alert.getById(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))
