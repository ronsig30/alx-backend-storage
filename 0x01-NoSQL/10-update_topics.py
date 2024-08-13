#!/usr/bin/env python3
""" 10-update_topics """


def update_topics(mongo_collection, name, topics):
    """Updates the topics of a school document.

    Args:
        mongo_collection (pymongo.collection.Collection): The pymongo collectio
        n object.
        name (str): The name of the school to update.
        topics (list of str): The list of topics to set.

    Returns:
        None
    """
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
