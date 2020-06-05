from flask import Blueprint, jsonify
from Enterprise.model.glo import Glo
from Enterprise.service.feature_extraction import FeatureExtraction
from Enterprise.service.get_data import GetData
from Enterprise.service.kmeans_classify import KmeansClassify

category = Blueprint('category', __name__)


@category.route('/')
def choose():
    GetData.load_data()
    Glo.word, Glo.weight = FeatureExtraction.feature_extraction(Glo.file_list)
    if len(Glo.cluster) == 0:
        KmeansClassify.classify(Glo.file_list, Glo.weight, Glo.cluster)

    show = {}
    for clu in Glo.cluster.items():
        show[clu[0]] = len(clu[1])
    show = sorted(show.items(), key=lambda x: x[0])
    ret_data = []
    for cate_info in show:
        ret_data.append({"category": '类别' + str(cate_info[0]), "number": cate_info[1]})
    return jsonify(ret_data)
