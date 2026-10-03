from lexer_folder.source_position import SourcePosition
from lexer_folder.token_type import TokenType
from lexer_folder.lexer_error import LexerError
from lexer_folder.token import Token

class Lexer:
    def __init__(self, source_code: str):
        self.__source = source_code
        self.__length = len(source_code)
        self.__tokens = []

        self.__start = 0
        self.__current = 0
        self.__line = 1
        self.__column = 1
        self.__token_start_column = 1

    def __is_at_end(self) -> bool:
        return self.__current >= self.__length

    def __advance(self) -> str:
        char = self.__source[self.__current]
        self.__current += 1
        self.__column += 1
        return char

    def __peek(self) -> str:
        if self.__is_at_end():
            return ''
        return self.__source[self.__current]

    def __peek_next(self) -> str:
        if self.__current + 1 >= self.__length:
            return ''
        return self.__source[self.__current + 1]

    def __match(self, expected: str) -> bool:
        if self.__is_at_end():
            return False
        if self.__source[self.__current] != expected:
            return False
        self.__current += 1
        self.__column += 1
        return True

    def __get_current_position(self) -> SourcePosition:
        return SourcePosition(self.__line, self.__token_start_column)

    @staticmethod
    def __is_alpha(char: str) -> bool:
        return ('a' <= char <= 'z') or ('A' <= char <= 'Z') or (char == '_')

    @staticmethod
    def __is_digit(char: str) -> bool:
        return '0' <= char <= '9'

    def __is_alpha_numeric(self, char: str) -> bool:
        return self.__is_alpha(char) or self.__is_digit(char)

    @staticmethod
    def __resolve_keyword(word: str) -> TokenType:
        if word == "buong_numero":
            return TokenType.URI_BUONG_NUMERO
        elif word == "lutang_numero":
            return TokenType.URI_LUTANG_NUMERO
        elif word == "titik_uri":
            return TokenType.URI_TITIK
        elif word == "salita":
            return TokenType.URI_SALITA
        elif word == "katotohanan":
            return TokenType.URI_KATOTOHANAN
        elif word == "itakda":
            return TokenType.ITAKDA
        elif word == "ipakita":
            return TokenType.IPAKITA
        elif word == "kung":
            return TokenType.KUNG
        elif word == "kundi_kung":
            return TokenType.KUNDI_KUNG
        elif word == "kundi":
            return TokenType.KUNDI
        elif word == "pihitan":
            return TokenType.PIHITAN
        elif word == "kaso":
            return TokenType.KASO
        elif word == "hinto":
            return TokenType.HINTO
        elif word == "likas":
            return TokenType.LIKAS
        elif word == "totoo":
            return TokenType.TOTOO
        elif word == "mali":
            return TokenType.MALI
        return TokenType.TAGATUKOY

    def __skip_block_comment(self, start_pos: SourcePosition):
        while not self.__is_at_end():
            if self.__peek() == '\n':
                self.__line += 1
                self.__column = 1
                self.__advance()
            elif self.__peek() == '*' and self.__peek_next() == '/':
                self.__advance()
                self.__advance()
                return
            else:
                self.__advance()

        raise LexerError("Hindi naisarang block comment (/* ... */).", start_pos)

    def __handle_string(self, position: SourcePosition) -> Token:
        literal_start = self.__current
        while self.__peek() != '"' and not self.__is_at_end():
            if self.__peek() == '\n':
                self.__line += 1
                self.__column = 1
            self.__advance()

        if self.__is_at_end():
            raise LexerError("Hindi naisarang panipi para sa salita (Unterminated string).", position)

        literal_value = self.__source[literal_start:self.__current]
        self.__advance()  # Skip closing quote '"'
        lexeme = self.__source[self.__start:self.__current]
        return Token(TokenType.TITIK, lexeme, literal_value, position)

    def __handle_character(self, position: SourcePosition) -> Token:
        if self.__is_at_end() or self.__peek() == "'":
            raise LexerError("Walang laman ang panipi ng karakter.", position)

        char_value = self.__advance()
        if self.__peek() != "'":
            raise LexerError("Isang karakter lamang ang pinapayagan sa loob ng '' (Char literal).", position)

        self.__advance()  # Skip closing quote "'"
        lexeme = self.__source[self.__start:self.__current]
        return Token(TokenType.KARAKTER, lexeme, char_value, position)

    def __handle_number(self, position: SourcePosition) -> Token:
        while self.__is_digit(self.__peek()):
            self.__advance()

        is_float = False
        if self.__peek() == '.' and self.__is_digit(self.__peek_next()):
            is_float = True
            self.__advance()  # Consume '.'
            while self.__is_digit(self.__peek()):
                self.__advance()

        lexeme = self.__source[self.__start:self.__current]
        literal_value = float(lexeme) if is_float else int(lexeme)
        return Token(TokenType.BILANG, lexeme, literal_value, position)

    def __handle_identifier_or_keyword(self, position: SourcePosition) -> Token:
        while self.__is_alpha_numeric(self.__peek()):
            self.__advance()

        lexeme = self.__source[self.__start:self.__current]
        token_type = self.__resolve_keyword(lexeme)

        literal_value = None
        if token_type == TokenType.TOTOO:
            literal_value = True
        elif token_type == TokenType.MALI:
            literal_value = False

        return Token(token_type, lexeme, literal_value, position)

    def tokenize(self):
        while not self.__is_at_end():
            self.__start = self.__current
            self.__token_start_column = self.__column
            char = self.__advance()
            position = self.__get_current_position()

            # Whitespace handling
            if char in (' ', '\t', '\r'):
                continue
            if char == '\n':
                self.__line += 1
                self.__column = 1
                continue

            # Comments and Division operator
            if char == '#':
                while self.__peek() != '\n' and not self.__is_at_end():
                    self.__advance()
                continue

            if char == '/':
                if self.__match('/'):
                    while self.__peek() != '\n' and not self.__is_at_end():
                        self.__advance()
                    continue
                elif self.__match('*'):
                    self.__skip_block_comment(position)
                    continue
                else:
                    self.__tokens.append(Token(TokenType.HATI, "/", None, position))
                    continue

            # Single-character delimiters and math
            if char == '+':
                self.__tokens.append(Token(TokenType.DAGDAG, "+", None, position))
            elif char == '-':
                self.__tokens.append(Token(TokenType.BAWAS, "-", None, position))
            elif char == '*':
                self.__tokens.append(Token(TokenType.PARAMI, "*", None, position))
            elif char == '%':
                self.__tokens.append(Token(TokenType.LABIS, "%", None, position))
            elif char == '{':
                self.__tokens.append(Token(TokenType.KALIWANG_KUKO, "{", None, position))
            elif char == '}':
                self.__tokens.append(Token(TokenType.KANANG_KUKO, "}", None, position))
            elif char == '(':
                self.__tokens.append(Token(TokenType.KALIWANG_PANIPI, "(", None, position))
            elif char == ')':
                self.__tokens.append(Token(TokenType.KANANG_PANIPI, ")", None, position))
            elif char == ';':
                self.__tokens.append(Token(TokenType.TULDOK_KUWIT, ";", None, position))
            elif char == ':':
                self.__tokens.append(Token(TokenType.TUTULDOK, ":", None, position))
            elif char == ',':
                self.__tokens.append(Token(TokenType.KUWIT, ",", None, position))

            # Assignment and Relational operators
            elif char == '=':
                if self.__match('='):
                    self.__tokens.append(Token(TokenType.PAREHO, "==", None, position))
                else:
                    self.__tokens.append(Token(TokenType.PAGTATAKDA, "=", None, position))

            elif char == '!':
                if self.__match('='):
                    self.__tokens.append(Token(TokenType.DI_PAREHO, "!=", None, position))
                else:
                    self.__tokens.append(Token(TokenType.LOHIKAL_HINDI, "!", None, position))

            elif char == '>':
                if self.__match('='):
                    self.__tokens.append(Token(TokenType.HIGIT_O_PAREHO, ">=", None, position))
                else:
                    self.__tokens.append(Token(TokenType.HIGIT, ">", None, position))

            elif char == '<':
                if self.__match('='):
                    self.__tokens.append(Token(TokenType.MABABA_O_PAREHO, "<=", None, position))
                else:
                    self.__tokens.append(Token(TokenType.MABABA, "<", None, position))

            # Java Logical operators
            elif char == '&':
                if self.__match('&'):
                    self.__tokens.append(Token(TokenType.LOHIKAL_AT, "&&", None, position))
                else:
                    raise LexerError("Kulang ang simbolo. Inaasahan ang '&&'.", position)

            elif char == '|':
                if self.__match('|'):
                    self.__tokens.append(Token(TokenType.LOHIKAL_O, "||", None, position))
                else:
                    raise LexerError("Kulang ang simbolo. Inaasahan ang '||'.", position)

            # Literals and Identifiers
            elif char == '"':
                self.__tokens.append(self.__handle_string(position))
            elif char == "'":
                self.__tokens.append(self.__handle_character(position))
            elif self.__is_digit(char):
                self.__tokens.append(self.__handle_number(position))
            elif self.__is_alpha(char):
                self.__tokens.append(self.__handle_identifier_or_keyword(position))

            else:
                raise LexerError(f"Di-kilalang simbolo '{char}'.", position)

        # Append End-Of-File sentinel
        end_position = SourcePosition(self.__line, self.__column)
        self.__tokens.append(Token(TokenType.DULO, "", None, end_position))
        return self.__tokens

