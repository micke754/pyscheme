# Phase 2: Parser Deep Dive - Functional Approach with Design Patterns

## Why Functional Programming for Parsing?

### **Functional vs Object-Oriented Thinking**

**Object-Oriented**: "Everything is an object with data and methods"
```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def parse(self):
        # Methods operate on self.data
```

**Functional**: "Everything is data transformed by functions"
```python
def parse(tokens, position=0):
    # Functions take input, return output
    # No hidden state, everything is explicit
    return ast_node, new_position
```

### **Benefits of Functional Approach:**
- **Easier to understand**: Input → Function → Output
- **Easier to test**: No hidden state to worry about
- **Easier to debug**: Each function is independent
- **Easier to reason about**: No "spooky action at a distance"

## Representing AST Nodes with Data

### **Using Python Dictionaries and Tuples**

Instead of classes, we'll use simple data structures:

```python
# AST Node as Dictionary (Tagged Union Pattern)
def number_node(value: float) -> dict:
    """Create a number node"""
    return {
        'type': 'number',
        'value': value
    }

def symbol_node(name: str) -> dict:
    """Create a symbol node"""
    return {
        'type': 'symbol', 
        'name': name
    }

def list_node(elements: list) -> dict:
    """Create a list node"""
    return {
        'type': 'list',
        'elements': elements
    }

# Example usage:
# number_node(42) → {'type': 'number', 'value': 42}
# symbol_node('+') → {'type': 'symbol', 'name': '+'}
# list_node([...]) → {'type': 'list', 'elements': [...]}
```

### **Pattern: Tagged Union**
This is the **Tagged Union** pattern - we use a 'type' field to distinguish between different kinds of data, then include the relevant data for each type.

**Why this works:**
- **Type safety**: Each node has a clear type identifier
- **Extensible**: Easy to add new node types
- **Simple**: Just dictionaries and functions
- **Testable**: Clear input/output for each function

## Functional Parser State Management

### **The Problem with Mutable State**
```python
# Object-oriented approach (mutable state)
class Parser:
    def __init__(self, tokens):
        self.position = 0  # This changes as we parse!
    
    def advance(self):
        self.position += 1  # Mutation - can cause bugs
```

### **Functional Solution: Return New State**
```python
# Functional approach (immutable state)
def parse_expression(tokens: list, position: int) -> tuple:
    """
    Parse one expression starting at position.
    
    Returns: (ast_node, new_position)
    - ast_node: The parsed expression
    - new_position: Where to continue parsing
    """
    if position >= len(tokens):
        raise ParseError("Unexpected end of input")
    
    token = tokens[position]
    
    if token == '(':
        return parse_list(tokens, position)
    elif is_number(token):
        return parse_number(tokens, position)
    else:
        return parse_symbol(tokens, position)
```

### **Pattern: State Threading**
This is the **State Threading** pattern - we explicitly pass state (position) between functions and return new state, rather than mutating hidden state.

**Benefits:**
- **No hidden state**: Everything is explicit
- **Easier to debug**: You can see exactly where parsing is at any point
- **Easier to test**: No setup required, just call function with inputs
- **Thread safe**: No shared mutable state

## TDD Cycle 1: Parse Simple Numbers

### **Step 1: Red - Write Failing Test**

```python
# tests/test_parser_functional.py
from src.parser_functional import parse_expression, number_node

def test_parse_single_number():
    """
    Parse a single number token into a number node.
    
    Learning goals:
    - Understand function input/output
    - See how tuples return multiple values
    - Understand the Tagged Union pattern
    """
    tokens = ["42"]
    position = 0
    
    result_node, new_position = parse_expression(tokens, position)
    
    # Check the returned AST node
    expected_node = number_node(42.0)
    assert result_node == expected_node
    
    # Check that position advanced correctly
    assert new_position == 1  # Consumed one token
```

### **Step 2: Green - Minimal Implementation**

