from __future__ import annotations

import unicodedata

from .errors import Diagnostic
from .tokens import KEYWORDS, Token, TokenType


class Lexer:
    """Analisador léxico usado como entrada do analisador sintático."""

    SIMPLE_TOKENS: dict[str, TokenType] = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "=": TokenType.EQUAL,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        ",": TokenType.COMMA,
        ";": TokenType.SEMICOLON,
        ":": TokenType.COLON,
        ".": TokenType.DOT,
        "<": TokenType.LESS,
        ">": TokenType.GREATER,
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.diagnostics: list[Diagnostic] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1

    def scan_tokens(self) -> tuple[list[Token], list[Diagnostic]]:
        while not self._is_at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column, self.current))
        return self.tokens, self.diagnostics

    def _scan_token(self) -> None:
        char = self._advance()

        if char in " \r\t\ufeff" or char == "\n":
            return
        if self._is_identifier_start(char):
            self._identifier()
            return
        if char.isdigit():
            self._number()
            return
        if char in {'"', "'"}:
            self._string(char)
            return

        if char == "/" and self._match("/"):
            self._line_comment()
            return
        if char == "{":
            self._block_comment("}")
            return
        if char == "(" and self._match("*"):
            self._block_comment("*)")
            return

        if char == ":" and self._match("="):
            self._add_token(TokenType.ASSIGN)
            return
        if char == "<" and self._match("="):
            self._add_token(TokenType.LESS_EQUAL)
            return
        if char == ">" and self._match("="):
            self._add_token(TokenType.GREATER_EQUAL)
            return
        if char == "<" and self._match(">"):
            self._add_token(TokenType.NOT_EQUAL)
            return
        if char == "!" and self._match("="):
            self._add_token(TokenType.NOT_EQUAL)
            return

        token_type = self.SIMPLE_TOKENS.get(char)
        if token_type is not None:
            self._add_token(token_type)
            return

        self._error(f"Caractere inesperado '{char}'.")

    def _identifier(self) -> None:
        while self._is_identifier_part(self._peek()):
            self._advance()

        text = self.source[self.start:self.current]
        normalized = unicodedata.normalize("NFC", text).lower()
        token_type = KEYWORDS.get(normalized, TokenType.IDENTIFIER)
        literal: object | None = None
        if token_type is TokenType.TRUE:
            literal = True
        elif token_type is TokenType.FALSE:
            literal = False
        self._add_token(token_type, literal)

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        is_real = False
        if self._peek() == "." and self._peek_next().isdigit():
            is_real = True
            self._advance()
            while self._peek().isdigit():
                self._advance()

        text = self.source[self.start:self.current]
        if self._is_identifier_start(self._peek()):
            while self._is_identifier_part(self._peek()):
                self._advance()
            invalid = self.source[self.start:self.current]
            self._error(f"Número malformado '{invalid}'. Identificadores não podem iniciar por dígito.")
            return

        self._add_token(TokenType.REAL_LITERAL if is_real else TokenType.INTEGER_LITERAL, float(text) if is_real else int(text))

    def _string(self, quote: str) -> None:
        value_chars: list[str] = []
        while not self._is_at_end() and self._peek() != quote:
            if self._peek() == "\n":
                self._error("Cadeia de caracteres não pode atravessar linha.")
                return
            char = self._advance()
            if char == "\\" and not self._is_at_end():
                escaped = self._advance()
                value_chars.append({"n": "\n", "t": "\t", "r": "\r", quote: quote, "\\": "\\"}.get(escaped, escaped))
            else:
                value_chars.append(char)

        if self._is_at_end():
            self._error("Cadeia de caracteres não finalizada.")
            return

        self._advance()
        self._add_token(TokenType.STRING_LITERAL, "".join(value_chars))

    def _line_comment(self) -> None:
        while self._peek() != "\n" and not self._is_at_end():
            self._advance()

    def _block_comment(self, terminator: str) -> None:
        while not self._is_at_end():
            if terminator == "}" and self._peek() == "}":
                self._advance()
                return
            if terminator == "*)" and self._peek() == "*" and self._peek_next() == ")":
                self._advance()
                self._advance()
                return
            self._advance()
        self._error("Comentário de bloco não finalizado.")

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        self._advance()
        return True

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _is_identifier_start(self, char: str) -> bool:
        return char == "_" or char.isalpha()

    def _is_identifier_part(self, char: str) -> bool:
        return char == "_" or char.isalpha() or char.isdigit()

    def _add_token(self, token_type: TokenType, literal: object | None = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.start_line, self.start_column, self.start))

    def _error(self, message: str) -> None:
        self.diagnostics.append(Diagnostic(message, self.start_line, self.start_column, self.start, "erro léxico"))
