# Phase 2: Parser Deep Dive - TDD with Classes and OOP

## Understanding Classes: Objects as Data + Behavior

### **What is a Class?**
Think of a class as a **blueprint** or **template** for creating objects. It's like a cookie cutter - it defines what shape the cookies will have, but it's not a cookie itself.

```python
# Class = Blueprint
class Car:
    def __init__(self, color, model):
        self.color = color    # Data
        self.model = model    # Data
    
    def start_engine(self):   # Behavior
        print(f"The {self.color} {self.model} engine starts!")

# Creating objects from the blueprint
my_car = Car("red", "Toyota")     # my_car is an INSTANCE of Car
your_car = Car("blue", "Honda")   # your_car is a different INSTANCE

# Using the objects
my_car.start_engine()    # "The red Toyota engine starts!"
your_car.start_engine()  # "The blue Honda engine starts!"
```

### **Key OOP Concepts:**
- **Class**: The blueprint/template
- **Object/Instance**: A specific thing created from the blueprint
- **Attributes**: Data stored in the object (`self.color`, `self.model`)
- **Methods**: Functions that belong to the object (`start_engine`)
- **`self`**: Refers to the specific instance being used

## Why Classes for AST Nodes?

We need to represent different types of program elements:
- Numbers (like `42`)
- Symbols (like `+`)  
- Lists (like `(+ 1 2)`)

**Each type needs:**
- **Data**: What it contains (the value, the name, the elements)
- **Behavior**: How to display it, how to evaluate it, etc.

Classes let us create different "types" of nodes that all work together.

## Setting Up AST Node Classes

### **Base Class - The Common Blueprint**

```python
# src/ast_nodes.py
from abc import ABC, abstractmethod
from typing import List, Union

class ASTNode(ABC):
    """
    Base class for all AST nodes.
    
    ABC = Abstract Base Class
    This means:
    1. You can't create ASTNode objects directly
    2. All subclasses must implement certain methods
    3. It's just a common interface/contract
    """
    pass

# Think of ASTNode as saying:
# "All AST nodes must follow this pattern, but each type will be different"
```

### **Concrete Node Classes**

```python
class NumberNode(ASTNode):
    """Represents a number like 42 or 3.14"""
    
    def __init__(self, value: float):
        """
        __init__ is the constructor - runs when creating a new object
        
        NumberNode(42) calls this with value=42
        """
        self.value = value    # Store the number
    
    def __repr__(self):
        """
        __repr__ controls how the object looks when printed
        Useful for debugging and testing
        """
        return f"NumberNode({self.value})"

class SymbolNode(ASTNode):
    """Represents a symbol like + or hello"""
    
    def __init__(self, name: str):
        self.name = name      # Store the symbol name
    
    def __repr__(self):
        return f"SymbolNode('{self.name}')"

class ListNode(ASTNode):
    """Represents a list like (+ 1 2)"""
    
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements    # Store list of child nodes
    
    def __repr__(self):
        return f"ListNode({self.elements})"
```

**Understanding the Classes:**
```python
# Creating instances (objects)
num = NumberNode(42)        # num.value = 42
sym = SymbolNode("+")       # sym.name = "+"
lst = ListNode([sym, num])  # lst.elements = [SymbolNode("+"), NumberNode(42)]

# Accessing data
print(num.value)    # 42
print(sym.name)     # +
print(lst.elements) # [SymbolNode('+'), NumberNode(42)]
```

## Parser Class - Managing State

```python
# src/parser.py
from typing import List
from .ast_nodes import ASTNode, NumberNode, SymbolNode, ListNode

class Parser:
    """
    Parser manages the process of converting tokens to AST.
    
    Why a class?
    - Needs to track current position in token list
    - Multiple methods need to share this state
    - Clean interface: create parser, call parse()
    """
    
    def __init__(self, tokens: List[str]):
        """Initialize parser with tokens"""
        self.tokens = tokens     # The list of tokens to parse
        self.position = 0        # Current position in the token list
    
    def current_token(self) -> str:
        """Get current token without moving position"""
        if self.position >= len(self.tokens):
            raise ParseError("Unexpected end of input")
        return self.tokens[self.position]
    
    def advance(self) -> str:
        """Get current token and move to next position"""
        token = self.current_token()
        self.position += 1
        return token
    
    def parse(self) -> ASTNode:
        """Main parsing method - will implement with TDD"""
        pass

class ParseError(Exception):
    """Custom exception for parsing errors"""
    pass
```