```python
# src/parser_functional.py

def number_node(value: float) -> dict:
    """Create a number AST node"""
    return {'type': 'number', 'value': value}

def symbol_node(name: str) -> dict:
    """Create a symbol AST node"""
    return {'type': 'symbol', 'name': name}

def list_node(elements: list) -> dict:
    """Create a list AST node"""
    return {'type': 'list', 'elements': elements}

class ParseError(Exception):
    """Parsing error"""
    pass

def is_number(token: str) -> bool:
    """Check if token represents a number"""
    try:
        float(token)
        return True
    except ValueError:
        return False

def parse_number(tokens: list, position: int) -> tuple:
    """
    Parse a number token.
    
    Returns: (number_node, new_position)
    """
    if position >= len(tokens):
        raise ParseError("Unexpected end of input")
    
    token = tokens[position]
    if not is_number(token):
        raise ParseError(f"Expected number, got {token}")
    
    node = number_node(float(token))
    new_position = position + 1
    return node, new_position

def parse_expression(tokens: list, position: int) -> tuple:
    """
    Parse one expression.
    
    Returns: (ast_node, new_position)
    """
    if position >= len(tokens):
        raise ParseError("Unexpected end of input")
    
    token = tokens[position]
    
    if is_number(token):
        return parse_number(tokens, position)
    else:
        raise ParseError(f"Don't know how to parse: {token}")
```

**Run the test:**
```bash
uv run pytest tests/test_parser_functional.py::test_parse_single_number -v
# Should pass!
```

### **Understanding the Functional Flow:**
```python
# Input: tokens=["42"], position=0
parse_expression(["42"], 0)
  → calls parse_number(["42"], 0)
    → creates number_node(42.0)
    → returns ({"type": "number", "value": 42.0}, 1)

# Result: AST node + new position to continue parsing
```

### **Step 3: Add More Number Tests**

```python
def test_parse_different_number():
    """Force generalization beyond hardcoded values"""
    tokens = ["123"]
    result_node, new_position = parse_expression(tokens, 0)
    
    assert result_node == number_node(123.0)
    assert new_position == 1

def test_parse_decimal_number():
    """Test floating point numbers"""
    tokens = ["3.14"]
    result_node, new_position = parse_expression(tokens, 0)
    
    assert result_node == number_node(3.14)
    assert new_position == 1

def test_parse_negative_number():
    """Test negative numbers"""
    tokens = ["-42"]
    result_node, new_position = parse_expression(tokens, 0)
    
    assert result_node == number_node(-42.0)
    assert new_position == 1
```

**All tests should pass with current implementation.**

## TDD Cycle 2: Parse Symbols

### **Step 1: Red - Add Symbol Test**

```python
def test_parse_symbol():
    """
    Parse symbol tokens into symbol nodes.
    
    Symbols are names like +, hello, first-name
    """
    tokens = ["+"]
    result_node, new_position = parse_expression(tokens, 0)
    
    expected_node = symbol_node("+")
    assert result_node == expected_node
    assert new_position == 1
```

### **Step 2: Green - Add Symbol Parsing**

```python
# src/parser_functional.py - add these functions

def parse_symbol(tokens: list, position: int) -> tuple:
    """
    Parse a symbol token.
    
    Returns: (symbol_node, new_position)
    """
    if position >= len(tokens):
        raise ParseError("Unexpected end of input")
    
    token = tokens[position]
    node = symbol_node(token)
    new_position = position + 1
    return node, new_position

def parse_expression(tokens: list, position: int) -> tuple:
    """Parse one expression - updated to handle symbols"""
    if position >= len(tokens):
        raise ParseError("Unexpected end of input")
    
    token = tokens[position]
    
    if is_number(token):
        return parse_number(tokens, position)
    else:
        # Treat everything else as a symbol for now
        return parse_symbol(tokens, position)
```

### **Pattern: Single Dispatch**
This is a simple form of the **Single Dispatch** pattern - we look at the type of input (number vs symbol) and dispatch to the appropriate function.

```python
# Single dispatch based on token type
if is_number(token):
    return parse_number(tokens, position)
else:
    return parse_symbol(tokens, position)
```

**Later we'll extend this:**
```python
if token == '(':
    return parse_list(tokens, position)
elif is_number(token):
    return parse_number(tokens, position)  
elif token in ['#true', '#false']:
    return parse_boolean(tokens, position)
else:
    return parse_symbol(tokens, position)
```

## TDD Cycle 3: Parse Empty Lists

### **Step 1: Red - Test Empty List**

```python
def test_parse_empty_list():
    """
    Parse () into an empty list node.
    
    This tests:
    - Recognition of list syntax
    - Handling of matched parentheses
    - Creation of list nodes
    """
    tokens = ["(", ")"]
    result_node, new_position = parse_expression(tokens, 0)
    
    expected_node = list_node([])  # Empty list
    assert result_node == expected_node
    assert new_position == 2  # Consumed both tokens
```

### **Step 2: Green - Add List Parsing**

