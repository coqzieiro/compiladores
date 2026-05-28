from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ASTNode:
    kind: str
    value: Any = None
    children: list["ASTNode"] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"tipo": self.kind}
        if self.value is not None:
            data["valor"] = self.value
        if self.children:
            data["filhos"] = [child.as_dict() for child in self.children]
        return data
