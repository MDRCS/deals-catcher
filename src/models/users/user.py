import uuid
from src.common.database import Database as db
from src.common.utils import Utils
import src.models.users.errors as exc
import src.models.users.constants as UserConstraints
from src.models.alerts.alert import Alert

class User(object):
    def __init__(self,email,password,_id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email,password):
        user = db.find_one(UserConstraints.Collection, {'email': email})
        if user is None:
            raise exc.UserNotExistsError("Your user does not exist")
        if not Utils.check_hashed_password(password,user['password']):
            raise exc.IncorrectPasswordError("Your password is wrong")

        return True

    @staticmethod
    def register_user(email,password):
        user = db.find_one(UserConstraints.Collection, {'email': email})
        if user is not None:
            raise exc.UserAlreadyRegisterError("The email you used to register is already exists.")
        if not Utils.email_is_valid(email):
            raise exc.InvalidEmailError("The email doesn't have a valid format.")

        User(email,Utils.hash_password(password)).save_database()

        return True

    def save_database(self):
        db.insert('users',self.json())

    def json(self):
        return {
            "email": self.email,
            "password": Utils.hash_password(self.password),
            "_id": self._id
        }

    @classmethod
    def getByEmail(cls,email):
        return cls(**db.find_one(UserConstraints.Collection, {'email': email}))

    def getAlerts(self):
        return Alert.getByEmail(self.email)
