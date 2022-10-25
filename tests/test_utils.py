from aiogram_tests.utils import camel_case2snake_case


def test_camle_case_convertor():
    snake_case = camel_case2snake_case("camelCase")
    assert snake_case == "camel_case"
    snake_case = camel_case2snake_case("CamelCase")
    assert snake_case == "camel_case"
    snake_case = camel_case2snake_case("CamelCaseCase")
    assert snake_case == "camel_case_case"
