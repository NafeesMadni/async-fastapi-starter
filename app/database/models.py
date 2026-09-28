from sqlalchemy import Column, Integer, Sequence, String

from app.database import db


class User(db.Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(255))
    email = Column(String(40))
