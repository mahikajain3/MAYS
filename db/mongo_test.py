import pymongo as pm

client = pm.MongoClient()
print("client")

insert_ret = client['dbName']['users'].insert_one({'foo': 'bar'})
print("insert_ret")

docs = client['dbName']['users'].find()
print("docs")
for doc in docs:
    print("docs")

db = client["dbName"]
print(db)
