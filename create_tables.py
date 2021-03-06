from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Followers(Base):
    __tablename__ = "followers"

    id = Column('id', Integer, primary_key=True)
    follower_name = Column('follower_name', String, unique=False)
    follow_at_name = Column('follow_at_name', String, unique=False)
    effected_by_bot = Column('effected_by_bot', Boolean, default=False)
    date_of_success = Column('date_of_success', Date, default=None)

    def __str__(self):
        return self.follower_name


class Targets(Base):
    __tablename__ = "targets"

    id = Column('id', Integer, primary_key=True)
    target_name = Column('target_name', String)
    target_followed_date = Column('target_followed_date', Date)
    shooter_name = Column('shooter_name', String)
    story_watched = Column('story_watched', Boolean, default=False)
    is_following_canceled = Column('is_following_canceled', Boolean, default=False)

    def __str__(self):
        return self.target_followed_date


# -------------------------------------------------------
# need to delete that table
class PotentialTargets(Base):
    __tablename__ = "potentialtargets"

    id = Column('id', Integer, primary_key=True)
    potential_target = Column('potential_target', String)
    take_from_page = Column('take_from_page', String)
    description = Column('description', String)
# -------------------------------------------------------


class OnHoldTargets(Base):
    __tablename__ = "onholdtargets"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    has_taken_from = Column('has_taken_from', String)  # follower of who
    shooter_name = Column('shooter_name', String)
    is_iterated = Column('is_iterated', Boolean, default=False)


class HighPotentialTargets(Base):
    __tablename__ = "highpotentialtargets"

    id = Column('id', Integer, primary_key=True)
    potential_target_name = Column('potential_target_name', String)
    followers_following_ratio = Column('followers_following_ratio', Float)
    follow_request_received_counter = Column('follow_request_received_counter', Integer, default=0)
    return_follower_counter = Column('return_follower_counter', Integer, default=0)
    return_received_ratio = Column('return_received_ratio', Float, default=0)


engine = create_engine('sqlite:///ig_bot.db', echo=True)
#Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()


'''
def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}')

is_following_canceled = Column('is_following_canceled', Boolean, default=False)
add_column(engine, 'targets', is_following_canceled)
'''




