import pytest
from scheme_interpreter.tokeniser import tokenise


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("42", ["42"]),
        ("123", ["123"]),
        ("-42", ["-42"]),
        ("3.12", ["3.12"]),
        ("3.12 -1 22", ["3.12", "-1", "22"]),
    ],
)
def test_tokenise_atom_number(input_text: str, expected: list[str]):
    result = tokenise(input_text)
    assert result == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("42 ", ["42"]),
        (" 123 ", ["123"]),
        ("  -42", ["-42"]),
        ("  3.12    ", ["3.12"]),
    ],
)
def test_tokenise_white_space(input_text: str, expected: list[str]):
    result = tokenise(input_text)
    assert result == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("", []),
        (" ", []),
    ],
)
def test_tokenise_empty_list(input_text: str, expected: list[str]):
    result = tokenise(input_text)
    assert result == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        (
            "(+ 1 2)",
            [
                "(",
                "+",
                "1",
                "2",
                ")",
            ],
        ),
        (
            "(+ (* 1 2) 2)",
            [
                "(",
                "+",
                "(",
                "*",
                "1",
                "2",
                ")",
                "2",
                ")",
            ],
        ),
    ],
)
def test_tokenise_parentheses(input_text: str, expected: list[str]):
    result = tokenise(input_text)
    assert result == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        (
            "(display 1 2)",
            [
                "(",
                "display",
                "1",
                "2",
                ")",
            ],
        ),
        (
            '(display "Hello world")',
            [
                "(",
                "display",
                '"Hello world"',
                ")",
            ],
        ),
        (
            '(string-append "Hello" " " "world")',
            [
                "(",
                "string-append",
                '"Hello"',
                '" "',
                '"world"',
                ")",
            ],
        ),
    ],
)
def test_tokenise_string(input_text: str, expected: list[str]):
    result = tokenise(input_text)
    assert result == expected
