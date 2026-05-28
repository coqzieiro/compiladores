# Analisador Sintático — LALG

Implementação completa de um analisador sintático descendente recursivo para uma linguagem LALG/Pascal-like.

## O que foi implementado

- Análise léxica auxiliar para gerar tokens de entrada.
- Análise sintática com recuperação de erros.
- AST em formato de árvore serializável para JSON.
- Tabela de símbolos com escopos simples.
- Validações básicas de uso de identificadores declarados.
- Procedimentos com parâmetros opcionais.
- Comandos `inicio/fim`, atribuição, chamada de procedimento, `se/senao`, `enquanto`, `leia` e `escreva`.
- Expressões aritméticas, relacionais e lógicas com precedência.

## Gramática suportada

```text
programa        -> PROGRAM IDENTIFICADOR ';' bloco '.'
bloco           -> declaracoes procedimento* comando_composto
declaracoes     -> VAR (ids ':' tipo ';')*
ids             -> IDENTIFICADOR (',' IDENTIFICADOR)*
tipo            -> INTEGER | REAL | BOOLEAN
procedimento    -> PROCEDURE IDENTIFICADOR parametros? ';' bloco ';'
parametros      -> '(' lista_parametros? ')'
lista_parametros-> ids ':' tipo (';' ids ':' tipo)*
comando_composto-> BEGIN comando (';' comando)* END
comando         -> atribuição | chamada | comando_composto | se | enquanto | leia | escreva
atribuição      -> IDENTIFICADOR ':=' expressao
chamada         -> IDENTIFICADOR ('(' argumentos? ')')?
se              -> IF expressao THEN comando (ELSE comando)?
enquanto        -> WHILE expressao DO comando
leia            -> READ '(' ids ')'
escreva         -> WRITE '(' argumentos? ')'
argumentos      -> expressao (',' expressao)*
expressao       -> expressao_simples (op_rel expressao_simples)*
```

## Como executar

Dentro da pasta deste projeto:

```bash
PYTHONPATH=src python -m lalg_sintatico.cli examples/valido.lalg
```

Saída completa em JSON:

```bash
PYTHONPATH=src python -m lalg_sintatico.cli examples/valido.lalg --json
```

Apenas tokens:

```bash
PYTHONPATH=src python -m lalg_sintatico.cli examples/valido.lalg --tokens
```

## Testes

Sem dependências externas:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Estrutura

```text
src/lalg_sintatico/
  ast.py       # nós da AST
  cli.py       # interface de linha de comando
  errors.py    # diagnósticos
  lexer.py     # léxico auxiliar
  parser.py    # analisador sintático
  symbols.py   # tabela de símbolos
  tokens.py    # tokens e palavras reservadas
examples/
  valido.lalg
  invalido.lalg
tests/
  test_lexer.py
  test_parser.py
```
