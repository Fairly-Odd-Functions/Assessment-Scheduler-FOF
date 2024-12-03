from flask import Blueprint, jsonify
from App.controllers import initialize

index_views = Blueprint('index_views', __name__, template_folder='../templates')

"""Home"""
@index_views.route('/', methods=['GET'])
def index():
    return '<h1>Project 04 | Assessment Scheduler - Fairly Odd Functions</h1>', 200

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    response_data = {"message": "Database Initialized!"}
    return jsonify(response_data), 200