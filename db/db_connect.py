"""
This file contains some common MongoDB code.
"""
import os
import json
import pymongo as pm
import bson.json_util as bsutil


# all of these will eventually be put in the env:
user_nm = "aliahjefree"
cloud_svc = "cluster0.bslxs.mongodb.net"
passwd = os.environ.get("MONGO_PASSWD", '')
cloud_mdb = "mongodb+srv"
db_params = "retryWrites=true&w=majority"
db_nm = "maysDB"


if os.environ.get("TEST_MODE", ''):
    db_nm = "test_maysDB"

REMOTE = "0"
LOCAL = "1"

client = None


def get_client():
    """
    This provides a uniform way to get the client across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    """
    global client
    if os.environ.get("LOCAL_MONGO", REMOTE) == LOCAL:
        print("Connecting to Mongo locally.")
        client = pm.MongoClient()
    else:
        print("Connecting to Mongo remotely.")
        client = pm.MongoClient(f"mongodb+srv://aliahjefree:{passwd}\
@cluster0.bslxs.mongodb.net/{db_nm}?retryWrites=true&w=majority")
    return client


def fetch_one(collect_nm, filters={}):
    """
    Fetch one record that meets filters.
    """
    return client[db_nm][collect_nm].find_one(filters)


def update_one(collect_nm, filters={}, updates={}):
    """
    Update one record that meets filters.
    """
    return client[db_nm][collect_nm].update_one(filters, updates)


def del_one(collect_nm, filters={}):
    """
    Delete one record that meets filters.
    """
    return client[db_nm][collect_nm].delete_one(filters)


def fetch_all(collect_nm, key_nm, filters={}):
    all_docs = {}
    for doc in client[db_nm][collect_nm].find(filters):
        # print(all_docs['netid'])
        # print(doc)
        if key_nm not in doc:
            print(f"doc={doc}")
            return all_docs
        all_docs[doc[key_nm]] = json.loads(bsutil.dumps(doc))
    return all_docs


def all_docs(collect_nm, filters={}):
    docs = []
    for doc in client[db_nm][collect_nm].find(filters):
        # print(all_docs['netid'])
        # print(doc)
        docs.append(json.loads(bsutil.dumps(doc)))
    return docs


def insert_doc(collect_nm, doc, filters={}):
    client[db_nm][collect_nm].insert_one(doc, filters)


def rename(db_nm: str, collect_nm: str, nm_map: dict):
    """    Renames specified fields on all documents in a collection.
    Parameters
    ----------
    db_nm: str
    The database name.
    collect_nm: str
    The name of the database collection.
    nm_map: dict
    A dictionary. The keys are the current field names.
    Each key maps to the desired field name:
    {
        "old_nm1": "new_nm1",
        "old_nm2": "new_nm2",
        }
    """
    collect = client[db_nm][collect_nm]
    return collect.update_many({},
                               {'$rename': nm_map})
