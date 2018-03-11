class singleton:

    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kw):
        if self.instance is None:
            self.instance = self.klass(*args, **kw)
        return self.instance
