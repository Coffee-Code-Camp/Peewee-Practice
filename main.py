from peewee import *
from datetime import date

import logging

logger = logging.getLogger("peewee")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# Open a database connection
db = SqliteDatabase("db.sqlite")


# Models
class Customer(Model):
    name = CharField()
    email = CharField()
    is_active = BooleanField(default=True)

    class Meta:
        database = db


class Order(Model):
    customer = ForeignKeyField(Customer, backref="orders")
    date = DateField()

    class Meta:
        database = db


# Initiating DB
def initiate_db():
    db.connect()
    db.create_tables([Customer, Order])
    print(" Database Initiated ".center(50, "-"))
    print("\n\n")


# CRUD operations
def create_customer(name, email):
    customer_count = Customer.select().where(Customer.email == email).count()
    if not customer_count:
        customer = Customer(name=name, email=email)
        customer.save()


def read_users(name=None, email=None):
    query = Customer.select()
    if name is not None:
        query = query.where(Customer.name == name)
    if email is not None:
        query = query.where(Customer.email == email)
    return list(query)


def read_user(name=None, email=None):
    query = Customer.select()
    if name is not None:
        query = query.where(Customer.name == name)
    if email is not None:
        query = query.where(Customer.email == email)
    return query.get()


def get_user_by_email(email):
    try:
        return Customer.get(email=email)
    except Customer.DoesNotExist:
        return None


def delete_user(user_id):
    c = Customer.select().where(Customer.id == user_id).get()
    c.delete_instance()


def change_name(customer_id, name):
    c = Customer.select().where(Customer.id == customer_id).get()
    c.name = name
    c.save()


def change_email(customer_id, email):
    c = Customer.select().where(Customer.id == customer_id).get()
    c.email = email
    c.save()


def create_order_for_user(user_id):
    c = Customer.select().where(Customer.id == user_id).get()
    o = Order(customer=c, date=date.today())
    o.save()
    return o


def print_user_orders(user_id):
    c = Customer.select().where(Customer.id == user_id).get()
    for o in c.orders:
        print(o.id)


# Main
if __name__ == "__main__":
    initiate_db()
    print_user_orders(2)
