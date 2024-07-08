import json
import logging
import os.path
import traceback

from flask import Flask, request, abort, send_file
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_sock import Sock
from sqlalchemy.orm.attributes import flag_modified

import interfaces
import utils
from api import api
from config import *
from handlers import ConcurrentTimedRotatingFileHandler
from socket_handler import SocketHandler
from tables import *

app = Flask(__name__)

logger = logging.getLogger("werkzeug")
# handler = ConcurrentTimedRotatingFileHandler("logs/backend", lockfile="logs/backend.lock")
# logger.addHandler(handler)

app.config["SQLALCHEMY_DATABASE_URI"] = "%s+%s://%s:%s@%s:%d/%s?charset=utf8" % (
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_size": -1, "pool_recycle": 120, "pool_pre_ping": True,
                                           "max_overflow": -1}

db.init_app(app)
CORS(app)
app.register_blueprint(api, url_prefix="/api")
# app.register_blueprint(interfaces.clan)
app.register_blueprint(interfaces.admin)
# app.register_blueprint(interfaces.prop)
# app.register_blueprint(interfaces.event)
sock = Sock(app)


class Config(object):
    JOBS = [
        {
            'id': 'match',
            'func': 'service:checkMatchReady',
            'args': (),
            'trigger': 'interval',
            'seconds': 1,
        }
    ]
    SCHEDULER_API_ENABLED = True


app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)


@app.before_request
def log_request():
    logger.info("\nremote: %s  path: %s  args: %s  json: %s" % (
        request.remote_addr, request.path, {k: v for k, v in request.args.items()},
        {k: v for k, v in request.json.items()} if request.method == "POST" else {}))


@sock.route('/connect')
def connect(ws):
    SocketHandler(ws).run()


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(User.username == username).first()
    if player is None or utils.password_hash(password, player.salt) != player.password:
        result["success"] = False
        result["message"] = "用户名或密码错误"
    elif player.ban_until_time is not None and player.ban_until_time > datetime.datetime.now():
        result["success"] = False
        result["message"] = "您已被封禁，%s之前禁止登录" % player.ban_until_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        player.last_login_ip = request.remote_addr
        db.session.commit()
        player = User.query.filter(User.username == username).first()

        result["success"] = True
        result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(User.username == username).first()
    if player is not None:
        result["success"] = False
        result["message"] = "该用户名已被注册"
    elif username == "New_Player":
        result["success"] = False
        result["message"] = "禁止使用New_Player作为名称"
    elif not User.is_username_valid(username):
        result["success"] = False
        result["message"] = "非法用户名"
    elif not User.is_password_valid(password):
        result["success"] = False
        result["message"] = "密码格式不正确"
    else:
        player = User()
        player.username = username
        player.salt = int.from_bytes(utils.randbytes(4), byteorder="little", signed=True)
        player.password = utils.password_hash(password, player.salt)
        player.last_login_ip = request.remote_addr

        db.session.add(player)
        db.session.flush()

        db.session.commit()
        result["success"] = True
        player = User.query.filter(User.username == username).first()
        result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@app.route("/set-guid", methods=["POST"])
def set_guid():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    guid = int(request.json.get("guid"))

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif player.unique_id is not None:
        result["success"] = False
        result["message"] = "GUID不能被修改，如需修改请联系管理员"
    elif User.query.filter(User.unique_id == guid).first() is not None:
        result["success"] = False
        result["message"] = "该GUID已被占用"
    else:
        player.unique_id = guid
        db.session.commit()
        player = User.query.filter(User.id == _id).first()
        result["success"] = True
        result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@app.route("/set-preference", methods=["POST"])
def set_preference():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    preference = int(request.json.get("preference"))

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    else:
        player.preference = preference
        db.session.commit()
        player = User.query.filter(User.id == _id).first()
        result["success"] = True
        result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@app.route("/change-username", methods=["POST"])