**Understanding Parser State:**
```python
parser = Parser(["(", "+", "1", "2", ")"])
# parser.tokens = ["(", "+", "1", "2", ")"]
# parser.position = 0

print(parser.current_token())  # "(" (position stays 0)
print(parser.advance())        # "(" (position becomes 1)
print(parser.current_token())  # "+" (position still 1)
print(parser.advance())        # "+" (position becomes 2)
```

## TDD Cycle 1: Parse Simple Numbers

### **Step 1: Red - Write Failing Test**

```python
# tests/test_parser.py
import pytest
from src.parser import Parser, ParseError
from src.ast_nodes import NumberNode, SymbolNode, ListNode

class TestParserNumbers:
    """Group related tests together using a test class"""
    
    def test_parse_single_number(self):
        """
        Start with the simplest possible case.
        
        Learning goals:
        - Understand how parser converts tokens to AST
        - See the difference between token "42" and NumberNode(42)
        """
        tokens = ["42"]
        parser = Parser(tokens)
        
        result = parser.parse()
        
        # Check the type of object created
        assert isinstance(result, NumberNode)
        # Check the value stored in the object
        assert result.value == 42
```

**Run the test:**
```bash
uv run pytest tests/test_parser.py::TestParserNumbers::test_parse_single_number -v

# Expected: FAILED - NotImplementedError or similar
# Because parser.parse() just has 'pass'
```

### **Step 2: Green - Minimal Implementation**

```python
# src/parser.py - update the parse method
def parse(self) -> ASTNode:
    """Parse a single expression"""
    token = self.advance()  # Get current token and move forward
    
    # For now, just handle numbers
    if token.replace('.', '').replace('-', '').isdigit():
        return NumberNode(float(token))
    else:
        raise ParseError(f"Don't know how to parse: {token}")
```

**Run the test again:**
```bash
uv run pytest tests/test_parser.py::TestParserNumbers::test_parse_single_number -v

# Expected: PASSED
```

**Learning Points:**
- **`isinstance(result, NumberNode)`**: Checks if `result` is a NumberNode object
- **`result.value`**: Accesses the data stored in the NumberNode
- **Minimal implementation**: Only handles the specific case being tested

### **Step 3: Refactor - Add More Test Cases**

```python
# tests/test_parser.py - add to TestParserNumbers class
def test_parse_different_number(self):
    """Force generalization beyond hardcoded values"""
    tokens = ["123"]
    parser = Parser(tokens)
    
    result = parser.parse()
    
    assert isinstance(result, NumberNode)
    assert result.value == 123

def test_parse_decimal_number(self):
    """Test floating point numbers"""
    tokens = ["3.14"]
    parser = Parser(tokens)
    
    result = parser.parse()
    
    assert isinstance(result, NumberNode)
    assert result.value == 3.14

def test_parse_negative_number(self):
    """Test negative numbers"""
    tokens = ["-42"]
    parser = Parser(tokens)
    
    result = parser.parse()
    
    assert isinstance(result, NumberNode)
    assert result.value == -42
```

**All tests should pass with current implementation.**

**Commit this milestone:**
```bash
git add .
git commit -m "Parser handles numbers - creates NumberNode objects"
```

## TDD Cycle 2: Parse Symbols

### **Step 1: Red - Add Symbol Test**

```python
# tests/test_parser.py
class TestParserSymbols:
    """Test parsing of symbols (identifiers)"""
    
    def test_parse_simple_symbol(self):
        """
        Symbols are names like +, hello, first
        Should create SymbolNode objects
        """
        tokens = ["+"]
        parser = Parser(tokens)
        
        result = parser.parse()
        
        assert isinstance(result, SymbolNode)
        assert result.name == "+"
```

**This will fail** because our parser only handles numbers.

### **Step 2: Green - Extend Parser**

```python
# src/parser.py - update parse method
def parse(self) -> ASTNode:
    """Parse a single expression"""
    token = self.advance()
    
    if token.replace('.', '').replace('-', '').isdigit():
        return NumberNode(float(token))
    else:
        # Treat everything else as a symbol for now
        return SymbolNode(token)
```

**Test should pass now.**

### **Step 3: Add More Symbol Tests**

