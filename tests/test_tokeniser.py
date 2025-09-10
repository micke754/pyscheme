def test_tokenise_single_number():
    from scheme_interpreter.tokeniser import tokenise

    result = tokenise("123")
    expected = ["123"]
    assert result == expected


def test_tokenise_different_single_number():
    from scheme_interpreter.tokeniser import tokenise

    result = tokenise("42")
    expected = ["42"]
    assert result == expected


def test_tokenise_extra_white_space():
    from scheme_interpreter.tokeniser import tokenise

    result = tokenise("42 ")
    expected = ["42"]
    assert result == expected
