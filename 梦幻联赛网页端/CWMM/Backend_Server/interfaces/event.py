import json

from flask import Blueprint, request, abort

from tables import *

event = Blueprint('event', __name__)


@event.route("/get-event-list", methods=["GET"])
def get_event_list():
    _id = int(request.args.get("id"))
    login_name = request.args.get("login_name")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()
    events = [event.to_json(player.id) for event in Event.query.all()]
    events.reverse()
    result["success"] = True
    result["data"]["events"] = events
    return json.dumps(result, ensure_ascii=False)


@event.route("/create-event", methods=["POST"])
def create_event():
    _id = request.json.get("id")
    login_name = request.json.get("login_name")
    title = request.json.get("title")
    content = request.json.get("content")
    start_time = datetime.datetime.strptime(request.json.get("start_time"), "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(request.json.get("end_time"), "%Y-%m-%d %H:%M:%S")
    choices = request.json.get("choices")

    result = {"success": False, "message": "", "data": {}}
    if start_time < datetime.datetime.now() + datetime.timedelta(minutes=-10):
        result["message"] = "开始时间不能早于现在"
        return json.dumps(result, ensure_ascii=False)
    if end_time < start_time + datetime.timedelta(days=1):
        result["message"] = "持续时间最少1天"
        return json.dumps(result, ensure_ascii=False)

    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()
    if player.admin_level < 2:
        abort(500)
    event = Event()
    event.title = title
    event.content = content
    event.start_time = start_time
    event.end_time = end_time
    event.choices = [str(choice) for choice in choices]
    db.session.add(event)
    Notification.add_public_announcement(
        "投注活动%s已发布，持续时间：%s ~ %s" % (
            title, start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S")))
    db.session.commit()
    events = [event.to_json(player.id) for event in Event.query.all()]
    events.reverse()
    result["success"] = True
    result["data"]["events"] = events
    return json.dumps(result, ensure_ascii=False)


@event.route("/vote-event", methods=["POST"])
def vote_event():
    _id = request.json.get("id")
    login_name = request.json.get("login_name")
    event_id = int(request.json.get("event_id"))
    choice = request.json.get("choice")
    gold = int(request.json.get("gold"))
    comment = request.json.get("comment")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()
    if player.gold < gold:
        abort(500)
    if player.round < 10:
        result["message"] = "你至少需要在游戏内游玩10局才能下注"
        return json.dumps(result, ensure_ascii=False)
    event = Event.query.filter(Event.id == event_id).first()
    if not event.is_active():
        abort(500)
    player.gold -= gold
    event.votes[str(_id)] = {"index": event.choices.index(choice), "gold": gold, "comment": comment}
    flag_modified(event, "votes")
    db.session.commit()
    events = [event.to_json(player.id) for event in Event.query.all()]
    events.reverse()
    result["success"] = True
    result["data"]["events"] = events
    result["data"]["user"] = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first().to_json()
    return json.dumps(result, ensure_ascii=False)


@event.route("/end-event", methods=["POST"])
def end_event():
    _id = request.json.get("id")
    login_name = request.json.get("login_name")
    event_id = int(request.json.get("event_id"))
    choice = request.json.get("choice")

    result = {"success": False, "message": "", "data": {}}
    player = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first()
    if player.admin_level < 2:
        abort(500)
    event = Event.query.filter(Event.id == event_id).first()
    if event.result is not None or event.start_time > datetime.datetime.now():
        abort(500)
    event.result = event.choices.index(choice)

    # win_index, total_share, win_share
    win_index = event.result
    total_share = 0
    win_share = 0
    for v in event.votes.values():
        total_share += v["gold"]
        if v["index"] == win_index:
            win_share += v["gold"]
    if win_share != 0:
        rate = total_share / win_share
        for k, v in event.votes.items():
            cur_player = User.query.filter(User.id == int(k)).first()
            if v["index"] == win_index:
                cur_player.gold += v["gold"] * rate
                cur_player.add_notification("酒馆活动结束",
                                            "酒馆活动%s已结束，你为%s投注了%d金币，最终赔率为%.2f，从而赢得了%d金币" % (
                                                event.title, event.choices[v["index"]], v["gold"], rate, v["gold"] * rate))
            else:
                cur_player.add_notification("酒馆活动结束",
                                            "酒馆活动%s已结束，你为%s投注了%d金币，很遗憾没有压中结果" % (event.title, event.choices[v["index"]], v["gold"]))

    db.session.commit()
    events = [event.to_json(player.id) for event in Event.query.all()]
    events.reverse()
    result["success"] = True
    result["data"]["events"] = events
    result["data"]["user"] = User.query.filter(and_(User.id == _id, User.login_name == login_name)).first().to_json()
    return json.dumps(result, ensure_ascii=False)


@event.errorhandler(Exception)
def catch_all_except(e):
    db.session.rollback()
    db.session.remove()
    raise e
