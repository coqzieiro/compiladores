from __future__ import annotations

from collections.abc import Iterable

from .ast import ASTNode
from .errors import Diagnostic
from .symbols import Symbol, SymbolTable
from .tokens import Token, TokenType


class Parser:
    """Analisador sintático descendente recursivo para LALG/Pascal-like."""

    TYPE_TOKENS = {TokenType.INTEGER, TokenType.REAL, TokenType.BOOLEAN}
    REL_OPS = {
        TokenType.EQUAL,
        TokenType.NOT_EQUAL,
        TokenType.LESS,
        TokenType.LESS_EQUAL,
        TokenType.GREATER,
        TokenType.GREATER_EQUAL,
    }
    ADD_OPS = {TokenType.PLUS, TokenType.MINUS, TokenType.OR}
    MUL_OPS = {TokenType.STAR, TokenType.SLASH, TokenType.DIV, TokenType.MOD, TokenType.AND}
    STATEMENT_START = {
        TokenType.BEGIN,
        TokenType.IF,
        TokenType.WHILE,
        TokenType.READ,
        TokenType.WRITE,
        TokenType.IDENTIFIER,
    }
    DECLARATION_START = {TokenType.VAR, TokenType.PROCEDURE, TokenType.BEGIN}

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0
        self.diagnostics: list[Diagnostic] = []
        self.symbol_table = SymbolTable()
        self._scope_prefix: list[str] = []

    def parse(self) -> tuple[ASTNode | None, list[Diagnostic], SymbolTable]:
        if not self.tokens:
            return None, self.diagnostics, self.symbol_table
        root = self._program()
        if not self._is_at_end():
            self._error(self._peek(), "Tokens após o final do programa.")
        return root, self.diagnostics, self.symbol_table

    def _program(self) -> ASTNode:
        self._consume(TokenType.PROGRAM, "Esperado 'programa'/'program' no início do programa.")
        name = self._consume(TokenType.IDENTIFIER, "Esperado identificador do programa.")
        if name.type is TokenType.IDENTIFIER:
            self._define(name, "programa", None, scoped=False)
        self._consume(TokenType.SEMICOLON, "Esperado ';' após o cabeçalho do programa.")
        block = self._block()
        self._consume(TokenType.DOT, "Esperado '.' ao final do programa.")
        return ASTNode("Programa", name.lexeme if name.type is TokenType.IDENTIFIER else None, [block])

    def _block(self) -> ASTNode:
        children: list[ASTNode] = []
        declarations = self._variable_declarations()
        if declarations.children:
            children.append(declarations)

        procedures: list[ASTNode] = []
        while self._match(TokenType.PROCEDURE):
            procedures.append(self._procedure_declaration())
        if procedures:
            children.append(ASTNode("Procedimentos", children=procedures))

        children.append(self._compound_statement())
        return ASTNode("Bloco", children=children)

    def _variable_declarations(self) -> ASTNode:
        declarations: list[ASTNode] = []
        if not self._match(TokenType.VAR):
            return ASTNode("Declaracoes")

        while not self._is_at_end() and not self._check_any({TokenType.PROCEDURE, TokenType.BEGIN}):
            if not self._check(TokenType.IDENTIFIER):
                self._error(self._peek(), "Esperado identificador na declaração de variável.")
                self._synchronize_declaration()
                continue
            declarations.append(self._single_variable_declaration())
        return ASTNode("Declaracoes", children=declarations)

    def _single_variable_declaration(self) -> ASTNode:
        identifiers = self._identifier_list("Esperado identificador na declaração de variável.")
        self._consume(TokenType.COLON, "Esperado ':' antes do tipo da declaração.")
        type_token = self._consume_any(self.TYPE_TOKENS, "Esperado tipo: inteiro, real ou lógico.")
        self._consume(TokenType.SEMICOLON, "Esperado ';' após declaração.")

        type_name = type_token.lexeme if type_token.type in self.TYPE_TOKENS else None
        nodes: list[ASTNode] = []
        for identifier in identifiers:
            if identifier.type is TokenType.IDENTIFIER:
                self._define(identifier, "variável", type_name, scoped=True)
                nodes.append(ASTNode("Variavel", {"nome": identifier.lexeme, "tipo": type_name}))
        return ASTNode("Declaracao", children=nodes)

    def _procedure_declaration(self) -> ASTNode:
        name = self._consume(TokenType.IDENTIFIER, "Esperado identificador do procedimento.")
        procedure_name = name.lexeme if name.type is TokenType.IDENTIFIER else "procedimento"
        if name.type is TokenType.IDENTIFIER:
            self._define(name, "procedimento", None, scoped=False)

        self._scope_prefix.append(procedure_name)
        params: list[ASTNode] = []
        if self._match(TokenType.LPAREN):
            params = self._formal_parameter_list()
            self._consume(TokenType.RPAREN, "Esperado ')' após parâmetros do procedimento.")

        self._consume(TokenType.SEMICOLON, "Esperado ';' após cabeçalho do procedimento.")
        block = self._block()
        self._consume(TokenType.SEMICOLON, "Esperado ';' após declaração de procedimento.")
        self._scope_prefix.pop()

        children = []
        if params:
            children.append(ASTNode("Parametros", children=params))
        children.append(block)
        return ASTNode("Procedimento", procedure_name, children)

    def _formal_parameter_list(self) -> list[ASTNode]:
        params: list[ASTNode] = []
        if self._check(TokenType.RPAREN):
            return params

        while not self._is_at_end():
            identifiers = self._identifier_list("Esperado identificador na lista de parâmetros.")
            self._consume(TokenType.COLON, "Esperado ':' antes do tipo do parâmetro.")
            type_token = self._consume_any(self.TYPE_TOKENS, "Esperado tipo do parâmetro.")
            type_name = type_token.lexeme if type_token.type in self.TYPE_TOKENS else None
            for identifier in identifiers:
                if identifier.type is TokenType.IDENTIFIER:
                    self._define(identifier, "parâmetro", type_name, scoped=True)
                    params.append(ASTNode("Parametro", {"nome": identifier.lexeme, "tipo": type_name}))
            if not self._match(TokenType.SEMICOLON):
                break
        return params

    def _identifier_list(self, message: str) -> list[Token]:
        identifiers = [self._consume(TokenType.IDENTIFIER, message)]
        while self._match(TokenType.COMMA):
            identifiers.append(self._consume(TokenType.IDENTIFIER, "Esperado identificador após ','."))
        return identifiers

    def _compound_statement(self) -> ASTNode:
        self._consume(TokenType.BEGIN, "Esperado 'início'/'begin' para iniciar bloco de comandos.")
        commands: list[ASTNode] = []

        while not self._check(TokenType.END) and not self._is_at_end():
            if self._match(TokenType.SEMICOLON):
                continue
            commands.append(self._statement())
            if self._check(TokenType.END) or self._check(TokenType.ELSE):
                break
            if not self._match(TokenType.SEMICOLON):
                self._error(self._peek(), "Esperado ';' entre comandos.")
                self._synchronize_statement()

        self._consume(TokenType.END, "Esperado 'fim'/'end' para encerrar bloco de comandos.")
        return ASTNode("ComandoComposto", children=commands)

    def _statement(self) -> ASTNode:
        if self._check(TokenType.BEGIN):
            return self._compound_statement()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.READ):
            return self._read_statement()
        if self._match(TokenType.WRITE):
            return self._write_statement()
        if self._check(TokenType.IDENTIFIER):
            return self._identifier_statement()

        self._error(self._peek(), "Comando inválido.")
        if not self._is_at_end():
            self._advance()
        return ASTNode("ComandoInvalido")

    def _identifier_statement(self) -> ASTNode:
        identifier = self._advance()
        if self._match(TokenType.ASSIGN):
            expr = self._expression()
            self._require_declared(identifier, expected_categories={"variável", "parâmetro"})
            return ASTNode("Atribuicao", identifier.lexeme, [expr])

        arguments: list[ASTNode] = []
        if self._match(TokenType.LPAREN):
            arguments = self._argument_list()
            self._consume(TokenType.RPAREN, "Esperado ')' após argumentos.")
        self._require_declared(identifier, expected_categories={"procedimento"})
        return ASTNode("ChamadaProcedimento", identifier.lexeme, arguments)

    def _if_statement(self) -> ASTNode:
        condition = self._expression()
        self._consume(TokenType.THEN, "Esperado 'então'/'then' após condição do se/if.")
        then_branch = self._statement()
        children = [condition, then_branch]
        if self._match(TokenType.ELSE):
            children.append(self._statement())
        return ASTNode("Se", children=children)

    def _while_statement(self) -> ASTNode:
        condition = self._expression()
        self._consume(TokenType.DO, "Esperado 'faça'/'do' após condição do enquanto/while.")
        body = self._statement()
        return ASTNode("Enquanto", children=[condition, body])

    def _read_statement(self) -> ASTNode:
        self._consume(TokenType.LPAREN, "Esperado '(' após leia/read.")
        identifiers: list[ASTNode] = []
        if not self._check(TokenType.RPAREN):
            for token in self._identifier_list("Esperado identificador em leia/read."):
                if token.type is TokenType.IDENTIFIER:
                    self._require_declared(token, expected_categories={"variável", "parâmetro"})
                    identifiers.append(ASTNode("Identificador", token.lexeme))
        self._consume(TokenType.RPAREN, "Esperado ')' após lista do leia/read.")
        return ASTNode("Leia", children=identifiers)

    def _write_statement(self) -> ASTNode:
        self._consume(TokenType.LPAREN, "Esperado '(' após escreva/write.")
        arguments = self._argument_list()
        self._consume(TokenType.RPAREN, "Esperado ')' após lista do escreva/write.")
        return ASTNode("Escreva", children=arguments)

    def _argument_list(self) -> list[ASTNode]:
        arguments: list[ASTNode] = []
        if self._check(TokenType.RPAREN):
            return arguments
        arguments.append(self._expression())
        while self._match(TokenType.COMMA):
            arguments.append(self._expression())
        return arguments

    def _expression(self) -> ASTNode:
        expr = self._simple_expression()
        while self._peek().type in self.REL_OPS:
            operator = self._advance()
            right = self._simple_expression()
            expr = ASTNode("ExpressaoBinaria", operator.lexeme, [expr, right])
        return expr

    def _simple_expression(self) -> ASTNode:
        if self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            expr = ASTNode("ExpressaoUnaria", operator.lexeme, [self._term()])
        else:
            expr = self._term()
        while self._peek().type in self.ADD_OPS:
            operator = self._advance()
            expr = ASTNode("ExpressaoBinaria", operator.lexeme, [expr, self._term()])
        return expr

    def _term(self) -> ASTNode:
        expr = self._factor()
        while self._peek().type in self.MUL_OPS:
            operator = self._advance()
            expr = ASTNode("ExpressaoBinaria", operator.lexeme, [expr, self._factor()])
        return expr

    def _factor(self) -> ASTNode:
        if self._match(TokenType.IDENTIFIER):
            token = self._previous()
            self._require_declared(token)
            return ASTNode("Identificador", token.lexeme)
        if self._match(TokenType.INTEGER_LITERAL, TokenType.REAL_LITERAL, TokenType.STRING_LITERAL, TokenType.TRUE, TokenType.FALSE):
            token = self._previous()
            return ASTNode("Literal", token.literal if token.literal is not None else token.lexeme)
        if self._match(TokenType.NOT):
            return ASTNode("ExpressaoUnaria", self._previous().lexeme, [self._factor()])
        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Esperado ')' após expressão.")
            return expr

        self._error(self._peek(), "Esperado identificador, literal ou expressão entre parênteses.")
        if not self._is_at_end():
            self._advance()
        return ASTNode("ExpressaoInvalida")

    def _define(self, token: Token, category: str, type_name: str | None, *, scoped: bool) -> None:
        name = self._scoped_name(token.lexeme) if scoped else token.lexeme
        if not self.symbol_table.define(Symbol(name, category, type_name, token.line, token.column)):
            self._error(token, f"Identificador '{token.lexeme}' já declarado neste escopo.")

    def _require_declared(self, token: Token, expected_categories: set[str] | None = None) -> None:
        symbol = self._lookup(token.lexeme)
        if symbol is None:
            self._error(token, f"Identificador '{token.lexeme}' não declarado.")
            return
        if expected_categories and symbol.category not in expected_categories:
            expected = "/".join(sorted(expected_categories))
            self._error(token, f"Identificador '{token.lexeme}' usado como {expected}, mas declarado como {symbol.category}.")

    def _lookup(self, name: str) -> Symbol | None:
        for scope in self._scope_search_order():
            symbol = self.symbol_table.lookup(f"{scope}.{name}")
            if symbol is not None:
                return symbol
        return self.symbol_table.lookup(name)

    def _scoped_name(self, name: str) -> str:
        scope = ".".join(self._scope_prefix)
        return f"{scope}.{name}" if scope else name

    def _scope_search_order(self) -> list[str]:
        return [".".join(self._scope_prefix[:index]) for index in range(len(self._scope_prefix), 0, -1)]

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        self._error(self._peek(), message)
        return self._dummy(token_type)

    def _consume_any(self, token_types: Iterable[TokenType], message: str) -> Token:
        token_type_set = set(token_types)
        if self._peek().type in token_type_set:
            return self._advance()
        self._error(self._peek(), message)
        return self._dummy(next(iter(token_type_set)))

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return token_type is TokenType.EOF
        return self._peek().type is token_type

    def _check_any(self, token_types: set[TokenType]) -> bool:
        return self._peek().type in token_types

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type is TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _dummy(self, expected: TokenType) -> Token:
        current = self._peek()
        return Token(expected, "", None, current.line, current.column, current.offset)

    def _error(self, token: Token, message: str) -> None:
        if self.diagnostics and self.diagnostics[-1].offset == token.offset and self.diagnostics[-1].message == message:
            return
        self.diagnostics.append(Diagnostic(message, token.line, token.column, token.offset, "erro sintático"))

    def _synchronize_declaration(self) -> None:
        while not self._is_at_end() and not self._check_any(self.DECLARATION_START | {TokenType.SEMICOLON}):
            self._advance()
        self._match(TokenType.SEMICOLON)

    def _synchronize_statement(self) -> None:
        while not self._is_at_end() and not self._check_any(self.STATEMENT_START | {TokenType.SEMICOLON, TokenType.END, TokenType.ELSE}):
            self._advance()
        self._match(TokenType.SEMICOLON)
