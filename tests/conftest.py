from pytest import fixture
from calculator import ExpressionCalculator


def pytest_addoption(parser):
    parser.addoption('--source', action='store', dest='source')
    parser.addoption('--target', action='store', dest='target')


@fixture(scope='module')
def source(request):
    return request.config.getoption("--source")


@fixture(scope='module')
def target(request):
    return request.config.getoption("--target")


@fixture(scope='module')
def calculator(source, target):
    return ExpressionCalculator(source, target, '.xml')
