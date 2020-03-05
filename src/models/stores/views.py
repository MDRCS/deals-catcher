from flask import Blueprint,render_template,request,redirect,url_for
from src.models.stores.decorators import requires_admin_permission
from src.models.stores.store import Store
import src.models.users.decorators as user_decorators

store_blueprint = Blueprint('stores',__name__)

@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_index.html',stores=stores)

@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.html', store=Store.getById(store_id))

@store_blueprint.route('/new',methods=['GET','POST'])
@user_decorators.requires_login
@requires_admin_permission
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = request.form['query']

        store = Store(name,url_prefix,tag_name,query)
        store.save_database()
        return redirect(url_for('.index'))

    return render_template('/stores/create_store.html')

@store_blueprint.route('/edit/<string:store_id>',methods=['GET','POST'])
@user_decorators.requires_login
@requires_admin_permission
def edit_store(store_id):
    store = Store.getById(store_id)
    if request.method == 'POST':
        store.name = request.form['name']
        store.url_prefix = request.form['url_prefix']
        store.tag_name = request.form['tag_name']
        store.query = request.form['query']
        store.update_record()
        return redirect(url_for('.store_page', store_id=store_id))
    return render_template('/stores/edit_store.html', store=store)

@store_blueprint.route('/delete/<string:store_id>',methods=['GET','POST'])
@user_decorators.requires_login
@requires_admin_permission
def delete_store(store_id):
    store = Store.getById(store_id)
    store.delete_record()
    return redirect(url_for('.index'))
