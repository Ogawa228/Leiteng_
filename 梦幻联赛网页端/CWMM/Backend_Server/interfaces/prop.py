import json

from flask import Blueprint, request

from tables import *

prop = Blueprint('prop', __name__)


@prop.route("/use-prop", methods=["POST"])
def use_prop():
    _id = request.json.get("id")
    login_name = request.json.get("login_name")
    prop = request.json.get("prop")

    result = {"success": False, "message": "暂不支持该功能", "data": {}}
    return json.dumps(result, ensure_ascii=False)
    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()
    player.props.remove(prop)
    msg = player.use_prop(util.get_prop_by_id(prop))
    flag_modified(player, "props")
    db.session.commit()
    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()
    result["success"] = True
    result["message"] = msg
    result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@prop.errorhandler(Exception)
def catch_all_except(e):
    db.session.rollback()
    db.session.remove()
    raise e
