import re
import sys
import os
import base64
import subprocess
from collections import namedtuple
from behave import when, then
from pytest import register_assert_rewrite
from behave_web_api.steps import *  # noqa

register_assert_rewrite()

dirname = os.path.dirname(os.path.realpath(__file__))
console_path = os.path.realpath(os.path.join(dirname, '..', 'console_mock.py'))
CommandResult = namedtuple('CommandResult', ['stdout', 'stderr', 'exit_code'])


class CommandRunner(object):
    def __init__(self, name, arguments=None):
        self.__name = name
        self.__arguments = arguments if arguments is not None else []
        self.__result = None
        self.__process = None

    def __build_command_line(self):
        line = [console_path]
        line.append(self.__name)
        for argument in self.__arguments:
            line.append(argument)
        line.append('--env=test')
        return line

    def __check_run(self):
        if not self.__result:
            if not self.__process:
                self.run()
            stdout, stderr = self.__process.communicate()
            self.__result = CommandResult(stderr, stderr, self.__process.returncode)

    def __remove_shell_codes(self, text):
        esc = r'\x1b'
        csi = esc + r'\['
        osc = esc + r'\]'
        cmd = '[@-~]'
        st = esc + r'\\'
        bel = r'\x07'
        pattern = '(' + csi + '.*?' + cmd + '|' + osc + '.*?' + '(' + st + '|' + bel + ')' + ')'
        return re.sub(pattern, '', text)

    def get_stdout(self):
        self.__check_run()
        return self.__remove_shell_codes(self.__result.stdout.decode('utf-8'))

    def get_stderr(self):
        self.__check_run()
        return self.__remove_shell_codes(self.__result.stderr.decode('utf-8'))

    def get_exit_code(self):
        self.__check_run()
        return self.__result.exit_code

    def run(self):
        self.__process = subprocess.Popen(
            self.__build_command_line(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def kill(self):
        self.__process.kill()


def get_command_runner(context):
    if not hasattr(context, 'command_runner'):
        raise Exception('Command must be setup before asserts')
    return context.command_runner


def assert_contains(searched_text, all_text):
    regex = re.escape(searched_text).replace('\\\n', r'\s*\n\s*')
    match = re.search(regex, all_text)
    assert match is not None, '{} don\'t contains {}.\n'.format(repr(all_text), repr(searched_text))


@when(u'I run the command "{}"')
def i_run_the_command(context, name):
    context.command_runner = CommandRunner(name)


@when(u'I run the command "{}" with arguments')
def i_run_the_command_with_arguments(context, name):
    arguments = context.text.splitlines()
    context.command_runner = CommandRunner(name, arguments)


@when(u'I run the command "{}" with base64 argument')
def i_run_the_command_with_base64_argument(context, name):
    arguments = [base64.b64encode(context.text.encode('utf-8')).decode('utf-8')]
    context.command_runner = CommandRunner(name, arguments)


@then(u'the command exit code should be {code:d}')
def the_command_exit_code_should_be(context, code):
    runner = get_command_runner(context)
    assert code == runner.get_exit_code()


@then(u'print stdout')
def then_print_stdout(context):
    sys.stdout.write(get_command_runner(context).get_stdout())
    sys.stdout.flush()


@then(u'print stderr')
def then_print_stderr(context):
    sys.stdout.write(get_command_runner(context).get_stderr())
    sys.stdout.flush()


@then(u'the stdout should contain')
def the_stdout_should_contain(context):
    runner = get_command_runner(context)
    assert_contains(context.text, runner.get_stdout())


@then(u'the stderr should contain')
def the_stderr_should_contain(context):
    runner = get_command_runner(context)
    assert_contains(context.text, runner.get_stderr())


@then(u'the file "{}" should contain')
def the_file_should_contain(context, path):
    text = open(path, 'r').read()
    assert_contains(context.text, text)
