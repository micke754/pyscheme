def number_node(value: float) -> dict:
    return {"type": "number", "name": value}


def symbol_node(name: str) -> dict:
    return {"type": "symbol", "name": name}


def list_node(elements: list) -> dict:
    return {"type": "list", "elements": elements}


class ParseError(Exception):
    """Parsing error"""

    pass


def is_number(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False


def parse_number(tokens: list[str], position: int) -> tuple:
    """
    Parse a number token.

    Returns: (number_node, new_position)
    """
    if position >= len(tokens):
        raise ParseError("Unexpected end of input")

    token = tokens[position]
    if not is_number(token):
        raise ParseError(f"Expected number, got {token}")

    node = number_node(float(token))
    new_position = position + 1
    return node, new_position


def parse_symbol(tokens: list[str], position: int) -> tuple:
    """
    Parse a symbol token.
    Returns: (symbol_node, new_position)
    """
    if position >= len(tokens):
        raise ParseError("Unexpected end of the input")

    token = tokens[position]
    node = symbol_node(token)
    new_position = position + 1
    return node, new_position


def parse_list(tokens: list, position: int) -> tuple:
    """
    Parse a list expression: (element1 element2 ...)
    Returns: (list_node, new_position)
    """

    if position >= len(tokens) or tokens[position] != "(":
        raise ParseError("Expected opening parenthesis")

    # Skip opening parenthesis
    position += 1
    elements = []

    # Parse elements until closing parenthesis
    while position < len(tokens) and tokens[position] != ")":
        element_node, position = parse_expression(
            tokens, position
        )  # Recursion?
        elements.append(element_node)

    # Check for closing parenthesis
    if position >= len(tokens):
        raise ParseError("Missing closing parenthesis")

    # Skip closing parenthesis
    position += 1

    return list_node(elements), position


def parse_expression(tokens: list[str], position: int) -> tuple:
    """
    Parse one expression starting at position

    Returns: (ast_node, new_position)
    - ast_node: the parsed_expression
    - new_position: Where to continue parsing
    """
    if position >= len(tokens):
        raise ParseError("Unexpected end of input")

    token = tokens[position]

    if token == "(":
        return parse_list(tokens, position)
    elif is_number(token):
        return parse_number(tokens, position)
    else:
        return parse_symbol(tokens, position)
