from flask import Blueprint, jsonify, request
from userLogin.service.login import Login

userLogin = Blueprint('userLogin', __name__)


@userLogin.route('/')
def choose():
    email = request.values.get('email')[2:]
    password = request.values.get('password')[2:]
    loginResult, isManager = Login.userLogin(email, password)
    ret_data = []
    ret_data.append({"loginResult": loginResult, "isManager": isManager})
    return jsonify(ret_data)
