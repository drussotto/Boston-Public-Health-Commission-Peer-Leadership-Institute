from bson import ObjectId

# This function is necessary because we need to use the mongomock ObjectId
# when in the tests, and the bson one when not. This setup is done before the
# app runs, and the config is overwritten during testing with the mongomock
# version.
def init_help(app):
    app.config["object_id"] = ObjectId