```python
# tests/test_parser.py - add to TestParserSymbols
def test_parse_word_symbol(self):
    tokens = ["hello"]
    parser = Parser(tokens)
    
    result = parser.parse()
    
    assert isinstance(result, SymbolNode)
    assert result.name == "hello"

def test_parse_hyphenated_symbol(self):
    """Scheme allows hyphens in symbols"""
    tokens = ["first-name"]
    parser = Parser(tokens)
    
    result = parser.parse()
    
    assert isinstance(result, SymbolNode)
    assert result.name == "first-name"
```

## TDD Cycle 3: Parse Empty Lists

### **Step 1: Red - Test Empty List**

```python
# tests/test_parser.py
class TestParserLists:
    """Test parsing of list expressions"""
    
    def test_parse_empty_list(self):
        """
        () should create a ListNode with no elements
        
        This is the simplest list case - no complexity of contents
        """
        tokens = ["(", ")"]
        parser = Parser(tokens)
        
        result = parser.parse()
        
        assert isinstance(result, ListNode)
        assert len(result.elements) == 0
        assert result.elements == []
```

**This will fail** - our parser doesn't handle parentheses.

### **Step 2: Green - Add List Parsing**

```python
# src/parser.py - update parse method
def parse(self) -> ASTNode:
    """Parse a single expression"""
    # Look at current token without consuming it
    token = self.current_token()
    
    if token == '(':
        return self.parse_list()
    elif token.replace('.', '').replace('-', '').isdigit():
        self.advance()  # Consume the number token
        return NumberNode(float(token))
    else:
        self.advance()  # Consume the symbol token
        return SymbolNode(token)

def parse_list(self) -> ListNode:
    """Parse (element1 element2 ...)"""
    self.advance()  # Consume opening '('
    
    elements = []
    
    # Keep parsing until we hit closing ')'
    while self.current_token() != ')':
        elements.append(self.parse())  # Recursive call!
    
    self.advance()  # Consume closing ')'
    return ListNode(elements)
```

**Key Learning Points:**
- **Recursion**: `parse_list` calls `parse()` to handle nested structures
- **State management**: Parser tracks position as it consumes tokens
- **Lookahead**: `current_token()` lets us decide what to do without committing

### **Step 3: Test Error Cases**

```python
# tests/test_parser.py - add to TestParserLists
def test_parse_unmatched_opening_paren(self):
    """Missing closing parenthesis should raise error"""
    tokens = ["("]
    parser = Parser(tokens)
    
    with pytest.raises(ParseError):
        parser.parse()

def test_parse_unmatched_closing_paren(self):
    """Unexpected closing parenthesis"""
    tokens = [")"]
    parser = Parser(tokens)
    
    with pytest.raises(ParseError):
        parser.parse()
```

**These tests will fail** because our error handling isn't robust. Let's fix it:

```python
# src/parser.py - improve error handling
def current_token(self) -> str:
    """Get current token without moving position"""
    if self.position >= len(self.tokens):
        raise ParseError("Unexpected end of input")
    return self.tokens[self.position]

def parse(self) -> ASTNode:
    """Parse a single expression"""
    token = self.current_token()
    
    if token == '(':
        return self.parse_list()
    elif token == ')':
        raise ParseError("Unexpected closing parenthesis")
    elif token.replace('.', '').replace('-', '').isdigit():
        self.advance()
        return NumberNode(float(token))
    else:
        self.advance()
        return SymbolNode(token)
```

## TDD Cycle 4: Parse Simple Lists with Content

### **Step 1: Red - Test List with Numbers**

```python
# tests/test_parser.py - add to TestParserLists
def test_parse_list_with_numbers(self):
    """
    (1 2 3) should create ListNode containing three NumberNodes
    
    This tests:
    - Multiple elements in a list
    - Recursive parsing of list contents
    """
    tokens = ["(", "1", "2", "3", ")"]
    parser = Parser(tokens)
    
    result = parser.parse()
    
    # Check it's a list
    assert isinstance(result, ListNode)
    assert len(result.elements) == 3
    
    # Check each element
    assert isinstance(result.elements[0], NumberNode)
    assert result.elements[0].value == 1
    
    assert isinstance(result.elements[1], NumberNode)
    assert result.elements[1].value == 2
    
    assert isinstance(result.elements[2], NumberNode)
    assert result.elements[2].value == 3
```

**This should pass** with our current implementation because the recursive `parse()` call handles the numbers.

### **Step 2: Test Mixed Content Lists**

