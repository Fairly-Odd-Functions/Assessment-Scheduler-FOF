from flask import Blueprint, flash, redirect, request, jsonify, render_template, url_for, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.controllers.auth import my_login_user, my_logout_user
from App.models.user import User
from App.models.staff import Staff
from App.models.admin import Admin
from App.database import db
# IMPORTS TO CLEAN UP

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

"""Login
Written
"""
@auth_views.route('/login', methods=['POST'])
def login_action():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error":"Email And Password Are Required"}), 400

        token = authenticate_and_login_user(data['email'], data['password'])
        if not token:
            return jsonify({"error": "Bad Email Or Password Given"}), 401

        return jsonify(access_token=token), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(error="An Error Occurred While Logging In"), 500

# Login Acion Helper Function
def authenticate_and_login_user(email, password):
    admin_user = db.session.query(Admin).filter(Admin.email == email).first()
    print(f"DEBUG: Attempting Admin Login: {admin_user}")
    if admin_user and admin_user.check_password(password):
        return my_login_user(admin_user)

    staff_user = db.session.query(Staff).filter(Staff.email == email).first()
    print(f"DEBUG: Attempting Staff Login: {staff_user}")
    if staff_user and staff_user.check_password(password):
        return my_login_user(staff_user)

    return None

"""LogOut"""
@auth_views.route('/logout', methods=['POST'])
@jwt_required()
def logout_action():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        print(f"DEBUG: Logging Out: {user.user_type} user")
        return my_logout_user()
    except Exception as e:
        print(f"DEBUG: Error During Logout: {e}")
        return jsonify(error="An Error Occurred While Logging Out"), 500