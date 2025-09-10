# Phase 1: TDD Deep Dive - Building a Tokenizer

## Understanding TDD Philosophy

### **The TDD Mantra: Red-Green-Refactor**

**Red**: Write a failing test (forces you to think about what you want)
**Green**: Write the simplest code to make it pass (forces minimal implementation)
**Refactor**: Improve the code while keeping tests green (forces clean design)

This isn't just about testing - it's about **design through examples**.

## Setting Up the Learning Environment

### **Project Structure**
```
scheme-interpreter/
├── .python-version        # pypy@3.11
├── pyproject.toml         # UV configuration
├── src/
│   └── scheme_interpreter/
│       └── __init__.py    # Package initialization
├── tests/
│   └── test_tokenizer.py  # Test files
└── README.md
```

### **Initial Commands**
```bash
# Set up project (if not done)
uv init scheme-interpreter
cd scheme-interpreter
uv python pin pypy@3.11
uv add --dev pytest

# Verify setup works
uv run pytest --version
```

## TDD Cycle 1: The Absolute Simplest Case

### **Step 1: Red - Write Your First Failing Test**

```python
# tests/test_tokenizer.py
def test_tokenize_single_number():
    """
    Learning goal: Start with the simplest possible case
    
    Why this test first?
    - Numbers are atomic in Scheme - can't be broken down further
    - No edge cases to worry about yet
    - Clear, unambiguous expected behavior
    """
    from scheme_interpreter.tokenizer import tokenize
    
    result = tokenize("42")
    expected = ["42"]
    
    assert result == expected
```

**Run the test and watch it fail:**
```bash
uv run pytest tests/test_tokenizer.py -v

# Expected output:
# ImportError: No module named 'src.tokenizer'
```

**Learning Points:**
- **Test fails for the right reason** - we haven't written the code yet
- **Test is focused** - tests exactly one behavior
- **Test is readable** - clear what we expect to happen

### **Step 2: Green - Minimal Implementation**

```python
# src/scheme_interpreter/tokenizer.py
def tokenize(text: str) -> list[str]:
    """
    Learning goal: Write the MINIMUM code to pass the test
    
    Resist the urge to over-engineer! Don't think about:
    - Multiple numbers
    - Parentheses  
    - Edge cases
    
    Just make THIS test pass.
    """
    return ["42"]
```

**Run the test again:**
```bash
uv run pytest tests/test_tokenizer.py -v

# Expected output:
# test_tokenizer.py::test_tokenize_single_number PASSED
```

**Learning Points:**
- **Hardcoding is OK at this stage** - we're proving the test works
- **Don't solve future problems** - solve exactly the problem at hand
- **Green is green** - doesn't matter how ugly the implementation is

### **Step 3: Refactor - But There's Nothing to Refactor Yet!**

Our code is too simple to need refactoring. This is normal for the first cycle.

**Commit this milestone:**
```bash
git add .
git commit -m "Add tokenizer - handles single number '42'"
```

## TDD Cycle 2: Force Generalization

### **Step 1: Red - Add a Test That Breaks Current Implementation**

```python
# tests/test_tokenizer.py (add to existing file)
def test_tokenize_different_single_number():
    """
    Learning goal: Force generalization of hardcoded solution
    
    This test will break our hardcoded return ["42"]
    """
    from scheme_interpreter.tokenizer import tokenize
    
    result = tokenize("123")
    expected = ["123"]
    
    assert result == expected
```

**Run tests:**
```bash
uv run pytest tests/test_tokenizer.py -v

# test_tokenize_single_number PASSED
# test_tokenize_different_single_number FAILED
```

**Learning Points:**
- **New test forces us to generalize** - can't hardcode anymore
- **Old test still passes** - regression safety
- **Failing for the right reason** - expected ["123"], got ["42"]

### **Step 2: Green - Simplest Generalization**

```python
# src/scheme_interpreter/tokenizer.py
def tokenize(text: str) -> list[str]:
    """
    Learning goal: Simplest change to make both tests pass
    
    What's the minimal change? Just return the input as a single-item list.
    """
    return [text.strip()]
```

