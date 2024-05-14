#!/usr/bin/env python3
""" Top students """


def top_students(mongo_collection):
    """function that returns all students sorted by average score.
    """
    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {"_id": "$_id", "name": {"$first": "$name"}, "averageScore": {"$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1}}
    ]
    top_students = mongo_collection.aggregate(pipeline)
    return list(top_students)
