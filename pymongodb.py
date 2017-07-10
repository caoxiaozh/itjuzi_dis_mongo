import pymongo

client = pymongo.MongoClient('localhost',28002,replicaset='hardy')
db = client['hardy']
cols = db.col
for col in cols.find({'x': {'$lt': 50.0}}).sort('x', pymongo.DESCENDING):
    print(col)

cols.insert({'x': 1000.0})
print(cols.count())
