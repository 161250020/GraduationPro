from flask import Blueprint
from flask import render_template, request
from Enterprise.model.glo import Glo
from Enterprise.service.feature_extraction import FeatureExtraction
from Enterprise.service.interpersonal_network import InterpersonalNetwork
from Enterprise.service.kmeans_classify import KmeansClassify

enterprise = Blueprint('enterprise', __name__)


@enterprise.route('/')
def dir():
    return render_template('dir.html')


@enterprise.route('/choose', methods=['POST'])
def choose():
    choose = request.form.get('func')
    if choose == 'category':
        Glo.word, Glo.weight = FeatureExtraction.feature_extraction(Glo.file_list)
        KmeansClassify.classify(Glo.file_list, Glo.weight, Glo.cluster)
        show = {}
        for clu in Glo.cluster.items():
            show[clu[0]] = len(clu[1])
        show = sorted(show.items(), key=lambda x: x[0])
        return render_template('categories.html', show=show)
    else:
        # 人际关系网络
        interpersonal_network = InterpersonalNetwork()
        for i in range(0, len(Glo.from_email)):
            interpersonal_network.add_node(interpersonal_network, Glo.from_email[i], Glo.to_email[i])
        return render_template('relationship.html')