```python
def test_parse_list_with_symbol_and_numbers(self):
    """
    (+ 1 2) should create ListNode with SymbolNode and two NumberNodes
    This represents a function call
    """
    tokens = ["(", "+", "1", "2", ")"]
    parser = Parser(tokens)
    
    result = parser.parse()
    
    assert isinstance(result, ListNode)
    assert len(result.elements) == 3
    
    # First element should be the operator symbol
    assert isinstance(result.elements[0], SymbolNode)
    assert result.elements[0].name == "+"
    
    # Rest should be numbers
    assert isinstance(result.elements[1], NumberNode)
    assert result.elements[1].value == 1
    
    assert isinstance(result.elements[2], NumberNode)  
    assert result.elements[2].value == 2
```

## TDD Cycle 5: Nested Lists

### **Step 1: Red - Test Nested Structure**

```python
def test_parse_nested_lists(self):
    """
    (+ 1 (* 2 3)) should create nested ListNode structure
    
    This is the real test of recursive parsing!
    """
    tokens = ["(", "+", "1", "(", "*", "2", "3", ")", ")"]
    parser = Parser(tokens)
    
    result = parser.parse()
    
    # Outer list: (+ 1 (...))
    assert isinstance(result, ListNode)
    assert len(result.elements) == 3
    
    # First element: +
    assert isinstance(result.elements[0], SymbolNode)
    assert result.elements[0].name == "+"
    
    # Second element: 1
    assert isinstance(result.elements[1], NumberNode)
    assert result.elements[1].value == 1
    
    # Third element: (* 2 3) - should be another ListNode
    inner_list = result.elements[2]
    assert isinstance(inner_list, ListNode)
    assert len(inner_list.elements) == 3
    
    # Contents of inner list
    assert isinstance(inner_list.elements[0], SymbolNode)
    assert inner_list.elements[0].name == "*"
    
    assert isinstance(inner_list.elements[1], NumberNode)
    assert inner_list.elements[1].value == 2
    
    assert isinstance(inner_list.elements[2], NumberNode)
    assert inner_list.elements[2].value == 3
```

**This should pass** with our current recursive implementation! The magic is in this line:
```python
elements.append(self.parse())  # This calls parse() recursively for nested lists
```

## Understanding the Recursion

### **How Nested Parsing Works:**

```python
# Parsing "(+ 1 (* 2 3))"
# tokens = ["(", "+", "1", "(", "*", "2", "3", ")", ")"]

parse():                           # Start parsing
  current_token() = "("            # See opening paren
  parse_list():                    # Call parse_list
    advance()                      # Consume "(" → position = 1
    elements = []
    
    # First iteration of while loop
    current_token() = "+"          # position = 1
    parse():                       # Recursive call for "+"
      current_token() = "+"        # It's a symbol
      advance()                    # Consume "+" → position = 2
      return SymbolNode("+")
    elements = [SymbolNode("+")]
    
    # Second iteration
    current_token() = "1"          # position = 2
    parse():                       # Recursive call for "1"
      current_token() = "1"        # It's a number
      advance()                    # Consume "1" → position = 3
      return NumberNode(1)
    elements = [SymbolNode("+"), NumberNode(1)]
    
    # Third iteration
    current_token() = "("          # position = 3 - another list!
    parse():                       # Recursive call for inner list
      current_token() = "("
      parse_list():                # NESTED parse_list call
        advance()                  # Consume "(" → position = 4
        elements = []              # NEW elements list for inner list
        
        # Parse "*", "2", "3" (similar to above)
        # advance() through all of them
        # position ends up at 8 (after consuming ")")
        
        return ListNode([SymbolNode("*"), NumberNode(2), NumberNode(3)])
    
    elements = [SymbolNode("+"), NumberNode(1), ListNode([...])]
    
    current_token() = ")"          # position = 8
    advance()                      # Consume ")" → position = 9
    return ListNode(elements)
```

## Advanced TDD Patterns

### **Parametrized Tests for Patterns**

```python
import pytest

@pytest.mark.parametrize("tokens,expected_type,expected_value", [
    (["42"], NumberNode, 42),
    (["3.14"], NumberNode, 3.14),
    (["-5"], NumberNode, -5),
    (["+"], SymbolNode, "+"),
    (["hello"], SymbolNode, "hello"),
])
def test_parse_atoms(tokens, expected_type, expected_value):
    """Test parsing of atomic expressions"""
    parser = Parser(tokens)
    result = parser.parse()
    
    assert isinstance(result, expected_type)
    if hasattr(result, 'value'):
        assert result.value == expected_value
    elif hasattr(result, 'name'):
        assert result.name == expected_value
```

