import re


def camel_case2snake_case(var: str) -> str:
    return re.sub("([A-Z]+)", r"_\1", var).lower()