```python
# src/parser_functional.py - add list parsing

def parse_list(tokens: list, position: int) -> tuple:
    """
    Parse a list expression: (element1 element2 ...)
    
    Returns: (list_node, new_position)
    """
    if position >= len(tokens) or tokens[position] != '(':
        raise ParseError("Expected opening parenthesis")
    
    # Skip opening parenthesis
    position += 1
    elements = []
    
    # Parse elements until closing parenthesis
    while position < len(tokens) and tokens[position] != ')':
        element_node, position = parse_expression(tokens, position)  # Recursion!
        elements.append(element_node)
    
    # Check for closing parenthesis
    if position >= len(tokens):
        raise ParseError("Missing closing parenthesis")
    
    # Skip closing parenthesis
    position += 1
    
    return list_node(elements), position

def parse_expression(tokens: list, position: int) -> tuple:
    """Parse one expression - updated to handle lists"""
    if position >= len(tokens):
        raise ParseError("Unexpected end of input")
    
    token = tokens[position]
    
    if token == '(':
        return parse_list(tokens, position)
    elif is_number(token):
        return parse_number(tokens, position)
    else:
        return parse_symbol(tokens, position)
```

### **Pattern: Recursive Descent**
This implements the **Recursive Descent** parsing pattern:

```python
def parse_list(tokens, position):
    # ...
    while not at_end:
        element, position = parse_expression(tokens, position)  # Recursive call
        # ...
```

**Key characteristics:**
- **Each parsing function handles one grammar rule**
- **Recursion handles nested structures naturally**
- **State (position) is threaded through recursive calls**

### **Understanding the Recursion**

```python
# Parsing "()"
parse_expression(["(", ")"], 0)
  → token is "(" → calls parse_list(["(", ")"], 0)
    → position = 1 (skip opening paren)
    → while tokens[1] != ")": # False, so skip loop
    → position = 2 (skip closing paren)  
    → return (list_node([]), 2)
```

## TDD Cycle 4: Lists with Content

### **Step 1: Red - Test List with Numbers**

```python
def test_parse_list_with_numbers():
    """
    Parse (1 2 3) into list node with number nodes.
    
    Tests:
    - Multiple elements in a list
    - Recursive parsing of list contents
    - Proper position tracking through multiple elements
    """
    tokens = ["(", "1", "2", "3", ")"]
    result_node, new_position = parse_expression(tokens, 0)
    
    expected_elements = [
        number_node(1.0),
        number_node(2.0), 
        number_node(3.0)
    ]
    expected_node = list_node(expected_elements)
    
    assert result_node == expected_node
    assert new_position == 5  # Consumed all tokens
```

**This should pass** with our current implementation!

### **Step 2: Test Mixed Content**

```python
def test_parse_list_with_symbol_and_numbers():
    """
    Parse (+ 1 2) - a function call structure.
    
    This represents the most common Scheme pattern:
    (function arg1 arg2 ...)
    """
    tokens = ["(", "+", "1", "2", ")"]
    result_node, new_position = parse_expression(tokens, 0)
    
    expected_elements = [
        symbol_node("+"),
        number_node(1.0),
        number_node(2.0)
    ]
    expected_node = list_node(expected_elements)
    
    assert result_node == expected_node
    assert new_position == 5
```

## TDD Cycle 5: Nested Lists (The Real Test)

### **Step 1: Red - Test Nested Structure**

```python
def test_parse_nested_lists():
    """
    Parse (+ 1 (* 2 3)) - nested expressions.
    
    This is the real test of recursive descent parsing!
    The inner (* 2 3) should be parsed as a complete subexpression.
    """
    tokens = ["(", "+", "1", "(", "*", "2", "3", ")", ")"]
    result_node, new_position = parse_expression(tokens, 0)
    
    # Build expected structure
    inner_list = list_node([
        symbol_node("*"),
        number_node(2.0),
        number_node(3.0)
    ])
    
    outer_list = list_node([
        symbol_node("+"), 
        number_node(1.0),
        inner_list  # Nested structure!
    ])
    
    assert result_node == outer_list
    assert new_position == 9  # Consumed all tokens
```

**This should pass** with our recursive implementation!

### **Tracing the Recursive Calls**

