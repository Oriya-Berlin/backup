from create_tables import *
from sqlalchemy.sql import exists
from sqlalchemy import and_
import datetime


# get all followers of specific shooter, return array
def get_all_followers_from_DB(follow_at_name):

    followers_list = []
    result = session.query(Followers).filter_by(follow_at_name=follow_at_name).all()
    for res in result:
        followers_list.append(res.follower_name)

    return followers_list


# insert new follower to 'Followers' table
def insert_follower_to_DB(follower_name, follow_at_name):

    if not is_he_in_my_followers(follower_name, follow_at_name):
        new_follower = Followers()
        new_follower.follower_name = follower_name
        new_follower.follow_at_name = follow_at_name
        new_follower.effected_by_bot = False
        session.add(new_follower)
        session.commit()
        session.close()
    else:
        return


# insert new target to the 'Targets' table
def insert_target_to_DB(target_name, shooter_name, boolean):
    new_target = Targets()
    new_target.target_name = target_name
    new_target.shooter_name = shooter_name
    new_target.target_followed_date = datetime.datetime.now()
    new_target.story_watched = boolean
    new_target.is_following_canceled = False
    session.add(new_target)
    session.commit()
    session.close()


# boolean, check if that user is in 'Followers' table under specific shooter
def is_he_in_my_followers(follower_name, follow_at_name):  # check if that target, is in the followers table [under the shooter]
    exist = session.query(exists().where(and_(Followers.follower_name==follower_name, Followers.follow_at_name==follow_at_name))).scalar()
    return exist


# boolean, check if that user is in 'Targets' table under specific shooter
def is_he_in_my_targets(target_name, shooter_name):
    exist = session.query(exists().where(and_(Targets.target_name==target_name, Targets.shooter_name==shooter_name))).scalar()
    return exist


# takes an array as a parameter, and return filtered array - without users that already in our targets/followers table
def filter_target_list(target_list, shooter):
    filtered_list = []
    for target in target_list:
        if is_he_in_my_followers(target, shooter):
            continue
        elif is_he_in_my_targets(target, shooter):
            continue
        else:
            filtered_list.append(target)
    return filtered_list


# return array, with all bot successes of specific shooter
def get_bot_successes_list(shooter):
    result = session.query(Followers).filter(Followers.follow_at_name==shooter, Followers.effected_by_bot==True).all()
    successes_list = []
    for res in result:
        successes_list.append(res.follower_name)
    return successes_list


# return pairs: {name, date}
def get_bot_successes_dic(shooter):
    result = session.query(Followers).filter(Followers.follow_at_name == shooter, Followers.effected_by_bot == True).all()
    successes_list = []

    for res in result:
        dic = {'name': f'{res.follower_name}', 'date': f'{res.date_of_success}'}
        successes_list.append(dic)

    return successes_list


# update 'effected_by_bot' column in 'Followers' table, if the target became our follower
def update_bot_successes(shooter):
    all_followers = session.query(Followers).filter(Followers.follow_at_name==shooter).all()
    for follower in all_followers:
        if is_he_in_my_targets(follower.follower_name, shooter):
            follower.effected_by_bot = True
            target_details = session.query(Targets).\
                filter(and_(Targets.shooter_name==shooter, Targets.target_name==follower.follower_name)).one()

            follower.date_of_success = target_details.target_followed_date
            session.commit()


# boolean, check the difference between current date, to the date we start to follow on some target
def check_date_diff(diff, bot_action_date):  # maybe we need to add 'shooter' and 'target' column as a parameters
    now = datetime.datetime.now()
    delta = (now - bot_action_date).days
    if delta > diff:
        return True
    return False


#
def get_expired_targets(shooter, diff):  # need to test that
    expired_targets_list = []
    result = session.query(Targets).filter_by(shooter_name=shooter, is_following_canceled=False).all()
    for res in result:
        if check_date_diff(diff, res.target_followed_date):
            expired_targets_list.append(res.target_name)
    return expired_targets_list


#
def change_target_status(target_name, shooter):  # need to test that
    user = session.query(Targets).filter_by(shooter_name=shooter, target_name=target_name)
    user.is_following_canceled = True
    session.commit()


#
def delete_follower_from_DB(follower, shooter):
        session.query(Followers).filter_by(follower_name=follower, follow_at_name=shooter).delete()
        session.commit()


# insert new target to 'OnHoldTargets' table
def insert_target_to_OnHold_table(target_name, has_taken_from, shooter_name):
    if not is_he_in_my_followers(target_name, shooter_name):
        if is_he_in_my_targets(target_name, shooter_name):
            new_target = OnHoldTargets()
            new_target.name = target_name
            new_target.shooter_name = shooter_name
            new_target.has_taken_from = has_taken_from
            new_target.is_iterated = False
            session.add(new_target)
            session.commit()
            session.close()


# will return 500 'on-hold' target of specific shooter
def get_targets_from_OnHold_table(shooter):  # need to test that
    waiting_list = []
    counter = 0
    all_shooters_waiting_targets = session.query(OnHoldTargets).filter_by(shooter_name=shooter, is_iterated=False).all()
    for i in all_shooters_waiting_targets:
        if counter > 500:
            break
        waiting_list.append(i.name)
        counter = counter + 1
    return waiting_list


'''
update_bot_successes('ben_liba')
x = get_bot_successes('ben_liba')
print(x)
print(len(x))
'''