**Run tests:**
```bash
uv run pytest tests/test_tokenizer.py -v

# Both tests should pass now
```

**Learning Points:**
- **Generalized just enough** - both tests pass
- **Still not handling multiple tokens** - we'll let future tests drive that
- **Used .strip()** - good defensive programming, handles whitespace

## TDD Cycle 3: Multiple Tokens

### **Step 1: Red - Test Multiple Numbers**

```python
# tests/test_tokenizer.py (add to existing)
def test_tokenize_multiple_numbers():
    """
    Learning goal: Drive out space-separated parsing
    
    This forces us to actually split on whitespace
    """
    from scheme_interpreter.tokenizer import tokenize
    
    result = tokenize("1 2 3")
    expected = ["1", "2", "3"]
    
    assert result == expected
```

**Run tests - this will fail:**
```bash
# Expected: ["1", "2", "3"]
# Got: ["1 2 3"]
```

### **Step 2: Green - Implement Splitting**

```python
# src/scheme_interpreter/tokenizer.py
def tokenize(text: str) -> list[str]:
    """
    Learning goal: Handle multiple tokens separated by whitespace
    
    .split() handles multiple whitespace types (spaces, tabs, etc.)
    """
    return text.split()
```

**Run tests - all should pass now.**

### **Step 3: Refactor - Clean Up and Document**

```python
# src/scheme_interpreter/tokenizer.py
def tokenize(text: str) -> list[str]:
    """
    Convert Scheme source code into tokens.
    
    Args:
        text: Source code string
        
    Returns:
        List of tokens (strings)
        
    Examples:
        >>> tokenize("42")
        ['42']
        >>> tokenize("1 2 3")
        ['1', '2', '3']
    """
    # Handle empty input gracefully
    if not text.strip():
        return []
    
    return text.split()
```

**Learning Points:**
- **Added documentation** - now that behavior is clear
- **Added edge case handling** - empty input
- **More explicit about behavior** - docstring with examples

**Should we test the empty input case?**
```python
def test_tokenize_empty_string():
    """Edge case: empty input should return empty list"""
    from scheme_interpreter.tokenizer import tokenize
    
    result = tokenize("")
    expected = []
    
    assert result == expected
```

**Commit this milestone:**
```bash
git add .
git commit -m "Tokenizer handles multiple numbers separated by whitespace"
```

## TDD Cycle 4: Scheme-Specific Tokens

### **Step 1: Red - Test Parentheses**

```python
# tests/test_tokenizer.py
def test_tokenize_parentheses():
    """
    Learning goal: Handle Scheme's special characters
    
    Parentheses are separate tokens in Scheme, even without spaces
    "(+ 1 2)" should become ["(", "+", "1", "2", ")"]
    """
    from scheme_interpreter.tokenizer import tokenize
    
    result = tokenize("(+ 1 2)")
    expected = ["(", "+", "1", "2", ")"]
    
    assert result == expected
```

**This will fail** - our current `.split()` approach treats "(+" as one token.

### **Step 2: Green - Handle Special Characters**

```python
# src/scheme_interpreter/tokenizer.py
def tokenize(text: str) -> list[str]:
    """
    Tokenize Scheme source code, handling parentheses as separate tokens.
    """
    if not text.strip():
        return []
    
    # Insert spaces around parentheses so .split() separates them
    text = text.replace('(', ' ( ')
    text = text.replace(')', ' ) ')
    
    # Split on whitespace and filter out empty strings
    tokens = text.split()
    return tokens
```

**Learning Points:**
- **Simple approach** - insert spaces, then split
- **Handles the immediate need** - parentheses become separate tokens
- **Not perfect** - but good enough for current tests

## Advanced TDD Concepts

### **Test Organization and Naming**

