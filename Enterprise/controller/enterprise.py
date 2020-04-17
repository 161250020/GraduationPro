from flask import Blueprint
from flask import render_template, request
from Enterprise.glo import Glo
from Enterprise.service.interpersonal_network import InterpersonalNetwork
from Enterprise.service.choose import classify

enterprise = Blueprint('enterprise',__name__)

@enterprise.route('/')
def dir():
    return render_template('dir.html')

@enterprise.route('/choose',methods=['POST'])
def choose():
    choose=request.form.get('func')
    if choose=='category':
        if(len(Glo.cluster)==0):
            classify(Glo.file_list, Glo.weight,Glo.cluster)
        show = {}
        for clu in Glo.cluster.items():
            show[clu[0]] = len(clu[1])
        show = sorted(show.items(), key=lambda x: x[0])
        return render_template('categories.html', show=show)
    else:
        #人际关系网络
        interpersonalNetwork = InterpersonalNetwork()
        for i in range(0, len(Glo.from_email)):
            interpersonalNetwork.addNode(Glo.from_email[i], Glo.to_email[i])
        return render_template('relationship.html')
