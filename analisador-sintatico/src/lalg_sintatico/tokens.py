from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class TokenType(str, Enum):
    EOF = "EOF"
    IDENTIFIER = "IDENTIFICADOR"
    INTEGER_LITERAL = "NUMERO_INTEIRO"
    REAL_LITERAL = "NUMERO_REAL"
    STRING_LITERAL = "CADEIA"

    PROGRAM = "PROGRAM"
    VAR = "VAR"
    INTEGER = "INTEGER"
    REAL = "REAL"
    BOOLEAN = "BOOLEAN"
    PROCEDURE = "PROCEDURE"
    BEGIN = "BEGIN"
    END = "END"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    WHILE = "WHILE"
    DO = "DO"
    READ = "READ"
    WRITE = "WRITE"
    TRUE = "TRUE"
    FALSE = "FALSE"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    DIV = "DIV"
    MOD = "MOD"

    PLUS = "MAIS"
    MINUS = "MENOS"
    STAR = "MULTIPLICACAO"
    SLASH = "DIVISAO"
    ASSIGN = "ATRIBUICAO"
    EQUAL = "IGUAL"
    NOT_EQUAL = "DIFERENTE"
    LESS = "MENOR"
    LESS_EQUAL = "MENOR_IGUAL"
    GREATER = "MAIOR"
    GREATER_EQUAL = "MAIOR_IGUAL"
    LPAREN = "ABRE_PARENTESE"
    RPAREN = "FECHA_PARENTESE"
    COMMA = "VIRGULA"
    SEMICOLON = "PONTO_E_VIRGULA"
    COLON = "DOIS_PONTOS"
    DOT = "PONTO"


KEYWORDS: dict[str, TokenType] = {
    "program": TokenType.PROGRAM,
    "programa": TokenType.PROGRAM,
    "var": TokenType.VAR,
    "integer": TokenType.INTEGER,
    "inteiro": TokenType.INTEGER,
    "real": TokenType.REAL,
    "boolean": TokenType.BOOLEAN,
    "bool": TokenType.BOOLEAN,
    "booleano": TokenType.BOOLEAN,
    "logico": TokenType.BOOLEAN,
    "lógico": TokenType.BOOLEAN,
    "procedure": TokenType.PROCEDURE,
    "procedimento": TokenType.PROCEDURE,
    "begin": TokenType.BEGIN,
    "inicio": TokenType.BEGIN,
    "início": TokenType.BEGIN,
    "end": TokenType.END,
    "fim": TokenType.END,
    "if": TokenType.IF,
    "se": TokenType.IF,
    "then": TokenType.THEN,
    "entao": TokenType.THEN,
    "então": TokenType.THEN,
    "else": TokenType.ELSE,
    "senao": TokenType.ELSE,
    "senão": TokenType.ELSE,
    "while": TokenType.WHILE,
    "enquanto": TokenType.WHILE,
    "do": TokenType.DO,
    "faca": TokenType.DO,
    "faça": TokenType.DO,
    "read": TokenType.READ,
    "readln": TokenType.READ,
    "leia": TokenType.READ,
    "ler": TokenType.READ,
    "write": TokenType.WRITE,
    "writeln": TokenType.WRITE,
    "escreva": TokenType.WRITE,
    "escrever": TokenType.WRITE,
    "true": TokenType.TRUE,
    "verdadeiro": TokenType.TRUE,
    "false": TokenType.FALSE,
    "falso": TokenType.FALSE,
    "and": TokenType.AND,
    "e": TokenType.AND,
    "or": TokenType.OR,
    "ou": TokenType.OR,
    "not": TokenType.NOT,
    "nao": TokenType.NOT,
    "não": TokenType.NOT,
    "div": TokenType.DIV,
    "mod": TokenType.MOD,
    "modulo": TokenType.MOD,
    "módulo": TokenType.MOD,
}


@dataclass(frozen=True)
class Position:
    line: int
    column: int
    offset: int

    def as_dict(self) -> dict[str, int]:
        return {"linha": self.line, "coluna": self.column, "offset": self.offset}


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    literal: Any
    line: int
    column: int
    offset: int

    @property
    def position(self) -> Position:
        return Position(self.line, self.column, self.offset)

    def as_dict(self) -> dict[str, Any]:
        return {
            "tipo": self.type.value,
            "lexema": self.lexeme,
            "literal": self.literal,
            "linha": self.line,
            "coluna": self.column,
            "offset": self.offset,
        }