```python
# Better test organization
class TestTokenizerNumbers:
    """Group related tests together"""
    
    def test_single_number(self):
        result = tokenize("42")
        assert result == ["42"]
    
    def test_multiple_numbers(self):
        result = tokenize("1 2 3")
        assert result == ["1", "2", "3"]
    
    def test_negative_numbers(self):
        result = tokenize("-42")
        assert result == ["-42"]

class TestTokenizerSymbols:
    """Test symbol tokenization"""
    
    def test_single_symbol(self):
        result = tokenize("+")
        assert result == ["+"]
    
    def test_multiple_symbols(self):
        result = tokenize("+ - *")
        assert result == ["+", "-", "*"]

class TestTokenizerLists:
    """Test list structure tokenization"""
    
    def test_empty_list(self):
        result = tokenize("()")
        assert result == ["(", ")"]
    
    def test_simple_list(self):
        result = tokenize("(+ 1 2)")
        assert result == ["(", "+", "1", "2", ")"]
```

### **Parametrized Tests for Patterns**

```python
import pytest

@pytest.mark.parametrize("input_text,expected", [
    ("42", ["42"]),
    ("123", ["123"]),
    ("-42", ["-42"]),
    ("3.14", ["3.14"]),
])
def test_tokenize_numbers(input_text, expected):
    """Test various number formats"""
    result = tokenize(input_text)
    assert result == expected

@pytest.mark.parametrize("input_text,expected", [
    ("+", ["+"]),
    ("-", ["-"]),
    ("*", ["*"]),
    ("first", ["first"]),
    ("list", ["list"]),
])
def test_tokenize_symbols(input_text, expected):
    """Test various symbols"""
    result = tokenize(input_text)
    assert result == expected
```

### **Testing Edge Cases**

```python
class TestTokenizerEdgeCases:
    """Test unusual but valid inputs"""
    
    def test_extra_whitespace(self):
        """Multiple spaces should be handled gracefully"""
        result = tokenize("  1    2   3  ")
        assert result == ["1", "2", "3"]
    
    def test_tabs_and_newlines(self):
        """Various whitespace types"""
        result = tokenize("1\t2\n3")
        assert result == ["1", "2", "3"]
    
    def test_nested_parentheses(self):
        """Nested list structures"""
        result = tokenize("((+ 1 2))")
        assert result == ["(", "(", "+", "1", "2", ")", ")"]
```

### **Error Testing**

```python
def test_tokenize_invalid_characters():
    """
    Learning goal: Think about error conditions
    
    What should happen with invalid input?
    For now, maybe just pass through - let parser handle errors
    """
    # This might be controversial - should tokenizer reject invalid chars?
    # TDD helps us think through these design decisions
    result = tokenize("hello@world")
    # For now, treat as symbol - parser will reject if invalid
    assert result == ["hello@world"]
```

## Key TDD Learning Points from This Phase

### **1. Test-First Thinking**
- **Specification by example** - tests document what code should do
- **Design pressure** - tests force you to think about interfaces
- **Incremental development** - each test adds one piece of behavior

### **2. Minimal Implementation Strategy**  
- **Resist over-engineering** - implement exactly what tests require
- **Hardcoding is OK initially** - generalize when forced by new tests
- **Simple solutions first** - optimize later if needed

### **3. Refactoring Confidence**
- **Green tests = safety net** - can change implementation fearlessly
- **Small steps** - refactor in tiny increments
- **Separate concerns** - refactor separate from adding features

### **4. Test Quality**
- **One concept per test** - focused, specific tests
- **Clear naming** - test name explains the behavior being tested
- **Readable assertions** - easy to understand what went wrong

### **5. Development Rhythm**
- **Short cycles** - red/green/refactor in minutes, not hours
- **Frequent commits** - each working feature gets committed
- **Incremental progress** - building complexity gradually

## Next Steps After Tokenizer

Once you have a solid tokenizer with good test coverage, you'll move on to:

1. **Parser** - converting tokens into an Abstract Syntax Tree
2. **Basic data structures** - SchemeValue, Environment  
3. **Simple evaluator** - handling numbers and basic operations

Each will follow the same TDD approach, building on the foundation you've established here.

## Practice Exercise

Try implementing one more tokenizer feature using TDD:

**Goal**: Handle string literals like `"hello world"`

**Challenge**: Strings can contain spaces, so they need special handling

**TDD Process**:
1. Write failing test for simple string
2. Implement minimal solution  
3. Test edge cases (empty strings, strings with quotes)
4. Refactor for clarity

This will reinforce the TDD cycle and give you practice with more complex tokenization logic!