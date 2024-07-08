import traceback

from flask import Blueprint, request

from config import *
from message import *
from tables import *

api = Blueprint('api', __name__)

"""
@api.route("/bind", methods=["GET"])
def bind():
    uid = int(request.args.get("p"))
    index = int(request.args.get("i"))
    login_name = request.args.get("u")
    verify = request.args.get("d")

    player = User.query.filter(and_(User.login_name == login_name, User.verify == verify)).first()
    if player is None:
        return message_show_server_message(index, "绑 定 失 败 ！ 角 色 名 或 验 证 码 不 正 确 ， 请 检 查 你 的 角 色 名 和 密 钥 ")
    elif player.unique_id is not None:
        return message_show_server_message(index, "绑 定 失 败 ！ 此 账 号 已 绑 定 其 他 key")
    elif User.query.filter(User.unique_id == uid).first() is not None:
        return message_show_server_message(index, "绑 定 失 败 ！ 一 个 key最 多 只 能 绑 定 一 个 账 号 ")
    else:
        player.unique_id = uid
        db.session.commit()
        player = User.query.filter(and_(User.login_name == login_name, User.unique_id == uid)).first()
        return message_update_player_statistics(player, index)
"""


@api.before_request
def ip_filter():
    remote_addr = request.headers.get("X-Real-IP")
    if remote_addr is None:
        remote_addr = request.remote_addr
    if remote_addr not in CWMM_SERVER_LIST:
        return ""


@api.route("/tick", methods=["GET"])
def tick():
    server_name = request.args.get("n")

    return message_server_match_status(server_name)


@api.route("/player-join", methods=["GET"])
def player_join():
    uid = int(request.args.get("p"))
    index = int(request.args.get("i"))
    username = request.args.get("n")
    servername = request.args.get("s")

    player = User.query.filter(User.username == username).first()
    if player is None or player.unique_id is None:
        return message_show_server_message(index, "您 的 GUID是 ： %d" % uid)

    if player.unique_id is not None and player.unique_id != uid:
        return message_kick_player(index)

    if player.is_banned():
        return message_kick_player(index)

    return message_player_status(servername, player.id, index)


@api.route("/cancel", methods=["GET"])
def cancel():
    server = request.args.get("s")
    player_guids = [int(c) for c in request.args.get("p").split(",")]

    return message_cancel_result(server, player_guids)


@api.route("/finish", methods=["GET"])
def finish():
    server = request.args.get("s")
    player_data = [int(c) for c in request.args.get("p").split(",")]
    team_1_score = int(request.args.get("s1"))
    team_2_score = int(request.args.get("s2"))

    return message_finish_result(server, player_data, team_1_score, team_2_score)


@api.errorhandler(Exception)
def catch_all_except(e):
    traceback.print_exc()
    db.session.rollback()
    db.session.remove()
    return ""
