#!/usr/bin/env python3
""" 9-insert_school """


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document into a collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The pymongo collectio
        n object.
        **kwargs: The fields and values to include in the new document.

    Returns:
        str: The _id of the newly inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return str(result.inserted_id)
