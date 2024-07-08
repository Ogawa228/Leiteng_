import json

from flask import Blueprint, request
from sqlalchemy.orm.attributes import flag_modified

import utils
from tables import *

admin = Blueprint('admin', __name__)


# admin_level:
# 1 - 查询玩家数据，重置玩家密码、GUID，封禁、解封玩家，取消比赛
# 10 - 给予、解除管理权限

@admin.route("/query-user-admin", methods=["POST"])
def query_user_admin():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    query_type = int(request.json.get("query_type"))  # 1 by username, others by guid
    query_value = request.json.get("query_value")

    result = {"success": False, "message": "", "data": {}}
    admin_player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if admin_player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif admin_player.admin_level < 1:
        result["success"] = False
        result["message"] = "管理权限不足"
    else:
        if query_type == 1:
            player = User.query.filter(User.username == query_value).first()
        else:
            player = User.query.filter(User.unique_id == int(query_value)).first()

        if player is None:
            result["success"] = False
            result["message"] = "玩家不存在"
        else:
            result["success"] = True
            result["data"]["user"] = player.to_admin_query_json()

    return json.dumps(result, ensure_ascii=False)


@admin.route("/unban-user", methods=["POST"])
def unban_user():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    target_user = int(request.json.get("target_user"))

    result = {"success": False, "message": "", "data": {}}
    admin_player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if admin_player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif admin_player.admin_level < 1:
        result["success"] = False
        result["message"] = "管理权限不足"
    else:
        player = User.query.filter(User.id == target_user).first()
        if player is None:
            result["success"] = False
            result["message"] = "玩家不存在，请刷新重试"
        else:
            player.ban_until_time = None
            db.session.commit()
            result["success"] = True
            player = User.query.filter(User.id == target_user).first()
            result["data"]["user"] = player.to_admin_query_json()
    return json.dumps(result, ensure_ascii=False)


@admin.route("/ban-user", methods=["POST"])
def ban_user():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    target_user = int(request.json.get("target_user"))
    minutes = int(request.json.get("minutes"))

    result = {"success": False, "message": "", "data": {}}
    admin_player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if admin_player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif admin_player.admin_level < 1:
        result["success"] = False
        result["message"] = "管理权限不足"
    else:
        player = User.query.filter(User.id == target_user).first()
        if player is None:
            result["success"] = False
            result["message"] = "玩家不存在，请刷新重试"
        elif admin_player.admin_level <= player.admin_level:
            result["success"] = False
            result["message"] = "管理权限不足"
        else:
            player.ban_until_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            db.session.commit()
            from service import globalService
            globalService.removeUserConnection(target_user)
            result["success"] = True
            player = User.query.filter(User.id == target_user).first()
            result["data"]["user"] = player.to_admin_query_json()
    return json.dumps(result, ensure_ascii=False)


@admin.route("/clear-guid", methods=["POST"])
def clear_guid():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    target_user = int(request.json.get("target_user"))

    result = {"success": False, "message": "", "data": {}}
    admin_player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if admin_player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif admin_player.admin_level < 1:
        result["success"] = False
        result["message"] = "管理权限不足"
    else:
        player = User.query.filter(User.id == target_user).first()
        if player is None:
            result["success"] = False
            result["message"] = "玩家不存在，请刷新重试"
        else:
            player.unique_id = None
            db.session.commit()
            result["success"] = True
            player = User.query.filter(User.id == target_user).first()
            result["data"]["user"] = player.to_admin_query_json()
    return json.dumps(result, ensure_ascii=False)


@admin.route("/reset-statistics", methods=["POST"])
def reset_statistics():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    target_user = int(request.json.get("target_user"))

    result = {"success": False, "message": "", "data": {}}
    admin_player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if admin_player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif admin_player.admin_level < 10:
        result["success"] = False
        result["message"] = "管理权限不足"
    else:
        player = User.query.filter(User.id == target_user).first()
        if player is None:
            result["success"] = False
            result["message"] = "玩家不存在，请刷新重试"
        else:
            player.rank = 1000
            player.rank_33 = 1000

            player.kill = 0
            player.death = 0
            player.match = 0
            player.win = 0
            player.lose = 0
            player.even = 0

            player.damage = 0
            player.team_damage = 0

            db.session.commit()
            result["success"] = True
            player = User.query.filter(User.id == target_user).first()
            result["data"]["user"] = player.to_admin_query_json()
    return json.dumps(result, ensure_ascii=False)


