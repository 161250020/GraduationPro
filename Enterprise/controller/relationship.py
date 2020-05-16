from flask import Blueprint
from flask import render_template
from Enterprise.model.glo import Glo
from Enterprise.service.interpersonal_network import InterpersonalNetwork

relationship = Blueprint('relationship', __name__)


@relationship.route('/')
def choose():
    # 人际关系网络
    interpersonal_network = InterpersonalNetwork()
    for i in range(0, len(Glo.from_email)):
        interpersonal_network.add_node(interpersonal_network, Glo.from_email[i], Glo.to_email[i])
    return render_template('relationship.html')
