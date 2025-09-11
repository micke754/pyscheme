test_case = '(display "hello world")'


def tokenise(input: str) -> list[str]:
    if not input:
        return []
    if '"' in input:
        return input.replace("(", " ( ").replace(")", " ) ").split(sep="\t")

    return input.replace("(", " ( ").replace(")", " ) ").strip().split()


print(tokenise(test_case))
