import os

from flask import Flask, render_template
from src.common.database import Database
from src.models.users.views import user_blueprint
from src.models.stores.views import store_blueprint
from src.models.alerts.views import alerts_blueprint
app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.urandom(16)

#@app.before_first_request
print(Database.DATABASE.client)

@app.route('/')
def home():
    return render_template('home.html')

app.register_blueprint(user_blueprint,url_prefix="/users")
app.register_blueprint(store_blueprint,url_prefix="/stores")
app.register_blueprint(alerts_blueprint,url_prefix="/alerts")

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'] ,port=4990)
