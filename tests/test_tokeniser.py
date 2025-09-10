def test_tokenise_single_number():
    from scheme_interpreter.tokeniser import tokenise

    result = tokenise("42")
    expected = ["42"]
    assert result == expected
