# Compiladores - LALG

Implementação completa de um analisador **léxico** e **sintático** para uma linguagem LALG/Pascal-like, feita em Python e sem dependências obrigatórias externas.

## Funcionalidades

- Reconhecimento de tokens:
	- palavras reservadas em português e inglês (`programa`/`program`, `inicio`/`begin`, `fim`/`end`, etc.);
	- variações comuns como `booleano`, `readln`, `writeln`, `ler`, `escrever`, `módulo`;
	- identificadores;
	- identificadores Unicode com acentos;
	- números inteiros e reais;
	- cadeias com aspas simples ou duplas;
	- operadores aritméticos, relacionais e lógicos;
	- delimitadores;
	- BOM UTF-8 no início do arquivo;
	- comentários `{ ... }`, `(* ... *)` e `// ...`.
- Relatório de erros léxicos com linha e coluna.
- Analisador sintático descendente recursivo.
- Construção de AST simples.
- Tabela de símbolos.
- Declarações de procedimentos com parâmetros opcionais.
- Validações básicas de escopo, declaração/uso e categoria de identificadores.
- Saída textual ou JSON.
- Exemplos e testes automatizados.

## Gramática suportada (resumo)

```text
programa        -> PROGRAM IDENTIFICADOR ';' bloco '.'
bloco           -> declaracoes procedimento* comando_composto
declaracoes     -> VAR (identificador (',' identificador)* ':' tipo ';')*
tipo            -> INTEGER | REAL | BOOLEAN
procedimento    -> PROCEDURE IDENTIFICADOR parametros? ';' bloco ';'
parametros      -> '(' lista_parametros? ')'
lista_parametros-> ids ':' tipo (';' ids ':' tipo)*
comando_composto-> BEGIN comando (';' comando)* END
comando         -> atribuição | chamada | comando_composto | se | enquanto | leia | escreva
atribuição      -> IDENTIFICADOR ':=' expressao
se              -> IF expressao THEN comando (ELSE comando)?
enquanto        -> WHILE expressao DO comando
leia            -> READ '(' IDENTIFICADOR (',' IDENTIFICADOR)* ')'
escreva         -> WRITE '(' expressao (',' expressao)* ')'
```

## Como executar

No diretório do projeto:

```bash
python -m lalg.cli examples/valido.lalg
```

Se o pacote ainda não estiver no `PYTHONPATH`, use:

```bash
PYTHONPATH=src python -m lalg.cli examples/valido.lalg
```

Saída em JSON:

```bash
PYTHONPATH=src python -m lalg.cli examples/valido.lalg --json
```

Apenas análise léxica:

```bash
PYTHONPATH=src python -m lalg.cli examples/valido.lalg --tokens
```

## Instalação opcional em modo editável

```bash
python -m pip install -e .
lalg examples/valido.lalg
```

## Testes

Sem dependências externas:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Com `pytest` instalado, também funciona:

```bash
PYTHONPATH=src pytest
```

Sem `pytest`, ainda é possível validar manualmente com:

```bash
PYTHONPATH=src python -m lalg.cli examples/valido.lalg --json
PYTHONPATH=src python -m lalg.cli examples/invalido.lalg
```

## Estrutura

```text
src/lalg/
	ast.py       # estrutura de AST
	cli.py       # interface de linha de comando
	errors.py    # diagnósticos e exceções
	lexer.py     # analisador léxico
	parser.py    # analisador sintático
	symbols.py   # tabela de símbolos
	tokens.py    # tipos de tokens e palavras reservadas
examples/
	valido.lalg
	invalido.lalg
tests/
	test_lexer.py
	test_parser.py
```