@admin.route("/set-password", methods=["POST"])
def set_password():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    target_user = int(request.json.get("target_user"))
    new_password = request.json.get("new_password")

    result = {"success": False, "message": "", "data": {}}
    admin_player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if admin_player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif admin_player.admin_level < 1:
        result["success"] = False
        result["message"] = "管理权限不足"
    else:
        player = User.query.filter(User.id == target_user).first()
        if player is None:
            result["success"] = False
            result["message"] = "玩家不存在，请刷新重试"
        elif not User.is_password_valid(new_password):
            result["success"] = False
            result["message"] = "密码格式不正确"
        else:
            player.password = utils.password_hash(new_password, player.salt)
            db.session.commit()
            result["success"] = True
            player = User.query.filter(User.id == target_user).first()
            result["data"]["user"] = player.to_admin_query_json()
    return json.dumps(result, ensure_ascii=False)


@admin.route("/admin-set-username", methods=["POST"])
def admin_set_username():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    target_user = int(request.json.get("target_user"))
    new_username = request.json.get("new_username")

    result = {"success": False, "message": "", "data": {}}
    admin_player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    player = User.query.filter(User.username == new_username).first()
    if admin_player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif admin_player.admin_level < 10:
        result["success"] = False
        result["message"] = "管理权限不足"
    elif player is not None:
        result["success"] = False
        result["message"] = "该用户名已被注册"
    elif new_username == "New_Player":
        result["success"] = False
        result["message"] = "禁止使用New_Player作为名称"
    elif not User.is_username_valid(new_username):
        result["success"] = False
        result["message"] = "非法用户名"
    else:
        player = User.query.filter(User.id == target_user).first()
        if player is None:
            result["success"] = False
            result["message"] = "玩家不存在，请刷新重试"
        else:
            player.history_names.append(player.username)
            flag_modified(player, "history_names")
            player.username = new_username
            db.session.commit()
            result["success"] = True
            player = User.query.filter(User.id == target_user).first()
            result["data"]["user"] = player.to_admin_query_json()
    return json.dumps(result, ensure_ascii=False)


@admin.route("/set-admin", methods=["POST"])
def set_admin():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    target_user = int(request.json.get("target_user"))

    result = {"success": False, "message": "", "data": {}}
    admin_player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if admin_player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif admin_player.admin_level < 10:
        result["success"] = False
        result["message"] = "管理权限不足"
    else:
        player = User.query.filter(User.id == target_user).first()
        if player is None:
            result["success"] = False
            result["message"] = "玩家不存在，请刷新重试"
        elif player.admin_level > 0:
            result["success"] = False
            result["message"] = "玩家已经是管理员了"
        else:
            player.admin_level = 1
            db.session.commit()
            result["success"] = True
            player = User.query.filter(User.id == target_user).first()
            result["data"]["user"] = player.to_admin_query_json()
    return json.dumps(result, ensure_ascii=False)


@admin.route("/unset-admin", methods=["POST"])
def unset_admin():
    _id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    target_user = int(request.json.get("target_user"))

    result = {"success": False, "message": "", "data": {}}
    admin_player = User.query.filter(and_(
        and_(User.id == _id, User.username == username),
        User.password == password)).first()
    if admin_player is None:
        result["success"] = False
        result["message"] = "用户信息错误，请尝试重新登录"
    elif admin_player.admin_level < 10:
        result["success"] = False
        result["message"] = "管理权限不足"
    else:
        player = User.query.filter(User.id == target_user).first()
        if player is None:
            result["success"] = False
            result["message"] = "玩家不存在，请刷新重试"
        elif player.admin_level > 1:
            result["success"] = False
            result["message"] = "权限等级不足"
        else:
            player.admin_level = 0
            db.session.commit()
            result["success"] = True
            player = User.query.filter(User.id == target_user).first()
            result["data"]["user"] = player.to_admin_query_json()
    return json.dumps(result, ensure_ascii=False)


@admin.errorhandler(Exception)
def catch_all_except(e):
    db.session.rollback()
    db.session.remove()
    raise e
