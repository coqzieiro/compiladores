from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class TokenType(str, Enum):
    # Especiais
    EOF = "EOF"
    IDENTIFIER = "IDENTIFICADOR"
    INTEGER_LITERAL = "NUMERO_INTEIRO"
    REAL_LITERAL = "NUMERO_REAL"
    STRING_LITERAL = "CADEIA"

    # Palavras reservadas canônicas
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

    # Operadores e delimitadores
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
    # Inglês/Pascal
    "program": TokenType.PROGRAM,
    "var": TokenType.VAR,
    "integer": TokenType.INTEGER,
    "real": TokenType.REAL,
    "boolean": TokenType.BOOLEAN,
    "bool": TokenType.BOOLEAN,
    "procedure": TokenType.PROCEDURE,
    "begin": TokenType.BEGIN,
    "end": TokenType.END,
    "if": TokenType.IF,
    "then": TokenType.THEN,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "do": TokenType.DO,
    "read": TokenType.READ,
    "readln": TokenType.READ,
    "write": TokenType.WRITE,
    "writeln": TokenType.WRITE,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "div": TokenType.DIV,
    "mod": TokenType.MOD,
    # Português comum em LALG
    "programa": TokenType.PROGRAM,
    "inteiro": TokenType.INTEGER,
    "logico": TokenType.BOOLEAN,
    "lógico": TokenType.BOOLEAN,
    "booleano": TokenType.BOOLEAN,
    "procedimento": TokenType.PROCEDURE,
    "inicio": TokenType.BEGIN,
    "início": TokenType.BEGIN,
    "fim": TokenType.END,
    "se": TokenType.IF,
    "entao": TokenType.THEN,
    "então": TokenType.THEN,
    "senao": TokenType.ELSE,
    "senão": TokenType.ELSE,
    "enquanto": TokenType.WHILE,
    "faca": TokenType.DO,
    "faça": TokenType.DO,
    "leia": TokenType.READ,
    "ler": TokenType.READ,
    "escreva": TokenType.WRITE,
    "escrever": TokenType.WRITE,
    "verdadeiro": TokenType.TRUE,
    "falso": TokenType.FALSE,
    "e": TokenType.AND,
    "ou": TokenType.OR,
    "nao": TokenType.NOT,
    "não": TokenType.NOT,
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
