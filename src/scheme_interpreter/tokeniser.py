test_case = '(string-append "Hello", " ", "world")'

if test_case:
    print("test_case:", test_case)
else:
    print("No test case provided.")


def tokenise(input: str) -> list[str]:
    def regular_tokeniser(input: str) -> list[str]:
        return input.replace("(", " ( ").replace(")", " ) ").strip().split()

    def quoted_pair_tokeniser(input: str) -> list[str]:
        quote_indices = [i for i, c in enumerate(input) if c == '"']
        quoted_substring_preserved = input[quote_indices[0] : quote_indices[1] + 1]
        pre_quoted_substring = input[: quote_indices[0]]
        post_quoted_substring = input[quote_indices[1] + 1 :]
        return (
            regular_tokeniser(pre_quoted_substring)
            + [quoted_substring_preserved]
            + tokenise(post_quoted_substring)  # Recursive composition
        )

    if not input:
        return []
    if '"' not in input:
        return regular_tokeniser(input)

    quote_count = input.count('"')
    if quote_count % 2 == 0:
        # Unpaired quotes - so handle as regular tokens
        return regular_tokeniser(input)

    return regular_tokeniser(input)


print("tokeniser_output:", tokenise(test_case))
