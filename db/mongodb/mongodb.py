#!/usr/bin/python3
import pymongo as pm

client = pm.MongoClient('localhost', 27017)
db = client.get_database('mynode')


def initCollection(collection):
    return db.get_collection(collection)
