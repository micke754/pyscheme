Convert this html page word for word in a clean human readable markdown version

# 1 Beginning Student

The grammar notation uses the notation X **...** (bold
dots) to indicate that X may occur an arbitrary number of times
(zero, one, or more). Separately, the grammar also defines ... as an
identifier to be used in templates.

See [How to Design Programs/2e, Intermezzo 1](https://htdp.org/2020-5-6/Book/i1-2.html) for an
explanation of the Beginning Student Language.

```
program ::= def-or-expr ...

def-or-expr ::= definition
              | expr
              | test-case
              | library-require

definition ::= (define (name variable variable ... ) expr)
             | (define name expr)
             | (define name (lambda (variable variable ...) expr))
             | (define-struct name (name ... ))

expr ::= (name expr expr ...)
       | (cond [expr expr] ...)
       | (cond [expr expr] ... [else expr])
       | (if expr expr expr)
       | (and expr expr expr ...)
       | (or expr expr expr ...)
       | name
       | 'name
       | '()
       | number
       | boolean
       | string
       | character
       | (signature signature-form)

signature-declaration ::= (: name signature-form)

signature-form ::= (enum expr ...)
                 | (mixed signature-form ...)
                 | (signature-form ... -> signature-form)
                 | (ListOf signature-form)
                 | signature-variable
                 | expr

signature-variable ::= %name

test-case ::= (check-expect expr expected-expression)
            | (check-random expr expected-expression)
            | (check-within expr expected-expression delta)
            | (check-member-of expr expr ...)
            | (check-range expr low-expression high-expression)
            | (check-satisfied expr name)
            | (check-error expr expected-error-message)
            | (check-error expr)

library-require ::= (require string)
                  | (require (lib string string ...))
                  | (require (planet string package))

package ::= (string string number number)
```

A name or a variable is a sequence of characters
not including a space or one of the following:

" , ` ( ) [ ] { } | ; #

A number is a number such as 123, 3/2, or
5.5.

A boolean is one of: #true or #false.

Alternative spellings for the #true constant are #t,
true, and #T. Similarly, #f, false, or
#F are also recognized as #false.

A symbol is a quote character followed by a name. A
symbol is a value, just like 42, '(), or #false.

A string is a sequence of characters enclosed by a pair of ". Unlike
symbols, strings may be split into characters and manipulated by a
variety of functions.  For example, "abcdef",
"This is a string", and "This is a string with \" inside" are all strings.

A character begins with #\ and has the
name of the character. For example, #\a, #\b,
and #\space are characters.

In function calls, the function appearing
immediately after the open parenthesis can be any functions defined
with define or define-struct, or any one of the
pre-defined functions.

### 1.1 Pre-defined Variables

* **empty**: The empty list.

* **true**: The #true value.

* **false**: The #false value.

### 1.2 Template Variables

* **..**: A placeholder for indicating that a function definition is a template.

* **...**: A placeholder for indicating that a function definition is a template.

* **....**: A placeholder for indicating that a function definition is a template.

* **.....**: A placeholder for indicating that a function definition is a template.

* **......**: A placeholder for indicating that a function definition is a template.

### 1.3 Syntax

(define (name variable variable ... ) expr)

Defines a function named name. The expression is the body
of the function. When the function is called,
the values of the arguments are inserted into the body in place of the
variables. The function returns the value of that new expression.

The function name’s cannot be the same as that of another function or
variable.

<pre><code>(define name expr)</code></pre>

Defines a variable called name with the the value of
expr. The variable name’s cannot be the same as that of
another function or variable, and name itself must not appear in
expression.

<pre><code>(define name (lambda (variable variable ...)))</code></pre>

An alternate way to defining functions. The name is the name of
the function, which cannot be the same as that of another function or
variable.

A lambda cannot be used outside of this alternate syntax.

<pre><code>'name</code></pre>

A quoted name is a symbol. A symbol is a value, just like
0 or '().

<pre><code>(define-struct structure-name (field-name ... ))</code></pre>

Defines a new structure called structure-name. The structure’s fields are
named by the field-names. After the define-struct, the following new
functions are available:

* **make-**structure-name : takes a number of
arguments equal to the number of fields in the structure,
and creates a new instance of that structure.

* structure-name-field-name : takes an
instance of the structure and returns the value in the field named by
field-name.

* structure-name? : takes any value, and returns
#true if the value is an instance of the structure.

The name of the new functions introduced by define-struct
must not be the same as that of other functions or variables,
otherwise define-struct reports an error.

<pre><code>(name expr expr ... )</code></pre>

Calls the function named name. The value of the call is the
value of name’s body when every one of the function’s
variables are replaced by the values of the corresponding
expressions.

The function named name must defined before it can be called. The
number of argument expressions must be the same as the number of arguments
expected by the function.

<pre><code>(cond [question-expression answer-expression] ...)
(cond [question-expression answer-expression] ... [else answer-expression])</code></pre>

Chooses a clause based on some condition. cond finds the first
question-expression that evaluates to #true, then
evaluates the corresponding answer-expression.

If none of the question-expressions evaluates to #true,
cond’s value is the answer-expression of the
else clause. If there is no else, cond reports
an error. If the result of a question-expression is neither
#true nor #false, cond also reports an error.

else cannot be used outside of cond.

<pre><code>(if question-expression then-answer-expression else-answer-expression)</code></pre>

When the value of the question-expression is #true,
if evaluates the then-answer-expression. When the test is
#false, if evaluates the else-answer-expression.

If the question-expression is neither #true nor
#false, if reports an error.

<pre><code>(and expr expr expr ...)</code></pre>

Evaluates to #true if all the expressions are
#true. If any expression is #false, the and
expression evaluates to #false (and the expressions to the
right of that expression are not evaluated.)