def change_username():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    new_username = request.json.get("new_username")

    result = {"success": False, "message": "", "data": {}}
    target_player = User.query.filter(User.username == new_username).first()
    player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif player.last_change_username_time is not None and \
            player.last_change_username_time + datetime.timedelta(days=30) > datetime.datetime.now():
        result["success"] = False
        result["message"] = "距离您上次改名还不到30天，%s之前不可改名" % (
                player.last_change_username_time + datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    elif target_player is not None:
        result["success"] = False
        result["message"] = "该用户名已被注册"
    elif username == new_username:
        result["success"] = False
        result["message"] = "新名称不能与旧名称相同"
    elif new_username == "New_Player":
        result["success"] = False
        result["message"] = "禁止使用New_Player作为名称"
    elif not User.is_username_valid(new_username):
        result["success"] = False
        result["message"] = "非法用户名"
    else:
        player.history_names.append(player.username)
        flag_modified(player, "history_names")
        player.username = new_username
        player.last_change_username_time = datetime.datetime.now()
        db.session.commit()
        player = User.query.filter(User.id == _id).first()
        result["success"] = True
        result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@app.route("/change-password", methods=["POST"])
def change_password():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    new_password = request.json.get("new_password")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif not User.is_password_valid(new_password):
        result["success"] = False
        result["message"] = "密码格式不正确"
    else:
        player.password = utils.password_hash(new_password, player.salt)
        db.session.commit()
        player = User.query.filter(User.id == _id).first()
        result["success"] = True
        result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@app.route("/refresh-user-data", methods=["GET"])
def refresh_user_data():
    _id = request.args.get("id")
    username = request.args.get("username")
    password = request.args.get("password")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    else:
        result["success"] = True
        result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@app.route("/get-match-history", methods=["GET"])
def get_match_history():
    _id = request.args.get("id")
    username = request.args.get("username")
    password = request.args.get("password")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    total_matches = Match.query.filter(or_(db.func.json_contains(Match.result["team_1"], "%d" % player.id),
                                           db.func.json_contains(Match.result["team_2"], "%d" % player.id))).all()
    matches = []
    for m in total_matches:
        if player.id in m.result["team_1"] or player.id in m.result["team_2"]:
            matches.append(m.to_json())
    if player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    else:
        result["success"] = True
        result["data"]["matches"] = matches
    return json.dumps(result, ensure_ascii=False)


@app.route("/get-total-data", methods=["GET"])
def get_total_data():
    result = {"success": True, "message": "",
              "data": {"maps": utils.maps, "modes": utils.modes, "ranks": RANKS, "config": {
                  "match_wait_ready_seconds": MATCH_WAIT_READY_SECONDS,
                  "match_pick_teammate_seconds": MATCH_PICK_TEAMMATE_SECONDS,
              }}}
    return json.dumps(result, ensure_ascii=False)


@app.route("/query-user-info", methods=["GET"])
def query_user_info():
    _id = request.args.get("id")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(User.id == _id).first()
    if player is None:
        result["success"] = False
        result["message"] = "用户不存在"
    else:
        result["success"] = True
        result["data"]["user"] = player.to_query_json()
    return json.dumps(result, ensure_ascii=False)


@app.route("/get-leaderboard", methods=["GET"])
def get_leaderboard():
    result = {"success": True, "message": "", "data": {}}

    update_time, leaderboard = utils.get_leaderboard()
    result["data"]["update_time"] = update_time.strftime("%Y-%m-%d %H:%M:%S")
    result["data"]["leaderboard"] = leaderboard[:20]
    return json.dumps(result, ensure_ascii=False)


"""
--------------       上面的代码都是已测试代码        -----------------
"""


@app.route("/image/<path:path>", methods=["GET"])
def image(path):
    file = "files/image/" + path + ".jpg"
    if os.path.isfile(file):
        return send_file(file, max_age=3600 * 24)
    return send_file("files/image/default.jpg", max_age=3600 * 24)


@app.route("/reforge/<path:version>", methods=["GET"])
def reforge(version):
    path = "files/reforge/"
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            if file.startswith("Reforge-v" + version):
                return send_file(path + file, as_attachment=True)
    abort(404)


@app.route("/static_files/<path:path>", methods=["GET"])
def static_files(path):
    return send_file("files/static/" + path)


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    return ""


# My Test Function
@app.route("/aj39g753jnase8u43tnr2", methods=["GET"])
def test():
    raise Exception("log test")

    return "hits"


@app.errorhandler(Exception)
def catch_all_except(e):
    logger.info(traceback.format_exc())
    db.session.rollback()
    db.session.remove()
    raise e


if __name__ == "__main__":
    scheduler.start()
    app.run('0.0.0.0', 80, debug=True)
