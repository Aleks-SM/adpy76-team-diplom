import sqlalchemy as sq
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = sq.Column(sq.BigInteger, primary_key=True)
    user_name = sq.Column(sq.String(length=50), unique=True)
    search_gender = sq.Column(sq.Integer)
    search_age_min = sq.Column(sq.Integer, nullable=False)
    search_age_max = sq.Column(sq.Integer, nullable=False)
    search_city = sq.Column(sq.String(length=50))
    state = sq.Column(sq.Integer)

class Favorite(Base):
    __tablename__ = "favorite"

    favorite_id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.BigInteger, sq.ForeignKey("user.user_id"), nullable=False)
    favorite_vk_user_id = sq.Column(sq.BigInteger, nullable=True)

    favorite = relationship(User, backref="user_fav")

class Blacklist(Base):
    __tablename__ = "blacklist"

    blacklist_id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.BigInteger, sq.ForeignKey("user.user_id"), nullable=False)
    blocked_vk_user_id = sq.Column(sq.Integer, nullable=True)

    user = relationship(User, backref="user_black")
