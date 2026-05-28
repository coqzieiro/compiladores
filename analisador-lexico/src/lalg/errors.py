from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Diagnostic:
    message: str
    line: int
    column: int
    offset: int
    kind: str = "erro"

    def __str__(self) -> str:
        return f"{self.kind}: {self.message} (linha {self.line}, coluna {self.column})"

    def as_dict(self) -> dict[str, int | str]:
        return {
            "tipo": self.kind,
            "mensagem": self.message,
            "linha": self.line,
            "coluna": self.column,
            "offset": self.offset,
        }


class LALGError(Exception):
    """Erro-base do projeto."""


class LexicalError(LALGError):
    def __init__(self, diagnostic: Diagnostic) -> None:
        super().__init__(str(diagnostic))
        self.diagnostic = diagnostic


class SyntaxErrorLALG(LALGError):
    def __init__(self, diagnostic: Diagnostic) -> None:
        super().__init__(str(diagnostic))
        self.diagnostic = diagnostic
