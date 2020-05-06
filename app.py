from flask import Flask, render_template, jsonify, request
from Enterprise.controller.classify_and_relationship import enterprise
from Enterprise.controller.topics import topics_con
from Enterprise.controller.summary_and_keywords import summary_con
from Personal.service import Relation

app = Flask(__name__) # 确定APP的启动路径
app.register_blueprint(enterprise,url_prefix='/enterprise')
app.register_blueprint(topics_con,url_prefix='/topic')
app.register_blueprint(summary_con,url_prefix='/summary')


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


@app.route('/getAllRelationship', methods=['GET', 'POST'])
def get_all_relationship():
    return Relation.get_all_realtionship()


@app.route('/getPersonalRelationship', methods=['GET', 'POST'])
def get_personal_relationship():
    email = request.form.get('email')
    return Relation.get_personal_relationship(email)



if __name__ == '__main__':
    app.run(debug=True,port=80) # 127.0.0.1:回路，自己访问自己
