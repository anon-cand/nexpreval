from calculator import ExpressionCalculator

def test_calculator_fixture(calculator):
    assert isinstance(calculator, ExpressionCalculator)

# def test_process(calculator):
#     reference = request.config.getoption('--target')