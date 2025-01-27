# ChatterLang Grammar and Parser

## Overview
This repository contains the implementation of a lexer, parser, and grammar for ChatterLang, a custom programming language designed to handle structured dialogues and logical flows. This includes:

- A **lexer** for tokenizing input source code.
- An **LL(1) parser** for parsing and validating ChatterLang programs.
- A **grammar specification** and corresponding parsing table.

## Grammar Specification

### Rules:
```
P:       F P | ε
F:       "Flow" D ":" S "End"
S:       T S | ε
T:       B | U | I | L | A
B:       "Bot:" Q
U:       "User:" D
I:       "If" C ":" S E "End"
E:       "Else:" S | ε
L:       "Loop:" S "End"
A:       "Let" D "=" C
C:       V EXP
EXP:     O V EXP | ε
V:       Q | N | D
Q:       "\"" .*? "\""
N:       [0-9]+(\.[0-9]+)?
ID:      "{" [a-zA-Z_][a-zA-Z0-9_]* "}"
O:       "==" | "!=" | "<" | ">" | "<=" | ">=" | "=" | "%" | "\+" | "-" | "\*" | "/"
```

### Parsing Table:
| **Non-Terminal** | **Flow** | **Bot:** | **User:** | **If** | **Else:** | **Loop:** | **Let** | **End** | **:** | **=** | **{** | **}** | **\"** | **number** | **==, !=, <, >, <=, >=, %, +, -, *, /** | **$** |
|-------------------|----------|----------|-----------|--------|-----------|-----------|---------|---------|-------|-------|--------|-------|-------|-----------|----------------------------------|-------|
| **P**            | F P      |          |           |        |           |           |         | ε       |       |       |        |       |       |           |                                  | ε     |
| **F**            | Flow D : S End |          |           |        |           |           |         |         |       |       |        |       |       |           |                                  |       |
| **S**            |          | T S      | T S       | T S    | ε         | T S       | T S     | ε       |       |       |        |       |       |           |                                  |       |
| **T**            |          | B        | U         | I      |           | L         | A       |         |       |       |        |       |       |           |                                  |       |
| **B**            |          | Bot: Q   |           |        |           |           |         |         |       |       |        |       |       |           |                                  |       |
| **U**            |          |          | User: D   |        |           |           |         |         |       |       |        |       |       |           |                                  |       |
| **I**            |          |          |           | If C : S E End |   |           |         |         |       |       |        |       |       |           |                                  |       |
| **E**            |          |          |           |        | Else: S   | ε         |         |         |       |       |        |       |       |           |                                  |       |
| **L**            |          |          |           |        |           | Loop: S End |         |         |       |       |        |       |       |           |                                  |       |
| **A**            |          |          |           |        |           |           | Let D = C |         |       |       |        |       |       |           |                                  |       |
| **C**            |          |          |           |        |           |           |         |         |       |       | V EXP  |       | V EXP | V EXP     |                                  |       |
| **EXP**          |          |          |           |        |           |           |         |         | ε     |       | O V EXP |       |       |           |                                  | ε     |
| **V**            |          |          |           |        |           |           |         |         |       |       | Q      |       | Q     | N         |                                  |       |
| **Q**            |          |          |           |        |           |           |         |         |       |       |        |       | "     |           |                                  |       |
| **N**            |          |          |           |        |           |           |         |         |       |       |        |       |       | number     |                                  |       |
| **D**            |          |          |           |        |           |           |         |         |       |       | {      |       |       |           |                                  |       |
| **O**            |          |          |           |        |           |           |         |         |       |       |        |       |       |           | ==, !=, <, >, <=, >=, %, +, -, *, / |       |

## Lexer
The lexer tokenizes the input source code using the following token definitions:
- **KEYWORD**: Reserved keywords like `Flow`, `Bot`, `User`, etc.
- **IDENTIFIER**: Variables enclosed in curly braces, e.g., `{name}`.
- **STRING**: Text enclosed in double quotes, e.g., `"Hello"`.
- **NUMBER**: Integer or floating-point numbers.
- **OPERATOR**: Includes `==`, `!=`, `<`, `>`, `<=`, `>=`, etc.
- **SEPARATOR**: Characters like `:`, `,`, `(`, `)`.
- **COMMENT**: Lines starting with `#` (ignored).
- **WHITESPACE**: Ignored.

## Usage

### Tokenizing Source Code
```python
source_code = """
Flow {main}:
    Bot: "Hello!"
    User: {response}
    If {response} == "yes":
        Bot: "Great!"
    Else:
        Bot: "Oh no!"
    End
End
"""

lexer = Lexer(source_code)
tokens = lexer.tokenize()
print(tokens)
```

### Parsing
```python
parser = Parser(tokens)
parser.parse()
```

## Tests
Comprehensive test cases ensure that the lexer and parser handle simple and complex conditions, including:

- Valid inputs:
  - Simple dialogues.
  - Nested flows and blocks.
  - Logical conditions (`If`, `Else`).
- Invalid inputs:
  - Unexpected tokens.
  - Missing `End` statements.

Run tests using:
```bash
python tests.py
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write clear commit messages and include tests for new features.
4. Open a pull request.

## License
This project is licensed under the MIT License.

