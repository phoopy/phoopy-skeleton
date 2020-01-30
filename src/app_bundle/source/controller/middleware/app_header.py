from time import time


def app_header():
    def decorate(fn):
        def inner(self, *args, **kwargs):
            kwargs['time'] = str(time())  # add the time before enter in the controller

            return fn(self, *args, **kwargs)

        return inner

    return decorate
