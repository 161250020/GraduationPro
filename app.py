from flask import Flask, render_template, request

# @app.route('/') # 路由
# return render_template('index.html') # 把HTML文件读进来，再交给浏览器
app = Flask(__name__) # 确定APP的启动路径

@app.route('/')
def Categories():


@app.route('/g',methods=['GET','POST'])
def pg():
    if request.method=='GET':
        name = request.args.get("name")
        print("form-get-name:", name)
        return render_template('index.html')
    if request.method=='POST':
        name = request.form.get("name")
        print("form-post-name:", name)
        return render_template('index.html')

@app.route('/p', methods=['post'])
def p():
    return render_template('index2.html',test='123')

if __name__ == '__main__':
    app.run(debug=True,port=80) # 127.0.0.1:回路，自己访问自己