If any of the expressions evaluate to a value other than #true or
#false, and reports an error.

<pre><code>(or expr expr expr ...)</code></pre>

Evaluates to #true as soon as one of the
expressions is #true (and the expressions to the right of that
expression are not evaluated.) If all of the expressions are #false,
the or expression evaluates to #false.

If any of the expressions evaluate to a value other than #true or
#false, or reports an error.

<pre><code>(check-expect expr expected-expression)</code></pre>

Checks that the first expression evaluates to the same value as the
expected-expression.

<pre><code>check-expect (fahrenheit->celsius 212) 100
check-expect (fahrenheit->celsius -40) -40

(define (fahrenheit->celsius f)
  (* 5/9 (- f 32)))</code></pre>

A check-expect expression must be placed at the top-level of a
student program. Also it may show up anywhere in the program, including
ahead of the tested function definition. By placing check-expects
there, a programmer conveys to a future reader the intention behind the
program with working examples, thus making it often superfluous to read
the function definition proper. Syntax errors in
 check-expect (and all check forms)
are intentionally delayed to run time so that students can write tests
<em>without</em> necessarily writing complete function headers.

It is an error for expr or expected-expr to produce an
inexact number or a function value; see note on
check-expect for details.

<pre><code>(check-random expr expected-expression)</code></pre>

Checks that the first expression evaluates to the same value as the
expected-expression.

The form supplies the same random-number generator to both parts. If both
parts request random numbers from the same interval in the same
order, they receive the same random numbers.

Here is a simple example of where check-random is useful:

<pre><code>(define WIDTH 100)
(define HEIGHT (* 2 WIDTH))

(define-struct player (name x y))
; A *Player* is (make-player String Nat Nat)

; String -> Player
(check-random (create-randomly-placed-player "David Van Horn")
              (make-player "David Van Horn"
                           (random WIDTH)
                           (random HEIGHT)))

(define (create-randomly-placed-player name)
  (make-player name (random WIDTH) (random HEIGHT)))</code></pre>

Note how random is called on the same numbers in the same order in
both parts of check-random. If the two parts call random
for different intervals, they are likely to fail:

<pre><code>; String -> Player
(check-random (create-randomly-placed-player "David Van Horn")
              (make-player "David Van Horn"
                           (random WIDTH)
                           (random HEIGHT)))

(define (create-randomly-placed-player name)
  (a-helper-function name
                     (random HEIGHT)))

; Striing Number -> Player
(define (a-helper-function name height)
  (make-player name (random WIDTH) height))

; String Number -> Player
(define (a-helper-function name height)
  (make-player name (random WIDTH) height))</code></pre>

Because the argument to a-helper-function is evaluated first,
random is first called for the interval [0,HEIGHT) and then
for [0,WIDTH), that is, in a different order than in the preceding
check-random.

It is an error for expr or expected-expr to produce a function
value or an inexact number; see note on
check-expect for details.

<pre><code>(check-within expr expected-expression delta)</code></pre>

Checks whether the value of the expression expression is
structurally equal to the value produced by the
expected-expression expression; every number in the first
expression must be within delta of the corresponding number in
the second expression.

<pre><code>(define-struct roots (x sqrt))
; RT is [List-of (make-roots Number Number)]

