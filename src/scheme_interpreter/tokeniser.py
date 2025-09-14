test_case = '(string-append "Hello" " " "world")'

if test_case:
    print("test_case:", test_case)
else:
    print("No test case provided.")


def tokenise(input: str) -> list[str]:
    def regular_tokeniser(input: str) -> list[str]:
        return input.replace("(", " ( ").replace(")", " ) ").strip().split()

    def quoted_pair_tokeniser(input: str) -> list[str]:
        first_quote = input.find('"')
        second_quote = input.find('"', first_quote + 1)

        pre_quoted_substring = input[:first_quote]
        quoted_substring_preserved = input[first_quote : second_quote + 1]
        post_quoted_substring = input[second_quote + 1 :]

        result = []
        if pre_quoted_substring.strip():
            result.extend(regular_tokeniser(pre_quoted_substring))
        result.append(quoted_substring_preserved)
        if post_quoted_substring.strip():
            result.extend(tokenise(post_quoted_substring))
        return result

    if not input:
        return []
    if '"' not in input:
        return regular_tokeniser(input)
    if input.count('"') % 2 != 0:
        # Unpaired quotes - so handle as regular tokens
        return regular_tokeniser(input)

    return quoted_pair_tokeniser(input)


print("tokeniser_output:", tokenise(test_case))