### **Helper Functions for Complex Tests**

```python
def create_parser(source: str) -> Parser:
    """Helper: create parser from source string"""
    from src.tokenizer import tokenize
    tokens = tokenize(source)
    return Parser(tokens)

def test_parse_complex_expression():
    """Test with integrated tokenizer"""
    parser = create_parser("(+ 1 (* 2 3))")
    result = parser.parse()
    
    # Use helper to make assertions cleaner
    assert_is_addition_of(result, 1, multiplication_of(2, 3))

def assert_is_addition_of(node, first_arg, second_arg):
    """Helper assertion for addition expressions"""
    assert isinstance(node, ListNode)
    assert len(node.elements) == 3
    assert isinstance(node.elements[0], SymbolNode)
    assert node.elements[0].name == "+"
    # ... more detailed assertions
```

## Error Handling and Edge Cases

### **Better Error Messages**

```python
class ParseError(Exception):
    """Enhanced parse error with position information"""
    
    def __init__(self, message: str, position: int = None, token: str = None):
        self.message = message
        self.position = position
        self.token = token
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.position is not None and self.token is not None:
            return f"{self.message} at position {self.position}: '{self.token}'"
        return self.message

# In Parser class:
def current_token(self) -> str:
    if self.position >= len(self.tokens):
        raise ParseError("Unexpected end of input", self.position)
    return self.tokens[self.position]

def parse(self) -> ASTNode:
    token = self.current_token()
    
    if token == ')':
        raise ParseError("Unexpected closing parenthesis", self.position, token)
    # ... rest of method
```

### **Test Error Messages**

```python
def test_error_message_quality():
    """Test that error messages are helpful"""
    tokens = ["(", "+", "1"]  # Missing closing paren
    parser = Parser(tokens)
    
    with pytest.raises(ParseError) as exc_info:
        parser.parse()
    
    error_msg = str(exc_info.value)
    assert "end of input" in error_msg.lower()
```

## Refactoring: Making Code Cleaner

### **Extract Methods for Clarity**

```python
class Parser:
    # ... existing methods ...
    
    def is_number_token(self, token: str) -> bool:
        """Check if token represents a number"""
        return token.replace('.', '').replace('-', '').isdigit()
    
    def parse_number(self) -> NumberNode:
        """Parse number token into NumberNode"""
        token = self.advance()
        return NumberNode(float(token))
    
    def parse_symbol(self) -> SymbolNode:
        """Parse symbol token into SymbolNode"""
        token = self.advance()
        return SymbolNode(token)
    
    def parse(self) -> ASTNode:
        """Parse a single expression - now cleaner"""
        token = self.current_token()
        
        if token == '(':
            return self.parse_list()
        elif token == ')':
            raise ParseError("Unexpected closing parenthesis", self.position, token)
        elif self.is_number_token(token):
            return self.parse_number()
        else:
            return self.parse_symbol()
```

## Key Learning Points from Parser Phase

### **Object-Oriented Design:**
- **Classes model real concepts** - NumberNode, SymbolNode, ListNode
- **Encapsulation** - data and behavior grouped together
- **Inheritance** - all nodes inherit from ASTNode
- **Polymorphism** - all nodes can be treated as ASTNode

### **Recursive Algorithms:**
- **Base cases** - atomic expressions (numbers, symbols)
- **Recursive cases** - lists contain other expressions
- **State management** - parser position advances through recursive calls

### **TDD Benefits:**
- **Incremental complexity** - start simple, add features
- **Regression safety** - old tests keep passing
- **Design pressure** - tests force clean interfaces
- **Documentation** - tests show how code is intended to be used

### **Error Handling:**
- **Fail fast** - catch errors at parse time, not evaluation time
- **Helpful messages** - include position and context
- **Recovery strategies** - how to handle malformed input

## Next Steps

After completing the parser:
1. **Integration with tokenizer** - parse real Scheme source code
2. **AST visualization** - pretty-print the tree structure
3. **Evaluation preparation** - AST is ready for the evaluator
4. **Error recovery** - handle partially malformed input

The parser is the bridge between flat text and structured data that the evaluator can work with. Getting this right makes evaluation much simpler!
