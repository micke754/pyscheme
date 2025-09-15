# Understanding Parsers, ASTs, and Their Relationship with Tokenizers

## The Big Picture: From Text to Meaning

```
Raw Text  →  Tokenizer  →  Parser  →   AST    →  Evaluator  →  Result
"(+ 1 2)"     Tokens      Structure   Tree       Execute      3
```

Think of this like understanding a sentence in English:
- **Text**: "The cat sat on the mat"
- **Tokenizer**: ["The", "cat", "sat", "on", "the", "mat"] (words)
- **Parser**: Identifies structure (subject, verb, prepositional phrase)
- **AST**: Tree showing grammatical relationships
- **Evaluator**: Understands meaning and can act on it

## What is an AST (Abstract Syntax Tree)?

### **Definition**
An **Abstract Syntax Tree** is a tree representation of the structure of your program. It captures the **meaning** and **relationships** of code elements, not just their textual order.

### **Why "Abstract"?**
It's "abstract" because it **ignores irrelevant details** like:
- Whitespace between tokens
- Exact positioning of parentheses
- Comments
- Specific formatting

It keeps only what matters for **meaning**.

### **Visual Example**

For the Scheme expression `(+ 1 (* 2 3))`:

```
        ListNode
       /    |    \
      /     |     \
 SymbolNode |   ListNode
    "+"     |   /   |   \
            |  /    |    \
       NumberNode  SymbolNode NumberNode
           1         "*"        2
                              /
                        NumberNode
                             3
```

Wait, let me fix that tree:

```
        ListNode
       /    |    \
      /     |     \
 SymbolNode |   ListNode  
    "+"     |   /   |   \
            |  /    |    \
       NumberNode SymbolNode NumberNode
           1         "*"        2
                              
                        NumberNode
                             3
```

Actually, let me draw this more clearly:

```
         Application
        /     |      \
   Operator  Arg1    Arg2
      +       1   Application
                   /   |   \
              Operator Arg1 Arg2
                 *      2    3
```

## Tokenizer vs Parser: Different Jobs

### **Tokenizer's Job: Breaking Down Text**

```python
# INPUT: "(+ 1 (* 2 3))"

def tokenize(text):
    # Simplified version
    text = text.replace('(', ' ( ')
    text = text.replace(')', ' ) ')
    return text.split()

# OUTPUT: ['(', '+', '1', '(', '*', '2', '3', ')', ')']
```

**The tokenizer doesn't understand structure** - it just identifies individual pieces.

### **Parser's Job: Understanding Structure**

```python
# INPUT: ['(', '+', '1', '(', '*', '2', '3', ')', ')']

class Parser:
    def parse_expression(self):
        if self.current_token() == '(':
            return self.parse_list()
        elif self.current_token().isdigit():
            return NumberNode(int(self.current_token()))
        else:
            return SymbolNode(self.current_token())
    
    def parse_list(self):
        self.consume('(')  # Skip opening paren
        elements = []
        while self.current_token() != ')':
            elements.append(self.parse_expression())
        self.consume(')')  # Skip closing paren
        return ListNode(elements)

# OUTPUT: ListNode containing the tree structure above
```

**The parser understands relationships** - which tokens belong together, what's nested inside what.

## Why Do We Need ASTs?

### **Problem with Direct Token Interpretation**

Imagine trying to evaluate directly from tokens:
```python
tokens = ['(', '+', '1', '(', '*', '2', '3', ')', ')']

# How do you know where the inner expression ends?
# How do you handle nesting?
# This becomes very complex very quickly!
```

### **AST Makes Evaluation Natural**

```python
def evaluate(node, environment):
    if isinstance(node, NumberNode):
        return node.value
    
    elif isinstance(node, SymbolNode):
        return environment.lookup(node.name)
    
    elif isinstance(node, ListNode):
        # First element is the function
        func = evaluate(node.elements[0], environment)
        # Rest are arguments
        args = [evaluate(arg, environment) for arg in node.elements[1:]]
        return apply_function(func, args)

# The tree structure makes recursion natural!
```

## Step-by-Step Example: `(+ 1 (* 2 3))`

### **Step 1: Tokenization**
```
Input:  "(+ 1 (* 2 3))"
Tokens: ["(", "+", "1", "(", "*", "2", "3", ")", ")"]
```

### **Step 2: Parsing (Building AST)**
```python
# Parser starts reading tokens left to right
# Sees '(' → knows this is a list
# Reads '+' → this is the operator (first element)
# Reads '1' → this is first argument (second element)  
# Sees '(' → this is another list (third element)
#   Recursively parse the inner list: (* 2 3)
# Sees ')' → end of inner list
# Sees ')' → end of outer list

# Result: AST representing nested structure
```

### **Step 3: AST Structure**
```
OuterList
├── Symbol("+")
├── Number(1)
└── InnerList
    ├── Symbol("*")
    ├── Number(2)
    └── Number(3)
```

### **Step 4: Evaluation (Walking the AST)**
```python
# Evaluate outer list:
#   - Function: + (addition)
#   - Arg1: 1
#   - Arg2: Evaluate inner list
#     - Function: * (multiplication)  
#     - Arg1: 2
#     - Arg2: 3
#     - Result: 6
#   - Apply +: 1 + 6 = 7
```

## Different Types of AST Nodes

### **For BSL (Beginning Student Language)**

