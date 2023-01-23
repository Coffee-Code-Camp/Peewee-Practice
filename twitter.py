import datetime
from peewee import *

import logging

logger = logging.getLogger("peewee")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


db = SqliteDatabase("twitter.sqlite")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = TextField(index=True)


class Tweet(BaseModel):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref="tweets")


class Favorite(BaseModel):
    user = ForeignKeyField(User, backref="favorites")
    tweet = ForeignKeyField(Tweet, backref="favorites")


def populate_test_data():
    db.create_tables([User, Tweet, Favorite])

    data = (
        ("huey", ("meow", "hiss", "purr")),
        ("mickey", ("woof", "whine")),
        ("zaizee", ()),
    )
    for username, tweets in data:
        user = User.create(username=username)
        for tweet in tweets:
            Tweet.create(user=user, content=tweet)

    # Populate a few favorites for our users, such that:
    favorite_data = (
        ("huey", ["whine"]),
        ("mickey", ["purr"]),
        ("zaizee", ["meow", "purr"]),
    )
    for username, favorites in favorite_data:
        user = User.get(User.username == username)
        for content in favorites:
            tweet = Tweet.get(Tweet.content == content)
            Favorite.create(user=user, tweet=tweet)


def show_all_tweets_n_plus_one():
    tweets = Tweet.select()
    for tweet in tweets:
        print(f"{tweet.user.username}: {tweet.content}")


def show_all_tweets_prefetch():
    tweets = Tweet.select()
    users = User.select()
    users_with_tweets = prefetch(users, tweets)
    for user in users_with_tweets:
        for tweet in user.tweets:
            print(f"{user.username}: {tweet.content}")


def get_tweets_based_on_username(username):
    return Tweet.select().join(User).where(User.username == username)


def insert_multiple_tweets(user_id, *tweets):
    user = User.get(User.id == user_id)
    with db.atomic() as txn:
        counter = 0
        for tweet in tweets:
            if counter >= 2:
                raise Exception("Some exception")
            Tweet.create(user=user, content=tweet)
            counter += 1


def get_tweets_based_on_user_id_sql_injection(user_id):
    return Tweet.select().join(User).where(SQL("user_id = %s" % user_id))


if __name__ == "__main__":
    tweets = get_tweets_based_on_user_id_sql_injection("3 or 1 == 1")
    print(list(tweets))
