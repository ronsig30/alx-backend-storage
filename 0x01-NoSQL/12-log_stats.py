#!/usr/bin/env python3
""" 12-log_stats.py """

from pymongo import MongoClient


def main():
    """Display statistics about Nginx logs from MongoDB."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    clctn = db.nginx

    # Total number of documents
    total_logs = clctn.count_documents({})
    print(f"{total_logs} logs")

    # Count documents by method
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print("Methods:")
    for method in methods:
        method_count = clctn.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Count documents with method=GET and path=/status
    status_check = clctn.count_documents({"method": "GET", "path": "/statu s"})
    print(f"{status_check} status check")


if __name__ == "__main__":
    main()