```python
# Parsing "(+ 1 (* 2 3))"
# tokens = ["(", "+", "1", "(", "*", "2", "3", ")", ")"]

parse_expression(tokens, 0):
  token = "(" → parse_list(tokens, 0):
    position = 1  # skip "("
    elements = []
    
    # First element: "+"
    parse_expression(tokens, 1):
      token = "+" → parse_symbol(tokens, 1):
        return (symbol_node("+"), 2)
    elements = [symbol_node("+")]
    position = 2
    
    # Second element: "1"  
    parse_expression(tokens, 2):
      token = "1" → parse_number(tokens, 2):
        return (number_node(1.0), 3)
    elements = [symbol_node("+"), number_node(1.0)]
    position = 3
    
    # Third element: "(" - another list!
    parse_expression(tokens, 3):
      token = "(" → parse_list(tokens, 3):  # RECURSIVE CALL
        position = 4  # skip "("
        inner_elements = []
        
        # Parse "*", "2", "3" recursively...
        # position ends up at 8 (after consuming ")")
        
        return (list_node([...]), 8)
    
    elements = [symbol_node("+"), number_node(1.0), inner_list]
    position = 8
    
    # tokens[8] = ")" → exit while loop
    position = 9  # skip ")"
    return (list_node(elements), 9)
```

## Helper Functions and Patterns

### **Pattern: Helper Functions for Clean Code**

```python
# Helper functions make the code more readable
def consume_token(tokens: list, position: int, expected: str) -> int:
    """
    Consume a specific token, returning new position.
    
    Pattern: Assertion Helper
    """
    if position >= len(tokens):
        raise ParseError(f"Expected '{expected}', got end of input")
    
    if tokens[position] != expected:
        raise ParseError(f"Expected '{expected}', got '{tokens[position]}'")
    
    return position + 1

def peek_token(tokens: list, position: int) -> str:
    """
    Look at current token without consuming it.
    
    Pattern: Lookahead
    """
    if position >= len(tokens):
        raise ParseError("Unexpected end of input")
    return tokens[position]

# Refactored parse_list using helpers:
def parse_list(tokens: list, position: int) -> tuple:
    """Parse list with cleaner helper functions"""
    position = consume_token(tokens, position, '(')
    elements = []
    
    while peek_token(tokens, position) != ')':
        element_node, position = parse_expression(tokens, position)
        elements.append(element_node)
    
    position = consume_token(tokens, position, ')')
    return list_node(elements), position
```

### **Pattern: Pure Functions**
All our parsing functions are **pure functions**:

```python
def parse_number(tokens: list, position: int) -> tuple:
    # Given the same inputs, always returns the same outputs
    # No side effects - doesn't modify tokens or global state
    # No hidden dependencies - everything needed is passed in
    pass
```

**Benefits of pure functions:**
- **Easy to test**: Just call with inputs, check outputs
- **Easy to debug**: No hidden state to investigate
- **Easy to reason about**: Input determines output
- **Composable**: Can combine functions easily

## Advanced TDD Patterns

### **Parametrized Tests for Patterns**

```python
import pytest

@pytest.mark.parametrize("tokens,expected_node", [
    (["42"], number_node(42.0)),
    (["3.14"], number_node(3.14)),
    (["-5"], number_node(-5.0)),
    (["+"], symbol_node("+")),
    (["hello"], symbol_node("hello")),
])
def test_parse_atoms(tokens, expected_node):
    """Test parsing of atomic expressions using parametrized tests"""
    result_node, new_position = parse_expression(tokens, 0)
    assert result_node == expected_node
    assert new_position == 1
```

### **Helper Functions for Test Data**

```python
# Pattern: Test Data Builders
def make_addition(arg1_node, arg2_node):
    """Helper to create (+ arg1 arg2) AST structure"""
    return list_node([symbol_node("+"), arg1_node, arg2_node])

def make_multiplication(arg1_node, arg2_node):
    """Helper to create (* arg1 arg2) AST structure"""
    return list_node([symbol_node("*"), arg1_node, arg2_node])

def test_parse_complex_expression():
    """Test using helper functions for readability"""
    tokens = ["(", "+", "1", "(", "*", "2", "3", ")", ")"]
    result_node, _ = parse_expression(tokens, 0)
    
    # More readable expected structure
    expected = make_addition(
        number_node(1.0),
        make_multiplication(number_node(2.0), number_node(3.0))
    )
    
    assert result_node == expected
```

### **Integration with Tokenizer**

```python
def parse_source(source: str) -> dict:
    """
    High-level function: source code → AST
    
    Pattern: Facade - simple interface hiding complexity
    """
    from .tokenizer import tokenize
    
    tokens = tokenize(source)
    ast_node, final_position = parse_expression(tokens, 0)
    
    # Check that we consumed all tokens
    if final_position != len(tokens):
        remaining = tokens[final_position:]
        raise ParseError(f"Unexpected tokens after expression: {remaining}")
    
    return ast_node

def test_parse_from_source():
    """Test integration of tokenizer + parser"""
    source = "(+ 1 (* 2 3))"
    result = parse_source(source)
    
    expected = make_addition(
        number_node(1.0),
        make_multiplication(number_node(2.0), number_node(3.0))
    )
    
    assert result == expected
```

