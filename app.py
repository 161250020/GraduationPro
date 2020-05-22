from flask import Flask, render_template, jsonify, request
from Enterprise.controller.category import category
from Enterprise.controller.relationship import relationship
from Enterprise.controller.topics import topics_con
from Enterprise.controller.summary_and_keywords import summary_con
from userLogin.controller.login import userLogin
from Personal.service import Relation
from Personal.service import LDA_keyword as Keyword
from Enterprise.controller import category as Category
from Enterprise.controller import topics as Topic
from Enterprise.controller import summary_and_keywords as Doc
from Personal.dao import db_connector as db

app = Flask(__name__)  # 确定APP的启动路径
app.register_blueprint(category, url_prefix='/category')
app.register_blueprint(relationship, url_prefix='/relationship')
app.register_blueprint(topics_con, url_prefix='/topic')
app.register_blueprint(summary_con, url_prefix='/summary')
app.register_blueprint(userLogin, url_prefix='/userLogin')


@app.route('/')
def dir():
    return render_template('dir.html')


@app.route('/drawChart', methods=['GET'])
def showChart():
    date = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    number = [820, 932, 901, 934, 1290, 1330, 1320]
    return jsonify({'date': date, 'number': number})


@app.route('/getUserName', methods=['GET', 'POST'])
def Try():
    userID = request.form.get('id')
    return 'Nie Wentao'


@app.route('/getMail', methods=['GET', 'POST'])
def get_mail():
    return db.get_email_list_in_json()


@app.route('/getAllRelationship', methods=['GET', 'POST'])
def get_all_relationship():
    return Relation.get_all_realtionship()


@app.route('/getPersonalRelationship', methods=['GET', 'POST'])
def get_personal_relationship():
    email = request.values.get('email')
    return Relation.get_personal_relationship(email)


@app.route('/getAllKeyword', methods=['GET', 'POST'])
def get_all_keyword():
    return Keyword.all_mail()


@app.route('/getKeywordByDate', methods=['GET', 'POST'])
def get_keyword_date():
    startTime = request.form.get('startTime')
    endTime = request.form.get('endTime')
    print(startTime, endTime)
    return Keyword.all_mail()
    # return Keyword.mail_by_date(datetime)


@app.route('/getCategory', methods=['GET', 'POST'])
def get_category():
    return Category.choose()


@app.route('/getTopic', methods=['GET', 'POST'])
def get_topic():
    return Topic.topics()


@app.route('/getDoc', methods=['GET', 'POST'])
def get_doc():
    return Doc.docs()


if __name__ == '__main__':
    app.run(debug=True, port=80)  # 127.0.0.1:回路，自己访问自己