```python
from abc import ABC, abstractmethod

class ASTNode(ABC):
    """Base class for all AST nodes"""
    pass

# Atomic values (leaves of the tree)
class NumberNode(ASTNode):
    def __init__(self, value: float):
        self.value = value

class BooleanNode(ASTNode):
    def __init__(self, value: bool):
        self.value = value

class SymbolNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

# Compound expressions (branches of the tree)
class ListNode(ASTNode):
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements

# Special forms might get their own nodes
class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: ASTNode, else_branch: ASTNode):
        self.condition = condition
        self.then_branch = then_branch  
        self.else_branch = else_branch
```

### **Example AST Nodes for Different Expressions**

```scheme
; 42
NumberNode(42)

; hello
SymbolNode("hello")

; #true  
BooleanNode(True)

; (+ 1 2)
ListNode([
    SymbolNode("+"),
    NumberNode(1), 
    NumberNode(2)
])

; (if #true 1 2)
ListNode([
    SymbolNode("if"),
    BooleanNode(True),
    NumberNode(1),
    NumberNode(2)  
])
# OR with special node:
IfNode(
    condition=BooleanNode(True),
    then_branch=NumberNode(1),
    else_branch=NumberNode(2)
)
```

## Parser Implementation Details

### **Recursive Descent Parsing**

```python
class Parser:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.position = 0
    
    def current_token(self) -> str:
        if self.position >= len(self.tokens):
            raise ParseError("Unexpected end of input")
        return self.tokens[self.position]
    
    def consume(self, expected: str) -> None:
        if self.current_token() != expected:
            raise ParseError(f"Expected '{expected}', got '{self.current_token()}'")
        self.position += 1
    
    def parse(self) -> ASTNode:
        """Main parsing entry point"""
        if self.current_token() == '(':
            return self.parse_list()
        elif self.current_token().replace('.', '').replace('-', '').isdigit():
            return self.parse_number()
        elif self.current_token() in ['#true', '#false']:
            return self.parse_boolean()
        else:
            return self.parse_symbol()
    
    def parse_list(self) -> ListNode:
        """Parse (expr1 expr2 ...)"""
        self.consume('(')
        elements = []
        
        while self.current_token() != ')':
            elements.append(self.parse())  # Recursive call!
        
        self.consume(')')
        return ListNode(elements)
    
    def parse_number(self) -> NumberNode:
        """Parse number literal"""
        token = self.current_token()
        self.position += 1
        return NumberNode(float(token))
```

### **Key Parsing Concepts**

**Recursion**: The parser calls itself to handle nested structures
```python
def parse_list(self):
    # ...
    while not at_end:
        elements.append(self.parse())  # Recursive!
```

**Lookahead**: Parser looks at current token to decide what to do
```python
if self.current_token() == '(':
    return self.parse_list()
elif self.current_token().isdigit():
    return self.parse_number()
```

**Error Recovery**: Parser detects malformed input
```python
if self.current_token() != ')':
    raise ParseError("Missing closing parenthesis")
```

## Alternative: Parse Directly to Values (No AST)

### **Some interpreters skip ASTs:**
```python
def evaluate_tokens(tokens, env):
    """Direct interpretation without AST"""
    if tokens[0] == '(':
        # Parse and evaluate list directly
        func_name = tokens[1]
        args = parse_args(tokens[2:-1])  # Complex!
        return apply_function(func_name, args, env)
```

### **Why ASTs are Usually Better:**
- **Separation of concerns**: Parsing separate from evaluation
- **Error detection**: Syntax errors caught before evaluation
- **Optimization**: Can analyze/transform AST before evaluation
- **Debugging**: Can inspect program structure
- **Multiple passes**: Can walk AST multiple times for different purposes

## TDD with Parsers

### **Start Simple:**
```python
def test_parse_number():
    tokens = ["42"]
    parser = Parser(tokens)
    result = parser.parse()
    
    assert isinstance(result, NumberNode)
    assert result.value == 42

def test_parse_symbol():
    tokens = ["+"]
    parser = Parser(tokens)
    result = parser.parse()
    
    assert isinstance(result, SymbolNode)
    assert result.name == "+"
```

### **Build Complexity:**
```python
def test_parse_simple_list():
    tokens = ["(", "+", "1", "2", ")"]
    parser = Parser(tokens)
    result = parser.parse()
    
    assert isinstance(result, ListNode)
    assert len(result.elements) == 3
    assert isinstance(result.elements[0], SymbolNode)
    assert result.elements[0].name == "+"
```

### **Test Error Cases:**
```python
def test_parse_unmatched_paren():
    tokens = ["(", "+", "1", "2"]  # Missing closing paren
    parser = Parser(tokens)
    
    with pytest.raises(ParseError):
        parser.parse()
```

## Summary: The Relationship

1. **Tokenizer**: Breaks text into meaningful pieces (words)
2. **Parser**: Understands how pieces relate to each other (grammar)  
3. **AST**: Represents the structure in a way that's easy to work with
4. **Evaluator**: Walks the AST to compute results

Each stage makes the next stage's job easier. The tokenizer removes the complexity of character-level processing. The parser removes the complexity of flat token sequences. The AST provides a clean interface for evaluation.

**Think of it like understanding a recipe:**
- **Text**: "Mix 2 cups flour with 1 cup sugar then bake"
- **Tokens**: ["Mix", "2", "cups", "flour", "with", "1", "cup", "sugar", "then", "bake"]  
- **AST**: Tree showing "Mix(flour, sugar)" and "Bake(mixture)"
- **Evaluation**: Actually following the recipe steps

The AST captures the **logical structure** that lets you understand what to do, regardless of how it was written!
