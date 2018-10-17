class HelloWorldService(object):
    def __init__(self):
        self.fail_test = False

    def set_fail_test(self, fail_test):
        self.fail_test = fail_test

    def get_hello_world_message(self):
        return 'Hello world' if not self.fail_test else 'Fail'
