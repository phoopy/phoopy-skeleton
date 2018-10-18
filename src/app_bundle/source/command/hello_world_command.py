# -*- coding: utf-8 -*-

from phoopy.console import AbstractCommand


class HelloWorldCommand(AbstractCommand):
    """
    Hello World Command

    app:hello_world
        {required_arg : Some required argument}
        {non_required_arg? : Some non required argument}
        {--option=5 : Some option that defaults to 5}
    """
    def __init__(self, logger, root_path, hello_world_service):
        super(HelloWorldCommand, self).__init__(logger)
        self.root_path = root_path
        self.hello_world_service = hello_world_service

    def handle(self):
        self.setup_logger()

        self.success(self.hello_world_service.get_hello_world_message())

        output_data = '\n'.join([
            'required_arg {}'.format(self.argument('required_arg')),
            'non_required_arg {}'.format(self.argument('non_required_arg')),
            'option {}'.format(self.option('option')),
            'root_path {}'.format(self.root_path),
            ''
        ])

        output_path = '{}/var/{}'.format(self.project_path, 'hello_world')
        self.info(output_data)
        open(output_path, 'w').write(output_data)
