#!/usr/bin/env python3
"""
Log stats
"""
from pymongo import MongoClient


def log_stats(mongo_collection):
    """ The top 10 of the most present IPs in the collection nginx of the database logs """
    print(f"{mongo_collection.count_documents({})} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    print(f"{mongo_collection.count_documents({'method': 'GET', 'path': '/status'})} status check")
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    ips = mongo_collection.aggregate(pipeline)
    for ip in ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    log_stats(collection)
