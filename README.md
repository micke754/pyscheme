# PyScheme

A Python implementation of the Scheme programming language, built as a learning project to master Python's standard library and Test-Driven Development (TDD).

## Goals

- **Short-term**: Implement the BSL (Beginning Student Language) subset of Scheme
- **Medium-term**: Support  Revised^5 Report on the Algorithmic Language Scheme otherwise known as R5RS (ambitious)
- **Long-term**: Target R7RS-small compliance (unlikely)

## Learning Focus

This project serves as a deep dive into:
- Python standard library mastery
- Test-Driven Development practices
- Language implementation concepts
- Functional programming principles

## Current Status

🚧 **Work in Progress** - Currently implementing the tokenizer using TDD

## Getting Started

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run the interpreter (when implemented)
uv run pyscheme
```

## Project Structure

```
src/scheme_interpreter/    # Core implementation
tests/                     # TDD test suite
docs/                      # Learning documentation
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

MIT License

Copyright (c) 2025 [Your Full Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