(define (root-of a)
  (make-roots a (sqrt a)))

(define (roots-table xs)
  (cond
    [(empty? xs) '()]
    [else (and (first xs) (roots-table (rest xs)))]))

(define (roots-table xs)
  (cond
    [(empty? xs) '()]
    [else (cons (root-of (first xs)) (roots-table (rest xs)))]))

(check-within (roots-table (list 1.0 2.0 3.0))
              (list (make-roots 1.0 1.0)
                    (make-roots 2 1.414)
                    (make-roots 3 1.713))
              0.1)</code></pre>

In contrast, when delta is small, the test fails:

Example:

<pre><code>&gt; (check-within (roots-table (list 2.0))
              (list (make-roots 2 1.414))
              #i1e-5)</code></pre>

It is an error for expression, low-expression, or
high-expression to produce a function value;
see note on check-expect for details.

<pre><code>(check-member-of expr expr ...)</code></pre>

Checks that the value of the first expression is that of
one of the following expressions.

<pre><code>; [List-of X] -> X
; pick a random element from the given list l
(define (pick-one l)
  (list-ref l (random (length l))))

&gt; (check-member-of (pick-one (list "a" "b" "c"))
                  "a" "b" "c"))</code></pre>

It is an error for any of expressions to produce a function value; see
note on check-expect for details.

<pre><code>(check-range expr low-expression high-expression)</code></pre>

Checks that the value of the first expression is a number in
between the value of the low-expression and the
high-expression, inclusive.

A check-range form is best used to delimit the possible results of
functions that compute inexact numbers:

<pre><code>(define EPSILON 0.001)
; [Real -> Real] Real -> Real
; what is the slope of f at x?
(define (differentiate f x)
  (slope f (- x EPSILON) (+ x EPSILON)))

; [Real -> Real] Real Real -> Real
(define (slope f left right)
  (/ (f right) (f left))
  (/ (- (f right) (f left))
     (* 2 EPSILON)))

(check-range (differentiate sin 0)
             0.99
             1.0)</code></pre>

It is an error for expression, low-expression, or
high-expression to produce a function value;
see note on check-expect for details.

<pre><code>(require string)</code></pre>

Makes the definitions of the module specified by string
available in the current module (i.e., the current file), where
string refers to a file relative to the current file.

The string is constrained in several ways to avoid
problems with different path conventions on different platforms: a
/ is a directory separator, .
always means the current directory, ..
always means the parent directory,
path elements can use only a through z
(uppercase or lowercase), 0 through 9,
-, _, and .. , and the string cannot be
empty or contain a leading or trailing /.

<pre><code>(require module-name)</code></pre>

Accesses a file in an installed library. The library name is an
identifier with the same constraints as for a relative-path string
(though without the quotes), with the additional constraint that it
must not contain a .

<pre><code>(require (lib string string ...))</code></pre>

Accesses a file in an installed library, making its definitions
available in the current module (i.e., the current file). The first
string names the library file, and the remaining
strings name the collection (and sub-collection, and so on)
where the file is installed. Each string is constrained in the same
way as for the (require string) form.

<pre><code>(require (planet string package))
(require (planet id))
(require (planet string))</code></pre>

Accesses a library that is distributed on the internet via the
PlaneT server, making it definitions available in the current module
(i.e., current file).

The full grammar for planet requires is given in [Importing and Exporting: require and provide](https://download.racket-lang.org/releases/8.18/doc/local-redirect/index.html?doc=reference&rel=require.html&version=8.18), but
the best place to find examples of the syntax is on the
[the PlaneT server](http://planet.racket-lang.org), in the
description of a specific package.

### 1.4 Signatures

Signatures do not have to be comment: They can also be part of the
code.  When a signature is attached to a function, DrRacket will check
that program uses the function in accordance with the signature and
display signature violations along with the test results.

A signature is a regular value, and is specified as a
signature form, a
special syntax that only works with : signature declarations
and inside signature expressions.

<pre><code>(: name signature-form)</code></pre>

This attaches the signature specified by signature-form to
the definition of name.
There must be a definition of name somewhere in the program.

On running the program, Racket checks whether the signatures attached
with : actually match the value of the variable.  If they
don’t, Racket reports signature violation along with test failures.

For example, this piece of code:

<pre><code>(: age Integer)
(define age "fortytwo")</code></pre>

Yields this output:

<pre><code>1 signature violation.

Signature violations:
        got "fortytwo" at line 2, column 12, signature at line 1, column 7</code></pre>

Note that a signature violation

