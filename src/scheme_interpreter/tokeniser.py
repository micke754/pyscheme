test_case = '(string-append "Hello", " ", "world")'


def tokenise(input: str) -> list[str]:
    def regular_tokeniser(input: str) -> list[str]:
        return input.replace("(", " ( ").replace(")", " ) ").strip().split()

    if not input:
        return []

    if '"' in input:
        quote_indices = [i for i, c in enumerate(input) if c == '"']
        substring_preserved = input[quote_indices[0] : quote_indices[1] + 1]
        substring1 = input[: quote_indices[0]]
        substring2 = input[quote_indices[1] + 1 :]

        return (
            regular_tokeniser(substring1)
            + [substring_preserved]
            + regular_tokeniser(substring2)
        )

    return regular_tokeniser(input)


print(tokenise(test_case))
