from sqlalchemy import Column, Integer, String

from app.database import db


class User(db.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(40))
