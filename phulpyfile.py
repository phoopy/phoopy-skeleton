from os import system, unlink
from os.path import dirname, join
import xml.etree.ElementTree as ET
from phulpy import task, Output
from time import sleep


@task
def test(phulpy):
    phulpy.start(['lint', 'unit_test', 'functional_test'])


@task
def lint(phulpy):
    result = system('flake8 src')
    if result:
        raise Exception('lint test failed')


@task
def unit_test(phulpy):
    result = system(
        'pytest --cov-report term-missing'
        + ' --cov-report xml --cov=src test'
    )
    if result:
        raise Exception('Unit tests failed')
    coverage_path = join(dirname(__file__), 'coverage.xml')
    xml = ET.parse(coverage_path).getroot()
    unlink(coverage_path)
    if float(xml.get('line-rate')) < 1:
        raise Exception('Unit test is not fully covered')


@task
def functional_test(phulpy):
    server = phulpy.execute('bin/console server:start --port=8080 --debug', quiet=True, sync=False)
    Output.out(Output.colorize('Starting web server (waiting 5 seconds)', 'yellow'))
    sleep(5)

    BASE_URL = 'localhost:8080'
    result = system('BASE_URL={} behave --no-capture --no-capture-stderr test/functional'.format(BASE_URL))
    server.kill()

    if result:
        raise Exception('Functional tests failed')


@task
def clean(phulpy):
    system('find . -name \'*.pyc\' -delete')
