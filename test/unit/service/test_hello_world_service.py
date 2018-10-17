from src.app_bundle.source.service import HelloWorldService


class TestHelloWorldService(object):

    def test_is_not_none(self):
        assert HelloWorldService is not None

    def test_constructor(self):
        service = HelloWorldService()
        assert service is not None

    def test_fail(self):

        service = HelloWorldService()
        service.set_fail_test(True)

        assert 'Fail' == service.get_hello_world_message()

        service.set_fail_test(False)
        assert 'Hello world' == service.get_hello_world_message()
