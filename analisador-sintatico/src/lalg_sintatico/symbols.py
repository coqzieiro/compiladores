from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Symbol:
    name: str
    category: str
    type_name: str | None
    line: int
    column: int

    def as_dict(self) -> dict[str, int | str | None]:
        return {
            "nome": self.name,
            "categoria": self.category,
            "tipo": self.type_name,
            "linha": self.line,
            "coluna": self.column,
        }


@dataclass
class SymbolTable:
    symbols: dict[str, Symbol] = field(default_factory=dict)

    def define(self, symbol: Symbol) -> bool:
        key = symbol.name.lower()
        if key in self.symbols:
            return False
        self.symbols[key] = symbol
        return True

    def lookup(self, name: str) -> Symbol | None:
        return self.symbols.get(name.lower())

    def as_list(self) -> list[dict[str, int | str | None]]:
        return [symbol.as_dict() for symbol in self.symbols.values()]
