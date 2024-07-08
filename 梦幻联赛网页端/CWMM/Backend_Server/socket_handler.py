import datetime
import json
import traceback

from sqlalchemy import *

from service import globalService
from tables import User


class SocketHandler:

    def __init__(self, ws):
        self.socket = ws
        self.user_id = -1

    def run(self):
        while True:
            buf = self.socket.receive()
            if buf is None:
                continue
            try:
                data = json.loads(buf)
                op = data["op"]
                args = data.get("args")
                if op == "connect":
                    user = User.query.filter(and_(
                        and_(User.id == int(args["id"]), User.username == args["username"]),
                        User.password == args["password"])).first()
                    if user is None or (
                            user.ban_until_time is not None and user.ban_until_time > datetime.datetime.now()):
                        self.send({"op": "relogin"})
                    else:
                        self.user_id = user.id
                        globalService.addUserConnection(user.id, self)
                elif op == "heart_beat":
                    globalService.receiveHeartBeat(self.user_id)
                elif op == "start_pool":
                    globalService.startPool(self.user_id, int(args["mode_id"]))
                elif op == "cancel_pool":
                    globalService.cancelPool(self.user_id)
                elif op == "accept_match":
                    globalService.acceptMatch(self.user_id)
                elif op == "choose_player":
                    globalService.choosePlayer(self.user_id, int(args["user"]))
                elif op == "send_message":
                    globalService.sendMessage(self.user_id, args["message"])
                elif op == "cancel_match":
                    globalService.cancelMatch(self.user_id, args["server"])
                elif op == "manual_close":
                    globalService.setManualClose(self.user_id)
            except:
                from main import logger
                logger.info(traceback.format_exc())
                break

    def send(self, js):
        try:
            self.socket.send(json.dumps(js))
        except:
            pass

    def close(self):
        self.socket.close()
