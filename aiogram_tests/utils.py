import re


def camel_case2snake_case(var: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", var).lower()
