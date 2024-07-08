import datetime
import random
from functools import cmp_to_key
from hashlib import sha256

from config import *


def password_hash(password: str, salt: int):
    return sha256((str(salt) + "|" + password).encode()).hexdigest()


def random_verify():
    return randbytes(3).hex()


def randbytes(length):
    result = b""
    for i in range(length):
        result += random.randint(0, 0xff).to_bytes(1, "little", signed=False)
    return result


def dict_convert_time(dic):
    result = {}
    for k, v in dic.items():
        if isinstance(v, datetime.datetime):
            result[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(v, dict):
            result[k] = dict_convert_time(v)
        else:
            result[k] = v
    return result


def is_server_name_valid(name):
    return name in CWMM_SERVER_NAMES


def get_map_mode_limit(map_id, mode_id):
    m = get_map_by_id(map_id)
    mode = get_mode_by_id(mode_id)
    return mode["limit"][m["type"]].copy()


def get_random_map_by_mode(mode_id):
    pool = current_map_pool[mode_id]
    # type_name = pool["types"][pool["current_type_index"]]
    type_name = random.choice(["open", "closed", "closed"]) if mode_id in (2, 3) else random.choice(pool["types"])
    if len(pool["maps"][type_name]) == 0:
        for m in maps:
            if m["type"] == type_name:
                for n in m["modes"]:
                    if n == mode_id:
                        pool["maps"][type_name].append(m["id"])
                        break
        random.shuffle(pool["maps"][type_name])
    pool["current_type_index"] = (pool["current_type_index"] + 1) % len(pool["types"])
    return pool["maps"][type_name].pop()


def str_convert_to_game(msg: str):
    result = ""
    for c in msg:
        if c.isascii():
            result += c
        else:
            result += c + " "
    return result


def get_map_by_id(id):
    for m in maps:
        if m["id"] == id:
            return m


def get_mode_by_id(id):
    for mode in modes:
        if mode["id"] == id:
            return mode


def get_leaderboard() -> (datetime.datetime, list):
    global update_time, leaderboard
    from tables import User
    now = datetime.datetime.now()
    if update_time + datetime.timedelta(seconds=LEADERBOARD_UPDATE_INTERVAL_SECONDS) < now:
        players = User.query.filter(User.match > 0).all()

        def cmp(a, b):
            a_score = a.rank
            b_score = b.rank
            if a_score < b_score:
                return -1
            if a_score > b_score:
                return 1
            return 0

        players.sort(key=cmp_to_key(cmp), reverse=True)
        update_time = now
        leaderboard = [player.to_leaderboard_json() for player in players]
    return update_time, leaderboard


def init_map_pool():
    for m in maps:
        for mode in m["modes"]:
            if m["type"] not in current_map_pool[mode]["types"]:
                current_map_pool[mode]["types"].append(m["type"])
            if current_map_pool[mode]["maps"].get(m["type"]) is None:
                current_map_pool[mode]["maps"][m["type"]] = [m["id"]]
            else:
                current_map_pool[mode]["maps"][m["type"]].append(m["id"])

    for mode in modes:
        mode_id = mode["id"]
        current_map_pool[mode_id]["current_type_index"] = random.randint(0, len(current_map_pool[mode_id]["types"]) - 1)
        for t in current_map_pool[mode_id]["types"]:
            random.shuffle(current_map_pool[mode_id]["maps"][t])


modes = MATCH_MODES
maps = MAPS

current_map_pool = {mode["id"]: {"types": [], "maps": {}, "current_type_index": 0} for mode in modes}
init_map_pool()

# d = {"open": 0, "closed": 0}
# for _ in range(1000):
#    d[get_map_by_id(get_random_map_by_mode(3))["type"]] += 1
# print(d)

update_time = datetime.datetime.now() + datetime.timedelta(days=-100)
leaderboard = []
