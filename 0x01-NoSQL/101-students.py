#!/usr/bin/env python3
""" 101-students """


def top_students(mongo_collection):
    """
    Returns all students sorted by average score in descending order.
    """
    # Aggregate pipeline to compute average score and sort by it
    pipeline = [
        {
            "$addFields": {
                "averageScore": {
                    "$divide": [
                        {"$sum": "$topics.score"},
                        {"$size": "$topics"}
                    ]
                }
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]

    # Execute the aggregation pipeline
    result = mongo_collection.aggregate(pipeline)

    # Convert the cursor to a list and return
    return list(result)
