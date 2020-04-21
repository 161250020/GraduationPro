from flask import Flask, render_template
from Enterprise.controller.classify_and_relationship import enterprise
from Enterprise.controller.topics import topics_con
from Enterprise.controller.summary_and_keywords import summary_con

app = Flask(__name__) # 确定APP的启动路径
app.register_blueprint(enterprise,url_prefix='/enterprise')
app.register_blueprint(topics_con,url_prefix='/topic')
app.register_blueprint(summary_con,url_prefix='/summary')

@app.route('/')
def dir():
    return render_template('dir.html')

if __name__ == '__main__':
    app.run(debug=True,port=80) # 127.0.0.1:回路，自己访问自己
