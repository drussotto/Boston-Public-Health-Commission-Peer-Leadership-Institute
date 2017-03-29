class ExampleCollection(object):
    def __init__(self):
        self.data = {}
    def add(self, **kwargs):
        self.data.update(kwargs)
    def __getattr__(self, attr):
        return self.data[attr]
