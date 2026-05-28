from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .lexer import Lexer
from .parser import Parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lalg",
        description="Analisador léxico e sintático para LALG.",
    )
    parser.add_argument("arquivo", type=Path, help="Arquivo-fonte .lalg/.pas a ser analisado.")
    parser.add_argument("--json", action="store_true", help="Imprime tokens, erros, AST e tabela de símbolos em JSON.")
    parser.add_argument("--tokens", action="store_true", help="Mostra somente a análise léxica.")
    parser.add_argument("--no-syntax", action="store_true", help="Não executa análise sintática.")
    return parser


def analyze(source: str) -> dict[str, object]:
    lexer = Lexer(source)
    tokens, lexical_errors = lexer.scan_tokens()
    result: dict[str, object] = {
        "tokens": [token.as_dict() for token in tokens],
        "erros_lexicos": [error.as_dict() for error in lexical_errors],
    }

    parser = Parser(tokens)
    ast, syntax_errors, symbol_table = parser.parse()
    result.update(
        {
            "erros_sintaticos": [error.as_dict() for error in syntax_errors],
            "tabela_simbolos": symbol_table.as_list(),
            "ast": ast.as_dict() if ast else None,
        }
    )
    return result


def _print_tokens(result: dict[str, object]) -> None:
    for token in result["tokens"]:  # type: ignore[index]
        print(
            f"{token['linha']:>4}:{token['coluna']:<3} "  # type: ignore[index]
            f"{token['tipo']:<18} {token['lexema']!r}"  # type: ignore[index]
        )


def _print_diagnostics(title: str, diagnostics: list[dict[str, object]]) -> None:
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

    lexer = Lexer(source)
    tokens, lexical_errors = lexer.scan_tokens()

    if args.tokens or args.no_syntax:
        result: dict[str, object] = {
            "tokens": [token.as_dict() for token in tokens],
            "erros_lexicos": [error.as_dict() for error in lexical_errors],
        }
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            _print_tokens(result)
            _print_diagnostics("Erros léxicos", result["erros_lexicos"])  # type: ignore[arg-type]
        return 1 if lexical_errors else 0

    parser = Parser(tokens)
    ast, syntax_errors, symbol_table = parser.parse()
    result = {
        "tokens": [token.as_dict() for token in tokens],
        "erros_lexicos": [error.as_dict() for error in lexical_errors],
        "erros_sintaticos": [error.as_dict() for error in syntax_errors],
        "tabela_simbolos": symbol_table.as_list(),
        "ast": ast.as_dict() if ast else None,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_tokens(result)
        _print_diagnostics("Erros léxicos", result["erros_lexicos"])  # type: ignore[arg-type]
        _print_diagnostics("Erros sintáticos/semânticos simples", result["erros_sintaticos"])  # type: ignore[arg-type]
        print("\nTabela de símbolos:")
        for symbol in result["tabela_simbolos"]:  # type: ignore[index]
            print(f"- {symbol['nome']} ({symbol['categoria']}, tipo={symbol['tipo']})")  # type: ignore[index]

    return 1 if lexical_errors or syntax_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
