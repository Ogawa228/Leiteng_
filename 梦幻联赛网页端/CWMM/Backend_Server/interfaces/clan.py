import json
import time

from flask import Blueprint, request, abort

from tables import *

clan = Blueprint('clan', __name__)


@clan.route("/dismiss-clan", methods=["POST"])
def dismiss_clan():
    _id = request.json.get("id")
    login_name = request.json.get("login_name")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()
    clan = Clan.query.filter(Clan.id == player.clan_member).first()

    if clan.leader != _id or len(clan.members) > 1:
        abort(500)

    player.clan_member = None
    for instance in clan.equipments:
        player.equipments.append(instance)
    flag_modified(player, "equipments")
    db.session.delete(clan)

    db.session.commit()
    result["success"] = True
    player = User.query.filter(User.id == _id).first()
    result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@clan.route("/quit-clan", methods=["POST"])
def quit_clan():
    _id = request.json.get("id")
    login_name = request.json.get("login_name")
    quit_user_id = int(request.json.get("quit_user_id"))

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()
    clan = Clan.query.filter(Clan.id == player.clan_member).first()
    clan.remove_user(_id, quit_user_id)
    db.session.commit()
    result["success"] = True
    player = User.query.filter(User.id == _id).first()
    result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@clan.route("/donate-gold", methods=["POST"])
def donate_gold():
    _id = request.json.get("id")
    login_name = request.json.get("login_name")
    gold = request.json.get("gold")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()
    if player.gold < gold or player.gold_givable < gold:
        abort(500)

    clan = Clan.query.filter(Clan.id == player.clan_member).first()
    clan.gold += gold
    player.gold -= gold
    player.gold_givable -= gold
    clan.records.insert(0, {"title": "金币捐赠", "content": "%s向战队捐赠了%d金币" % (player.login_name, gold),
                            "time": time.strftime("%Y-%m-%d %H:%M:%S")})
    for member in clan.members:
        if member["id"] == player.id:
            member["donate"] += gold
            break
    flag_modified(clan, "members")
    flag_modified(clan, "records")
    db.session.commit()
    result["success"] = True
    player = User.query.filter(User.id == _id).first()
    result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@clan.route("/donate-equipment", methods=["POST"])
def donate_equipment():
    _id = request.json.get("id")
    login_name = request.json.get("login_name")
    item = int(request.json.get("item"))

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()

    clan = Clan.query.filter(Clan.id == player.clan_member).first()
    item_instance = util.get_item_by_instance_id(item)
    if item_instance["unsold"]:
        result["message"] = "该物品不可转移"
        return json.dumps(result, ensure_ascii=False)
    player.equipments.remove(item)
    flag_modified(player, "equipments")
    clan.equipments.append(item)
    flag_modified(clan, "equipments")
    clan.records.insert(0, {"title": "装备捐赠",
                            "content": "%s向仓库添加了%s" % (
                                player.login_name, util.item_instance_format_name(item_instance)),
                            "time": time.strftime("%Y-%m-%d %H:%M:%S")})
    for member in clan.members:
        if member["id"] == player.id:
            member["put"] += 1
            break
    flag_modified(clan, "members")
    flag_modified(clan, "records")
    db.session.commit()
    result["success"] = True
    player = User.query.filter(User.id == _id).first()
    result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@clan.route("/take-equipment", methods=["POST"])
def take_equipment():
    _id = request.json.get("id")
    login_name = request.json.get("login_name")
    item = int(request.json.get("item"))

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()

    clan = Clan.query.filter(Clan.id == player.clan_member).first()
    if clan.leader == player.id:
        player.equipments.append(item)
        flag_modified(player, "equipments")
        clan.equipments.remove(item)
        flag_modified(clan, "equipments")
        clan.records.insert(0, {"title": "装备索取",
                                "content": "%s从仓库拿走了%s" % (
                                    player.login_name, util.item_instance_format_name(util.get_item_by_instance_id(item))),
                                "time": time.strftime("%Y-%m-%d %H:%M:%S")})
        flag_modified(clan, "records")
        for member in clan.members:
            if member["id"] == player.id:
                member["put"] -= 1
                break
        flag_modified(clan, "members")
    else:
        exist = False
        for req in clan.requests:
            if req["type"] == Clan.TAKE_EQUIPMENT_REQUEST and req["user"] == player.id:
                exist = True
                break
        if not exist:
            clan.requests.append({"type": Clan.TAKE_EQUIPMENT_REQUEST, "user": player.id, "item": item})
            flag_modified(clan, "requests")
        else:
            result["message"] = "你已发起过装备请求，同一时刻最多只能存在一个未处理的请求"
            return json.dumps(result, ensure_ascii=False)

    db.session.commit()
    result["success"] = True
    player = User.query.filter(User.id == _id).first()
    result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@clan.route("/handle-request", methods=["POST"])
def handle_request():
    _id = request.json.get("id")
    login_name = request.json.get("login_name")
    index = int(request.json.get("index"))
    user_id = int(request.json.get("user"))
    _result = request.json.get("result")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()
    clan = Clan.query.filter(and_(Clan.id == player.clan_member, Clan.leader == player.id)).first()
    if clan.requests[index]["user"] != user_id:
        abort(500)
    req = clan.requests.pop(index)
    if req["type"] == Clan.JOIN_CLAN_REQUEST:
        joiner = User.query.filter(User.id == req["user"]).first()
        joiner.clan_request = None
        joiner.clan_member = clan.id if _result else None
        if _result:
            clan.members.append({"id": joiner.id, "role": Clan.ROLE_NORMAL, "donate": 0, "put": 0})
            flag_modified(clan, "members")
        action_str = "接受" if _result else "拒绝"
        joiner.add_notification("战队请求", "你加入%s战队的请求已被%s" % (clan.name, action_str))
        clan.add_record("成员加入" if _result else "处理记录", "%s%s了%s加入战队的请求" % (player.login_name, action_str, joiner.login_name))
    elif req["type"] == Clan.TAKE_EQUIPMENT_REQUEST:
        taker = User.query.filter(User.id == req["user"]).first()
        item = util.get_item_by_instance_id(req["item"])
        if _result and item["instance_id"] in clan.equipments:
            taker.equipments.append(item["instance_id"])
            flag_modified(taker, "equipments")
            clan.equipments.remove(item["instance_id"])
            flag_modified(clan, "equipments")
            for member in clan.members:
                if member["id"] == taker.id:
                    member["put"] -= 1
                    break
            flag_modified(clan, "members")
            clan.add_record("装备索取", "%s从仓库拿走了%s" % (taker.login_name, util.item_instance_format_name(item)))
        action_str = "接受" if _result else "拒绝"
        taker.add_notification("战队请求", "你从战队仓库获取%s的请求已被%s" % (util.item_instance_format_name(item), action_str))
    flag_modified(clan, "requests")

    db.session.commit()
    result["success"] = True
    player = User.query.filter(User.id == _id).first()
    result["data"]["user"] = player.to_json()
    return json.dumps(result, ensure_ascii=False)


@clan.errorhandler(Exception)
def catch_all_except(e):
    db.session.rollback()
    db.session.remove()
    raise e
