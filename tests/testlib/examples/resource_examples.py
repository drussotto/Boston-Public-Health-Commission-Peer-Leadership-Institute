from mongomock import ObjectId

resource1 = {
    "_id" : ObjectId(),
    "link": "http://google.com",
    "name": "Google",
    "category": "sexual health",
<<<<<<< HEAD
    "rtype": "student",
=======
    "type": "student",
>>>>>>> 04f4b69... Testing for resource endpoints
    "active": True
}

resource2 = {
    "_id" : ObjectId(),
    "link": "http://example.com",
    "name": "Example.com",
    "category": "wellness",
<<<<<<< HEAD
    "rtype": "peerleader",
=======
    "type": "peerleader",
>>>>>>> 04f4b69... Testing for resource endpoints
    "active": True
}

resource3 = {
    "_id" : ObjectId(),
    "link": "http://notareal.business",
    "name": "We ran out of examples",
    "category": "wellness",
<<<<<<< HEAD
    "rtype": "peerleader",
=======
    "type": "peerleader",
>>>>>>> 04f4b69... Testing for resource endpoints
    "active": False 
}

ex.add(
    resource1=resource1,
    resource2=resource2,
    resource3=resource3
)

def add_mocked_resources(db):
    db.resources.insert_many([resource1, resource2, resource3])
