from flask import Blueprint, render_template, request

index_enter = Blueprint('index_enter',__name__)

@index_enter.route('/')
def dir():
    return render_template('dir.html')