class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.line = 1
        self.token_specification = [
            ("KEYWORD", r"(Flow|Bot:|User:|to|Else:|End|Loop:|Let)"),
            ("IDENTIFIER", r"\{[a-zA-Z_][a-zA-Z0-9_]*\}"),
            ("STRING", r'".*?"'),
            ("NUMBER", r"\b\d+(\.\d+)?\b"),
            ("OPERATOR", r"==|!=|<=|>=|<|>|=|%|\+|-|\*|/"),
            ("SEPARATOR", r"[:,{}()]"),
            ("WHITESPACE", r"\s+"),
            ("COMMENT", r"#.*"),
            ("MISMATCH", r"."),
        ]

    def tokenize(self):
        import re
        code = self.source_code
        token_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in self.token_specification)
        line_number = 1
        line_start = 0

        for match in re.finditer(token_regex, code):
            kind = match.lastgroup
            value = match.group()
            if kind == "NEWLINE":
                self.line += 1
            elif kind == "WHITESPACE":
                continue
            elif kind == "COMMENT":
                continue
            #elif kind == "MISMATCH":
                #raise ValueError(f"1Unexpected token '{value}' at line {line_number}")
            else:
                self.tokens.append((kind, value))

            if "\n" in value:
                line_number += 1
                line_start = match.end()

        self.tokens.append(("EOF", "$"))
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.parsing_table = {
            "P": {"Flow": ["F", "P"], "$": []},
            "F": {"Flow": ["Flow", "ID", ":", "S", "End"]},
            "S": {"Bot:": ["T", "S"], "User:": ["T", "S"], "to": ["T", "S"], "Loop:": ["T", "S"], "Let": ["T", "S"], "End": [], "Else:": []},
            "T": {"Bot:": ["B"], "User:": ["U"], "to": ["I"], "Loop:": ["L"], "Let": ["A"]},
            "B": {"Bot:": ["Bot:", "Q"]},
            "U": {"User:": ["User:", "ID"]},
            "I": {"to": ["to", "C", ":", "S", "E", "End"]},
            "E": {"Else:": ["Else:", "S"], "End": []},
            "L": {"Loop:": ["Loop:", "S", "End"]},
            "A": {"Let": ["Let", "ID", "=", "C"]},
            "C": {"IDENTIFIER": ["V", "EXPR"], "NUMBER": ["V", "EXPR"], "STRING": ["V", "EXPR"]},
            "EXPR": {"OPERATOR": ["O", "V", "EXPR"], "EOF": []},
            "V": {"STRING": ["Q"], "NUMBER": ["N"], "IDENTIFIER": ["ID"]},
            "Q": {"STRING": ["STRING"]},
            "N": {"NUMBER": ["NUMBER"]},
            "ID": {"IDENTIFIER": ["IDENTIFIER"]},
            "O": {"OPERATOR": ["OPERATOR"]},
        }

        self.stack = ["P"]

    def get_next_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return ("EOF", "$")

    def parse(self):
        i = 1
        while self.stack:
            print("\nIteration: ", i); i +=1
            print("Stack: ", self.stack)
            top = self.stack.pop()
            current_token_type, current_lexeme = self.get_next_token()
            print(f"Current Token: {current_token_type}: {current_lexeme}")

            if top in self.parsing_table:
                if current_lexeme in self.parsing_table[top]:
                    production = self.parsing_table[top][current_lexeme]
                    self.stack.extend(reversed(production))
                elif current_token_type in self.parsing_table[top]:
                    production = self.parsing_table[top][current_token_type]
                    self.stack.extend(reversed(production))
                elif [] in self.parsing_table[top].values():  # Handle epsilon
                    print(f"Expanding {top} -> []")
                    continue
                else:
                    raise SyntaxError(f"Unexpected token '{current_lexeme}' for non-terminal '{top}'")
                print(f"Expanding {top} -> {production}")
            elif top == current_lexeme or (
                top in ["IDENTIFIER", "STRING", "NUMBER", "OPERATOR"] and current_token_type == top
            ):
                print(f"Matched terminal: {top}")
                self.current_token_index += 1
            else:
                raise SyntaxError(f"Unexpected token '{current_lexeme}' for terminal '{top}'")
            
        print("\nStack: ", self.stack, "\nParsing successful!")



# Example usage
source_code = """
Flow {Demo}:
    Let {counter} = 1
    Let {max_count} = 5
    Bot: "Welcome to the advanced demo!"
    Loop:
        to {counter} == {max_count}:
            Bot: "Counter has reached the maximum value of {max_count}."
            Let {status} = "done"
        Else:
            to {counter} % 2 == 0:
                Bot: "Counter {counter} is even."
            Else:
                Bot: "Counter {counter} is odd."
            End
            Let {counter} = {counter} + 1
        End
    End
    to {status} == "done":
        Bot: "The loop is complete."
    Else:
        Bot: "Something went wrong with the loop."
    End
    Bot: "Thank you for using ChatterLang!"
End
"""

try:
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print("Tokens:")
    for token_type, lexeme in tokens:
        print(f"{token_type: <12} | {lexeme: <20}")

    print("\nParsing...")
    parser = Parser(tokens)
    parser.parse()
except (ValueError, SyntaxError) as e:
    print('\n', e)
