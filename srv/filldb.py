import redis
import json
from redis.commands.json.path import Path

# pip3 install redis
# redis-cli
# service redis-server start

redis_db=redis.Redis()

f=open("products.json","r")
content=json.load(f)

for i in content:
    print(str(i))
    redis_db.mset({str(i["product_name"]):str(i)})
    

