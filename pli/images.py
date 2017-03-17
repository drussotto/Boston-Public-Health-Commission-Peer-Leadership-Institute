from service_util import get_gridfs

# Returns a file-like object which will stream the image binary
# And a content-type. 2-tuple
def get_img_file(img_id):
    grid_out = get_gridfs().get(img_id)
    if grid_out is None:
        return (None, None)
    return grid_out, grid_out.content_type

# Given a file-like object for the image bytes,
# and a content-type returns an ObjectId to the newly created
# image in gridfs
def add_new_img(stream, content_type):
    return get_gridfs().put(stream.read(), content_type=content_type, encoding="UTF-8")
