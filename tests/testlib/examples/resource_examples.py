from mongomock import ObjectId

resource1 = {
    "_id" : ObjectId(),
    "link": "http://google.com",
    "name": "Google",
    "category": "sexual health",
    "type": "student",
    "active": True
}

resource2 = {
    "_id" : ObjectId(),
    "link": "http://example.com",
    "name": "Example.com",
    "category": "wellness",
    "type": "peerleader",
    "active": True
}

resource3 = {
    "_id" : ObjectId(),
    "link": "http://notareal.business",
    "name": "We ran out of examples",
    "category": "wellness",
    "type": "peerleader",
    "active": False 
}

ex.add(
    resource1=resource1,
    resource2=resource2,
    resource3=resource3
)

def add_mocked_resources(db):
    db.resources.insert_many([resource1, resource2, resource3])
