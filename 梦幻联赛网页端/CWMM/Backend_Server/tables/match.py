from sqlalchemy import *

from .base import db


class Match(db.Model):
    __tablename__ = "match"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 需要存储的数据有：模式，地图，双方玩家，比分，玩家数据，玩家排位分变动
    result = Column(JSON, nullable=False)
    start_time = Column(DateTime, nullable=False)

    def to_json(self):
        result = {}
        for k, v in self.__dict__.items():
            if k not in ("_sa_instance_state",):
                result[k] = v

        result["start_time"] = None if self.start_time is None else self.start_time.strftime("%Y-%m-%d %H:%M:%S")

        return result
