from sqlalchemy import Column, BigInteger, Integer, String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String(length=50))
    search_gender = Column(Integer)
    search_age_min = Column(Integer)
    search_age_max = Column(Integer)
    search_city = Column(String(length=50))
    state = Column(Integer)


class Favorite(Base):
    __tablename__ = "favorite"

    favorite_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    favorite_vk_user_id = Column(BigInteger, nullable=True)

    favorite = relationship(User, backref="user_fav")


class Blacklist(Base):
    __tablename__ = "blacklist"

    blacklist_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    blocked_vk_user_id = Column(Integer, nullable=True)

    user = relationship(User, backref="user_black")
