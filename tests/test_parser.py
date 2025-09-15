from scheme_interpreter.parser import parse_expression, number_node


def test_parse_single_number():
    tokens = ["42"]
    position = 0

    result_node, new_position = parse_expression(tokens, position)

    expected_node = number_node(42)
    assert result_node == expected_node

    assert new_position == 1
