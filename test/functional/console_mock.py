#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from mock import Mock

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dirname, '..', '..'))

from app.app_kernel import AppKernel # noqa
from phoopy.console import Application # noqa
from cleo.inputs.argv_input import ArgvInput # noqa

_input = ArgvInput()

env = _input.get_parameter_option('--env', 'dev')
debug = True if 'dev' == env else False

kernel = AppKernel(env, debug)

# Mocks
hello_world_service = Mock(['get_hello_world_message'])
hello_world_service.get_hello_world_message.return_value = 'Hello World'

dependencies = {
    'hello_world_service': lambda c: hello_world_service,
}

kernel.boot()
container = kernel.get_container()

for (key, value) in dependencies.items():
    container[key] = value

application = Application(kernel)
application.run(_input)