## Error Handling Patterns

### **Pattern: Early Validation**

```python
def parse_expression(tokens: list, position: int) -> tuple:
    """Validate inputs early for better error messages"""
    # Input validation
    if not isinstance(tokens, list):
        raise TypeError("tokens must be a list")
    if not isinstance(position, int) or position < 0:
        raise ValueError("position must be a non-negative integer")
    
    # Range checking
    if position >= len(tokens):
        raise ParseError(f"Position {position} beyond end of tokens (length {len(tokens)})")
    
    # Normal parsing logic...
```

### **Pattern: Contextual Error Messages**

```python
def parse_list(tokens: list, position: int) -> tuple:
    """Enhanced error messages with context"""
    start_position = position
    
    try:
        position = consume_token(tokens, position, '(')
        elements = []
        
        while peek_token(tokens, position) != ')':
            element_node, position = parse_expression(tokens, position)
            elements.append(element_node)
        
        position = consume_token(tokens, position, ')')
        return list_node(elements), position
        
    except ParseError as e:
        # Add context to error
        context = f"while parsing list starting at position {start_position}"
        raise ParseError(f"{e}: {context}") from e
```

## Key Functional Programming Patterns

### **1. Immutable Data Structures**
```python
# Never modify existing data - always create new data
def add_element_to_list(list_node_dict, new_element):
    new_elements = list_node_dict['elements'] + [new_element]
    return list_node(new_elements)  # New node, don't modify original
```

### **2. Function Composition**
```python
# Combine simple functions to create complex behavior
def parse_scheme_program(source: str) -> dict:
    return parse_source(source)  # tokenize → parse → validate

# Could be written as:
# tokenize(source) |> parse_tokens |> validate_ast
```

### **3. Higher-Order Functions**
```python
def parse_many(parser_func, tokens: list, position: int) -> tuple:
    """
    Higher-order function: takes a parser function as parameter
    
    Parses multiple expressions using the given parser
    """
    results = []
    
    while position < len(tokens):
        result, position = parser_func(tokens, position)
        results.append(result)
    
    return results, position

# Usage:
expressions, final_pos = parse_many(parse_expression, tokens, 0)
```

## Why This Functional Approach Works

### **Clear Data Flow**
```python
# Easy to trace: input → function → output
tokens = ["(", "+", "1", "2", ")"]
ast_node, position = parse_expression(tokens, 0)
```

### **Easy Testing**
```python
# No setup required - just call functions
def test_any_parsing_function():
    result = parse_whatever(input_data)
    assert result == expected_output
```

### **Easy Debugging**
```python
# Add print statements anywhere to see data flow
def parse_list(tokens, position):
    print(f"Parsing list at position {position}: {tokens[position:]}")
    # ... rest of function
```

### **Easy Composition**
```python
# Functions naturally compose
def full_parsing_pipeline(source: str):
    tokens = tokenize(source)              # String → List[str]
    ast, _ = parse_expression(tokens, 0)    # List[str] → Dict
    return validate_ast(ast)               # Dict → ValidatedDict
```

## Next Steps: Connecting to Evaluation

The functional approach sets us up perfectly for evaluation:

```python
def evaluate(ast_node: dict, environment: dict) -> any:
    """Evaluate AST node in given environment"""
    node_type = ast_node['type']
    
    if node_type == 'number':
        return ast_node['value']
    elif node_type == 'symbol':
        return environment[ast_node['name']]
    elif node_type == 'list':
        # Evaluate function application
        func_node = ast_node['elements'][0]
        arg_nodes = ast_node['elements'][1:]
        # ... evaluation logic
```

The same patterns (pure functions, immutable data, single dispatch) carry forward naturally to the evaluator!

## Summary: Functional Patterns Used

1. **Tagged Union**: AST nodes as dictionaries with 'type' field
2. **State Threading**: Explicit state passing instead of mutation  
3. **Recursive Descent**: Functions call themselves for nested structures
4. **Single Dispatch**: Route to different functions based on input type
5. **Pure Functions**: No side effects, same input → same output
6. **Immutable Data**: Never modify existing data structures
7. **Helper Functions**: Small, focused functions for clarity
8. **Early Validation**: Check inputs at function boundaries

These patterns make the code easier to understand, test, and debug while building the foundation for a robust Scheme interpreter!
