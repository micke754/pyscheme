def tokenise(input: str) -> list[str]:
    if not input:
        return []
    return input.replace("(", " ( ").replace(")", " ) ").strip().split()
