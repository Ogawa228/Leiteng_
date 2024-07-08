import datetime
import math
import random
import threading

from sqlalchemy.orm.attributes import flag_modified

import utils
from config import *
from tables import User, Match, db


class GlobalService:

    def __init__(self):
        self.totalLock = threading.Lock()

        self.nextMatchId = 1
        self.onlineUserLastUpdateTime = datetime.datetime.now() - datetime.timedelta(days=1)
        self.onlineUsers = 0
        self.idleServers = 0

        self.userTable = {}
        self.matchTable = {}
        self.serverTable = {
            name: {
                "name": name,
                "state": "offline",  # idle, in_match
                "last_tick_time": datetime.datetime.now() - datetime.timedelta(days=1),
                "match_id": -1,
            } for name in CWMM_SERVER_NAMES
        }
        self.poolTable = {}
        for mode in utils.modes:
            self.poolTable[mode["id"]] = {
                "users": [],
                "next_match_time": datetime.datetime.now(),
            }

    def buildActiveData(self, id):
        data = {k: v for k, v in self.userTable[id]["active_data"].items()}
        data["pool_size"] = {}
        for mode in utils.modes:
            data["pool_size"][mode["id"]] = len(self.poolTable[mode["id"]]["users"])

        now = datetime.datetime.now()
        if now > self.onlineUserLastUpdateTime + datetime.timedelta(seconds=ONLINE_INFO_UDPATE_INTERVAL_SECONDS):
            self.onlineUsers = 0
            self.idleServers = 0
            self.onlineUserLastUpdateTime = now
            for user in self.userTable.values():
                if now < user["last_heartbeat_time"] + datetime.timedelta(seconds=HEARTBEAT_ALIVE_SECONDS):
                    self.onlineUsers += 1
                else:
                    if user["is_manual_close"] and user["active_data"]["state"] == "in_pool":
                        self.poolTable[user["active_data"]["pool_match_id"]]["users"].remove(user["id"])
                        user["active_data"]["state"] = "in_lobby"
                        user["active_data"]["pool_match_id"] = -1
            for server in self.serverTable.values():
                if server["state"] == "idle":
                    self.idleServers += 1

        data["online_user_count"] = self.onlineUsers
        data["idle_server_count"] = self.idleServers

        if self.userTable[id]["admin_level"] > 0:
            data["servers"] = [{"name": v["name"], "state": v["state"]} for v in self.serverTable.values()]

        if data["state"] == "in_match":
            data["match"] = {k: v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, datetime.datetime) else v for k, v in
                             self.matchTable[data["pool_match_id"]].items()}

        if data["state"] == "in_pool":
            data["pool"] = utils.dict_convert_time(self.poolTable[data["pool_match_id"]])

        return data

    def cancelMatch(self, id, server_name):
        with self.totalLock:
            if self.userTable[id]["admin_level"] >= 1:
                server = self.serverTable[server_name]
                if server["state"] == "in_match":
                    self.doCancelMatch(server_name, self.matchTable[server["match_id"]]["users"])

        self.receiveHeartBeat(id)

    def doCancelMatch(self, server_name: str, players_return_to_pool):
        server = self.serverTable[server_name]
        if server["state"] == "in_match":
            match = self.matchTable[server["match_id"]]
            server["state"] = "idle"
            server["match_id"] = -1
            server["last_tick_time"] = datetime.datetime.now()
            self.broadcastMessage(BROADCAST_MESSAGE_NAME, "%s的比赛被取消" % server_name)
            self.poolTable[match["mode"]]["next_match_time"] = datetime.datetime.now() + datetime.timedelta(
                seconds=NEXT_MATCH_START_WAIT_SECONDS)

            players_return_to_lobby = [u for u in match["users"] if u not in players_return_to_pool]
            for u in players_return_to_pool:
                self.userTable[u]["active_data"]["state"] = "in_pool"
                self.userTable[u]["active_data"]["pool_match_id"] = match["mode"]
                self.userTable[u]["active_data"]["waited_matches"] += 1
                self.poolTable[match["mode"]]["users"].append(u)
            for u in players_return_to_lobby:
                self.userTable[u]["active_data"]["state"] = "in_lobby"
                self.userTable[u]["active_data"]["pool_match_id"] = -1
            self.matchTable.pop(match["id"])

    def messageCancelMatch(self, server_name: str, guids):
        with self.totalLock:
            server = self.serverTable[server_name]
            if server["state"] == "in_match":
                match = self.matchTable[server["match_id"]]
                users = User.query.filter(User.unique_id.in_(guids)).all()
                joined_users = []
                for user in users:
                    if user.id in match["users"]:
                        joined_users.append(user.id)

                self.doCancelMatch(server_name, joined_users)
        return "1|5"

    def checkMatchFinish(self):
        with self.totalLock:
            matches = [m for m in self.matchTable.values()]
            for match in matches:
                if match["state"] == "show_result" and datetime.datetime.now() > match["show_result_until"]:
                    for u in match["users"]:
                        self.userTable[u]["active_data"]["state"] = "in_lobby"
                        self.userTable[u]["active_data"]["pool_match_id"] = -1
                    for i in self.poolTable[match["mode"]]["users"]:
                        self.userTable[i]["active_data"]["waited_matches"] += 1
                    self.matchTable.pop(match["id"])

    def messageFinishMatch(self, server_name: str, data, team_1_score: int, team_2_score: int):
        with self.totalLock:
            server = self.serverTable[server_name]
            if server["state"] == "in_match":
                match = self.matchTable[server["match_id"]]
                server["state"] = "idle"
                server["match_id"] = -1
                server["last_tick_time"] = datetime.datetime.now()
                self.poolTable[match["mode"]]["next_match_time"] = datetime.datetime.now() + datetime.timedelta(
                    seconds=NEXT_MATCH_START_WAIT_SECONDS + MATCH_RESULT_SHOW_SECONDS)

                data_rearranged = []
                for i in range(0, len(data) // 10):
                    data_rearranged.append(tuple(data[i * 10:i * 10 + 10]))
                guids = [u[0] for u in data_rearranged]
                users = User.query.filter(User.unique_id.in_(guids)).all()
                map_uid_to_id = {}
                map_id_to_user = {}
                result = {
                    "mode": match["mode"],
                    "map": match["map"],
                    "team_1_faction": match["team_1_faction"],
                    "team_2_faction": match["team_2_faction"],
                    "team_1_score": team_1_score,
                    "team_2_score": team_2_score,
                    "team_1": [i for i in match["team_1"]],
                    "team_2": [i for i in match["team_2"]],
                    "statistics": {},
                }
                match["result"] = result
                self.broadcastMessage(BROADCAST_MESSAGE_NAME, "%s的比赛已经结束" % server_name)
                match["state"] = "show_result"
                match["show_result_until"] = datetime.datetime.now() + datetime.timedelta(
                    seconds=MATCH_RESULT_SHOW_SECONDS)
                for u in users:
                    map_uid_to_id[u.unique_id] = u.id
                    map_id_to_user[u.id] = u
                total_damage_team_1 = 0
                total_damage_team_2 = 0
                total_rank_team_1 = 0
                total_rank_team_2 = 0
                for record in data_rearranged:
                    user_id = map_uid_to_id[record[0]]
                    if user_id in match["team_1"]:
                        total_damage_team_1 += record[4]
                        total_rank_team_1 += map_id_to_user[user_id].rank
                    elif user_id in match["team_2"]:
                        total_damage_team_2 += record[4]
                        total_rank_team_2 += map_id_to_user[user_id].rank
                total_damage_team_1 = max(total_damage_team_1, 1)
                total_damage_team_2 = max(total_damage_team_2, 1)
                is3v3 = match["mode"] == 1
                isOpenMap = utils.get_map_by_id(match["map"])["type"] == "open"
                for record in data_rearranged:
                    user_id = map_uid_to_id[record[0]]
                    user = map_id_to_user[user_id]
                    # 计算方法：
                    # total_rank_delta = (20 + 40 * 比分差 / 6) * 每队人数
                    # 开阔图步兵修正系数 inf_buffer = 0.15 * inf_spawn_count / round_count
                    # 实力平衡修正系数 balance_buffer = 1 / (1 + math.exp(-8e-4 * abs(rank_difference))) - 0.5
                    #
                    # 胜方 rank_delta = damage_ratio * total_rank_delta
                    # 负方 rank_delta = (damage_ratio - 1.9 / team_size) * total_rank_delta
                    # 平局 rank_delta = (damage_ratio - 0.9 / team_size) * total_rank_delta
                    # 步兵修正 rank_delta = rank_delta * (1 + inf_buffer) or rank_delta * (1 - inf_buffer)

                    total_rank_delta = (20 + abs(team_1_score - team_2_score) * 40 / 6) * len(match["team_1"])
                    win = 0
                    if team_1_score > team_2_score:
                        if user_id in match["team_1"]:
                            win = 1
                        else:
                            win = -1
                    elif team_1_score < team_2_score:
                        if user_id in match["team_1"]:
                            win = -1
                        else:
                            win = 1
                    if user_id in match["team_1"]:
                        damage_ratio = record[4] / total_damage_team_1
                    else:
                        damage_ratio = record[4] / total_damage_team_2
                    if win == 1:
                        rank_delta = damage_ratio * total_rank_delta
                    elif win == -1:
                        rank_delta = (damage_ratio - 1.9 / len(match["team_1"])) * total_rank_delta
                    else:
                        rank_delta = (damage_ratio - 0.9 / len(match["team_1"])) * total_rank_delta

                    inf_buffer = min(0.15, 0.15 * record[8] / (team_1_score + team_2_score))
                    if isOpenMap and rank_delta > 0:
                        rank_delta = rank_delta * (1 + inf_buffer)
                    elif isOpenMap and rank_delta < 0:
                        rank_delta = rank_delta * (1 - inf_buffer)
                    # rank_difference > 0 表示自己的水平低于对面平均水平
                    if user_id in match["team_1"]:
                        rank_difference = total_rank_team_2 / len(match["team_1"]) - user.rank
                    else:
                        rank_difference = total_rank_team_1 / len(match["team_1"]) - user.rank
                    balance_buffer = 1 / (1 + math.exp(-8e-4 * rank_difference)) - 0.5
                    if rank_delta > 0:
                        # rank_difference>0时balance_buffer>0，多加
                        # rank_difference<0时balance_buffer<0，少加
                        rank_delta = rank_delta * (1 + balance_buffer)
                    elif rank_delta < 0:
                        # rank_difference>0时balance_buffer>0，少扣
                        # rank_difference<0时balance_buffer<0，多扣
                        rank_delta = rank_delta * (1 - balance_buffer)

                    rank_delta = int(rank_delta)
                    new_rank = (user.rank if not is3v3 else user.rank_33) + rank_delta
                    result["statistics"][user_id] = {
                        "stat": record[1:],
                        "rank_change": (user.rank if not is3v3 else user.rank_33, new_rank),
                    }
                    if not is3v3:
                        user.rank += rank_delta
                        if user.rank < 1:
                            user.rank = 1
                        user.match += 1
                        user.kill += record[1]
                        user.death += record[3]
                        if win == 1:
                            user.win += 1
                        elif win == 0:
                            user.even += 1
                        else:
                            user.lose += 1
                        user.damage += record[4]
                        user.team_damage += record[5]
                    else:
                        user.rank_33 += rank_delta
                        if user.rank_33 < 1:
                            user.rank_33 = 1

                match_db = Match()
                match_db.start_time = match["match_start_time"]
                match_db.result = result
                flag_modified(match_db, "result")
                db.session.add(match_db)
                db.session.commit()

                users = User.query.filter(User.id.in_(match["users"])).all()
                user_json = [u.to_query_json() for u in users]
                self.broadcastPacket({"op": "update_user", "args": {"users": user_json}})

        return "1|5"

    def cancelPool(self, id):
        with self.totalLock:
            if self.userTable[id]["active_data"]["state"] == "in_pool":
                self.poolTable[self.userTable[id]["active_data"]["pool_match_id"]]["users"].remove(id)

                self.userTable[id]["active_data"]["state"] = "in_lobby"
                self.userTable[id]["active_data"]["pool_match_id"] = -1

        self.receiveHeartBeat(id)

    def acceptMatch(self, id):
        with self.totalLock:
            if self.userTable[id]["active_data"]["state"] == "in_match":
                match = self.matchTable[self.userTable[id]["active_data"]["pool_match_id"]]
                if match["wait_for_ready_until"] > datetime.datetime.now() and id in match["users"] and \
                        id not in match["ready_users"]:
                    match["ready_users"].append(id)
                    if len(match["ready_users"]) == len(match["users"]):
                        match["map"] = utils.get_random_map_by_mode(match["mode"])
                        self.broadcastMessage(BROADCAST_MESSAGE_NAME, "%s正在选人" % match["server"])
                        # 分配队伍及开始选人
                        users = User.query.filter(User.id.in_(match["users"])).order_by("rank").all()
                        leaders = [users[-1].id]
                        for i in range(len(users) - 2, -1, -1):
                            if users[i].rank == users[-1].rank:
                                leaders.append(users[i].id)
                            else:
                                break
                        if len(leaders) == 1:
                            to_add = [users[-2].id]
                            for i in range(len(users) - 3, -1, -1):
                                if users[i].rank == users[-2].rank:
                                    to_add.append(users[i].id)
                                else:
                                    break
                            leaders.append(random.choice(to_add))
                        elif len(leaders) > 2:
                            random.shuffle(leaders)
                            leaders = leaders[:2]
                        bit = random.randint(0, 1)
                        match["team_1"].append(leaders[bit])
                        match["team_2"].append(leaders[1 - bit])
                        match["state"] = "choose_team"

                        match["choosing_team"] = 1
                        match["choose_num_index"] = 0
                        match["choose_num_current"] = 0
                        match["choose_until"] = datetime.datetime.now() + datetime.timedelta(
                            seconds=MATCH_PICK_TEAMMATE_SECONDS)
                        self.userTable[match["team_1"][0]]["socket"].send(
                            {"op": "play_sound", "args": {"name": "choose.ogg"}})

                        if len(match["users"]) == 2:
                            self.setMatchStart(match)

        self.receiveHeartBeat(id)

    def sendMessage(self, id, message):
        name = User.query.filter(User.id == id).first().username
        with self.totalLock:
            self.broadcastMessage(name, message)

    def broadcastPacket(self, json):
        for user in self.userTable:
            try:
                self.userTable[user]["socket"].send(json)
            except:
                pass

    def broadcastMessage(self, name, message):
        for user in self.userTable:
            try:
                self.userTable[user]["socket"].send(
                    {"op": "send_message", "args": {"message": {"user": name, "message": message}}})
            except:
                pass

    def choosePlayer(self, leader, teammate):
        with self.totalLock:
            if self.userTable[leader]["active_data"]["state"] == "in_match":
                match = self.matchTable[self.userTable[leader]["active_data"]["pool_match_id"]]
                if match["state"] == "choose_team" and match["choosing_team"] == 1 and match["team_1"][0] == leader \
                        and teammate in match["users"] and teammate not in match["team_1"] and \
                        teammate not in match["team_2"] and datetime.datetime.now() < match["choose_until"]:
                    self.matchTeamChoosePlayer(match, 1, teammate)
                elif match["state"] == "choose_team" and match["choosing_team"] == 2 and match["team_2"][0] == leader \
                        and teammate in match["users"] and teammate not in match["team_1"] and \
                        teammate not in match["team_2"] and datetime.datetime.now() < match["choose_until"]:
                    self.matchTeamChoosePlayer(match, 2, teammate)

        self.receiveHeartBeat(leader)

    def messageServerMatchStatus(self, name):
        # 1|距离下次tick时间（秒）
        message = "1|10"

        start_match = False
        with self.totalLock:
            if self.serverTable.get(name) is not None:
                server = self.serverTable[name]
                server["last_tick_time"] = datetime.datetime.now()
                if server["state"] == "offline":
                    server["state"] = "idle"
                if server["state"] == "idle":
                    message = "1|20"
                elif server["state"] == "in_match" and self.matchTable[server["match_id"]]["state"] != "in_game":
                    message = "1|3"
                else:
                    start_match = True
        if start_match:
            message = self.messageStartMatch(server["match_id"])

        return message

    # 2|模式ID|场景ID|1队国家|2队国家|每队人数|射手限制|步兵限制|骑兵限制|等待时间|Match ID
    def messageStartMatch(self, match_id):
        message = "1|3"
        with self.totalLock:
            match = self.matchTable[match_id]

            limit = utils.get_map_mode_limit(match["map"], match["mode"])

            message = "2|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d" % (
                match["mode"], match["map"], match["team_1_faction"] + 14, match["team_2_faction"] + 14,
                utils.get_mode_by_id(match["mode"])["count"], limit[0], limit[1], limit[2],
                MATCH_WAIT_START_SECONDS, match["id"])

        return message

    def messagePlayerStatus(self, server_name, user_id, player_index):
        message = ""
        with self.totalLock:
            if self.userTable.get(user_id) is not None and self.userTable[user_id]["active_data"][
                "state"] == "in_match" and \
                    self.matchTable[self.userTable[user_id]["active_data"]["pool_match_id"]]["state"] == "in_game" and \
                    self.matchTable[self.userTable[user_id]["active_data"]["pool_match_id"]]["server"] == server_name:
                if user_id in self.matchTable[self.userTable[user_id]["active_data"]["pool_match_id"]]["team_1"]:
                    message = "7|%d|1" % player_index
                elif user_id in self.matchTable[self.userTable[user_id]["active_data"]["pool_match_id"]]["team_2"]:
                    message = "7|%d|2" % player_index
        return message

    def startPool(self, id, mode_id):
        with self.totalLock:
            if self.userTable[id]["active_data"]["state"] == "in_lobby":
                if (not ALLOW_TEST_MODES_FOR_EVERYONE) and self.userTable[id]["admin_level"] == 0 and mode_id in (4, 5):
                    self.userTable[id]["socket"].send({"op": "alert", "args": {"message": "测试接口，禁止使用"}})
                else:
                    self.userTable[id]["active_data"]["state"] = "in_pool"
                    self.userTable[id]["active_data"]["pool_match_id"] = mode_id
                    self.userTable[id]["active_data"]["waited_matches"] = 0

                    self.poolTable[mode_id]["users"].append(id)

                    self.startPossibleMatch(mode_id)

        self.receiveHeartBeat(id)

    def startPossibleMatch(self, mode_id):
        if len(self.poolTable[mode_id]["users"]) >= utils.get_mode_by_id(mode_id)["count"] * 2 \
                and datetime.datetime.now() > self.poolTable[mode_id]["next_match_time"] \
                and len([v for v in self.serverTable.values() if
                         v["state"] == "idle" or (ALLOW_OFFLINE_SERVERS and v["state"] == "offline")]) > 0:
            match = {
                "id": self.nextMatchId,
                "mode": mode_id,
                "map": -1,
                "team_1_faction": random.randint(1, 5),
                "team_2_faction": 0,
                "server": random.choice(
                    [k for k in self.serverTable.keys() if
                     self.serverTable[k]["state"] == "idle" or (
                             ALLOW_OFFLINE_SERVERS and self.serverTable[k]["state"] == "offline")]),
                "users": [],
                "ready_users": [],
                "state": "wait_for_ready",
                "wait_for_ready_until": datetime.datetime.now() + datetime.timedelta(
                    seconds=MATCH_WAIT_READY_SECONDS),
                "team_1": [],
                "team_2": [],
                "choosing_team": 1,
                "choose_num_index": 0,
                "choose_num_current": 0,
                "choose_until": datetime.datetime.now(),
                "result": {},
                "show_result_until": datetime.datetime.now(),

                "match_start_time": datetime.datetime.now(),
            }
            team_2_faction = random.choice([i for i in range(1, 6) if i != match["team_1_faction"]])
            if team_2_faction == 3:
                team_2_faction = 6
            match["team_2_faction"] = team_2_faction
            if match["team_1_faction"] == 3:
                match["team_1_faction"] = 6
            self.serverTable[match["server"]]["state"] = "in_match"
            self.serverTable[match["server"]]["match_id"] = match["id"]
            self.nextMatchId += 1
            target_count = utils.get_mode_by_id(mode_id)["count"] * 2
            user_count_waited_matches = {}
            user_waited_matches = {}
            max_waited_matches = 0
            for i in self.poolTable[mode_id]["users"]:
                waited_matches = self.userTable[i]["active_data"]["waited_matches"]
                max_waited_matches = max(max_waited_matches, waited_matches)
                if user_count_waited_matches.get(waited_matches) is None:
                    user_count_waited_matches[waited_matches] = 1
                    user_waited_matches[waited_matches] = [i]
                else:
                    user_count_waited_matches[waited_matches] += 1
                    user_waited_matches[waited_matches].append(i)
            for m in range(max_waited_matches, -1, -1):
                if len(match["users"]) + user_count_waited_matches.get(m, 0) <= target_count:
                    match["users"].extend(user_waited_matches.get(m, []))
                elif user_count_waited_matches.get(m) > 0:
                    users_chosen_from = [i for i in user_waited_matches[m]]
                    random.shuffle(users_chosen_from)
                    match["users"].extend(users_chosen_from[:target_count - len(match["users"])])
                elif len(match["users"]) >= target_count:
                    break
            assert len(match["users"]) == target_count

            for u in match["users"]:
                self.poolTable[mode_id]["users"].remove(u)
                self.userTable[u]["socket"].send({"op": "play_sound", "args": {"name": "ready.mp3"}})
                self.userTable[u]["active_data"]["state"] = "in_match"
                self.userTable[u]["active_data"]["pool_match_id"] = match["id"]
                self.userTable[u]["active_data"]["waited_matches"] += 1

            for u in self.poolTable[mode_id]["users"]:
                self.userTable[u]["active_data"]["waited_matches"] += 1

            self.matchTable[match["id"]] = match

    def matchTeamChoosePlayer(self, match, team_id, player_id):
        match["team_%d" % team_id].append(player_id)
        match["choose_num_current"] += 1
        match["choose_until"] = datetime.datetime.now() + datetime.timedelta(
            seconds=MATCH_PICK_TEAMMATE_SECONDS)
        if match["choose_num_current"] >= utils.get_mode_by_id(match["mode"])["choose"][match["choose_num_index"]]:
            match["choosing_team"] = 1 if team_id == 2 else 2
            match["choose_num_current"] = 0
            if len(match["team_1"]) + len(match["team_2"]) == len(match["users"]):
                self.setMatchStart(match)
                return
            else:
                match["choose_num_index"] += 1
        self.userTable[match["team_%d" % match["choosing_team"]][0]]["socket"].send(
            {"op": "play_sound", "args": {"name": "choose.ogg"}})

    def setMatchStart(self, match):
        match["state"] = "in_game"
        match["match_start_time"] = datetime.datetime.now()

    def setManualClose(self, id):
        with self.totalLock:
            if self.userTable.get(id) is not None:
                self.userTable[id]["is_manual_close"] = True

    def addUserConnection(self, id, ws):
        with self.totalLock:
            user = User.query.filter(User.id == id).first()
            active_data = {
                "state": "in_lobby",  # in_lobby, in_pool, in_match
                "pool_match_id": -1,
                "waited_matches": 0,
            }
            if self.userTable.get(id) is not None:
                self.userTable[id]["socket"].send({"op": "relogin"})
                active_data = self.userTable[id]["active_data"]

            self.userTable[id] = {
                "id": id,
                "socket": ws,
                "last_heartbeat_time": datetime.datetime.now() - datetime.timedelta(days=1),
                "admin_level": user.admin_level,
                "is_manual_close": False,
                "active_data": active_data,
            }
            self.broadcastMessage(BROADCAST_MESSAGE_NAME,
                                  "%s%s上线了" % ("管理员" if user.admin_level > 0 else "", user.username))

        self.receiveHeartBeat(id)

    def checkMatchChoose(self):
        with self.totalLock:
            matches = [self.matchTable[i] for i in self.matchTable.keys()]
            for match in matches:
                if match["state"] == "choose_team" and datetime.datetime.now() > match["choose_until"]:
                    remaining = []
                    for i in match["users"]:
                        if i not in match["team_1"] and i not in match["team_2"]:
                            remaining.append(i)

                    from main import app
                    with app.app_context():
                        users = User.query.filter(User.id.in_(remaining)).order_by("rank").all()
                        highest = [int(users[-1].id)]
                        for i in range(len(users) - 2, -1, -1):
                            if users[i].rank == highest[0]:
                                highest.append(int(users[i].id))
                            else:
                                break
                        db.session.remove()
                    self.matchTeamChoosePlayer(match, match["choosing_team"], random.choice(highest))

    def checkMatchReady(self):
        with self.totalLock:
            matches = [self.matchTable[i] for i in self.matchTable.keys()]
            for match in matches:
                if match["state"] == "wait_for_ready" and ((len(match["ready_users"]) < len(match["users"])
                                                            and datetime.datetime.now() > match[
                                                                "wait_for_ready_until"]) or
                                                           (len(match["ready_users"]) >= len(match["users"])
                                                            and datetime.datetime.now() > match[
                                                                "wait_for_ready_until"] + datetime.timedelta(
                                                                       seconds=3))):
                    for u in match["users"]:
                        if u in match["ready_users"]:
                            self.userTable[u]["active_data"]["state"] = "in_pool"
                            self.userTable[u]["active_data"]["pool_match_id"] = match["mode"]
                            self.userTable[u]["active_data"]["waited_matches"] += 1
                            self.poolTable[match["mode"]]["users"].append(u)
                        else:
                            self.userTable[u]["active_data"]["state"] = "in_lobby"
                            self.userTable[u]["active_data"]["pool_match_id"] = -1
                    self.serverTable[match["server"]]["state"] = "idle"
                    self.serverTable[match["server"]]["match_id"] = -1
                    self.matchTable.pop(match["id"])

    def receiveHeartBeat(self, id):
        with self.totalLock:
            self.userTable[id]["last_heartbeat_time"] = datetime.datetime.now()
            active_data = self.buildActiveData(id)
        self.userTable[id]["socket"].send(
            {"op": "heart_beat_received", "args": {"active_data": active_data}})

    def checkMatchStart(self):
        with self.totalLock:
            for mode in utils.modes:
                self.startPossibleMatch(mode["id"])

    def checkServerOffline(self):
        with self.totalLock:
            for server in self.serverTable.values():
                if server["state"] == "idle" and datetime.datetime.now() > \
                        server["last_tick_time"] + datetime.timedelta(seconds=SERVER_TICK_IDLE_SECONDS):
                    server["state"] = "offline"

    def removeUserConnection(self, id):
        with self.totalLock:
            if self.userTable.get(id) is not None:
                self.userTable[id]["socket"].send({"op": "relogin"})


globalService = GlobalService()


def checkMatchReady():
    globalService.checkMatchFinish()
    globalService.checkMatchStart()
    globalService.checkMatchReady()
    globalService.checkMatchChoose()
    globalService.checkServerOffline()
