#!/usr/bin/env python3
""" 102-log_stats """

from pymongo import MongoClient


def log_stats():
    """
    Provides statistics about Nginx logs stored in MongoDB.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    n = db.nginx

    # Count total logs
    total_logs = n.count_documents({})

    # Count logs per method
    methods_count = n.aggregate([
        {"$group": {"_id": "$method", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "method": "$_id", "count": 1}},
        {"$sort": {"method": 1}}
    ])

    # Count status check logs
    stats_check_count = n.count_documents({"method": "GET", "path": "/status"})

    # Count IPs and get top 10
    ip_counts = n.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    # Print results
    print(f"{total_logs} logs")
    print("Methods:")

    methods = {method['method']: method['count'] for method in methods_count}
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        print(f"\tmethod {method}: {methods.get(method, 0)}")

    print(f"{stats_check_count} status check")
    print("IPs:")
    for ip in ip_counts:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()
