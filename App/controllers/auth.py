import flask_login
from flask import jsonify
from functools import wraps
from App.models import User, Admin, Staff
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

# Setup JWT Authentication
def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
      return user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
      identity = jwt_data["sub"]
      return User.query.get(identity)

# Setup Flask-Login
def setup_flask_login(app):
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login' # Login View

    @login_manager.user_loader
    def load_user(user_id):
       staff = Staff.query.get(user_id)
       if staff: 
          return staff

       admin = Admin.query.get(user_id)
       if admin:
          return admin
       return None

def login_user(user):
  flask_login.login_user(user)
  access_token = create_access_token(identity=user.userID)
  return jsonify(access_token=access_token), 200

def logout_user(user):
  flask_login.logout_user()
  return jsonify(message="Logged Out successfully"), 200

def login_required(required_class):
  def wrapper(f):

    @wraps(f)
    @jwt_required()  # Ensure JWT Authentication
    def decorated_function(*args, **kwargs):
      user = required_class.query.filter_by(
          username=get_jwt_identity()).first()
      print(user.__class__, required_class, user.__class__ == required_class)
      if user.__class__ != required_class:  # Check Class Equality
        return jsonify(error='Invalid user role'), 403
      return f(*args, **kwargs)
    return decorated_function
  return wrapper

def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        is_authenticated = True
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated = is_authenticated, current_user = current_user)

# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return User.query.get(payload['identity'])