"""Seed file for feedback db"""

from models import User, db
from app import app

db.drop_all()
db.create_all()

# Users
a = User.register('test1','testpwd1', 'test1@test1.com', 'first1', 'last1')

b = User.register('test2','testpwd2', 'test2@test2.com', 'first2', 'last2')

c = User.register('test3','testpwd3', 'test3@test3.com', 'first3', 'last3')

d = User.register('test4','testpwd4', 'test4@test4.com', 'first4', 'last4')

e = User.register('test5','testpwd5', 'test5@test5.com', 'first5', 'last5')

# add and commit
db.session.add_all([a, b, c, d, e])
db.session.commit()