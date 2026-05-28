from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .lexer import Lexer
from .parser import Parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lalg-sintatico",
        description="Analisador sintático para LALG.",
    )
    parser.add_argument("arquivo", type=Path, help="Arquivo-fonte .lalg/.pas a ser analisado.")
    parser.add_argument("--json", action="store_true", help="Imprime tokens, erros, AST e tabela de símbolos em JSON.")
    parser.add_argument("--tokens", action="store_true", help="Mostra somente a análise léxica auxiliar.")
    return parser


def analyze(source: str) -> dict[str, Any]:
    lexer = Lexer(source)
    tokens, lexical_errors = lexer.scan_tokens()
    parser = Parser(tokens)
    ast, syntax_errors, symbol_table = parser.parse()
    return {
        "tokens": [token.as_dict() for token in tokens],
        "erros_lexicos": [error.as_dict() for error in lexical_errors],
        "erros_sintaticos": [error.as_dict() for error in syntax_errors],
        "tabela_simbolos": symbol_table.as_list(),
        "ast": ast.as_dict() if ast else None,
    }


def _print_tokens(result: dict[str, Any]) -> None:
    for token in result["tokens"]:
        print(f"{token['linha']:>4}:{token['coluna']:<3} {token['tipo']:<18} {token['lexema']!r}")


def _print_diagnostics(title: str, diagnostics: list[dict[str, Any]]) -> None:
    if not diagnostics:
        return
    print(f"\n{title}:")
    for diagnostic in diagnostics:
        print(f"- {diagnostic['mensagem']} (linha {diagnostic['linha']}, coluna {diagnostic['coluna']})")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        source = args.arquivo.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Erro ao ler arquivo: {exc}", file=sys.stderr)
        return 2

    result = analyze(source)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.tokens:
        _print_tokens(result)
        _print_diagnostics("Erros léxicos", result["erros_lexicos"])
    else:
        _print_diagnostics("Erros léxicos", result["erros_lexicos"])
        _print_diagnostics("Erros sintáticos/semânticos simples", result["erros_sintaticos"])
        if not result["erros_lexicos"] and not result["erros_sintaticos"]:
            print("Análise sintática concluída com sucesso.")
        print("\nTabela de símbolos:")
        for symbol in result["tabela_simbolos"]:
            print(f"- {symbol['nome']} ({symbol['categoria']}, tipo={symbol['tipo']})")

    return 1 if result["erros_lexicos"] or result["erros_sintaticos"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
