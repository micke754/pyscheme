import pytest
from scheme_interpreter.parser import parse_expression, number_node, symbol_node


# Symbols
@pytest.mark.parametrize(
    "input_tokens",
    [
        ("+"),
        ("%"),
        ('"Hello"'),
        ("string-append"),
    ],
)
def test_parse_symbols(input_tokens: str):
    """
    Parse symbol tokens into symbol nodes.
    Symbols are names like +, hello, first-name
    """
    tokens = [input_tokens]
    result_node, new_position = parse_expression(tokens, 0)
    assert result_node == symbol_node(input_tokens)
    assert new_position == 1


# Numbers
@pytest.mark.parametrize(
    "input_tokens",
    [
        (42),
        (123),
        (3.14),
        (-42),
    ],
)
def test_parse_single_number_variants(input_tokens):
    tokens = [input_tokens]
    result_node, new_position = parse_expression(tokens, 0)
    assert result_node == number_node(input_tokens)
    assert new_position == 1
