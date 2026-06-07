# Relatório — Trabalho 1: Analisador Léxico (LALG)

> Disciplina: **SCC0217 — Linguagens de Programação e Compiladores**
> Professor: **Dr. Diego Raphael Amancio** — `diego@icmc.usp.br`
> Linguagem analisada: **LALG** (Pascal-like)

## 1. Membros do grupo

> ⚠️ **Preencher antes da entrega.** Inclua nome completo e número USP (NUSP) de cada
> integrante:
>
> - `Nome 1` — NUSP `xxxxxxxx`
> - `Nome 2` — NUSP `xxxxxxxx`
> - `Nome 3` — NUSP `xxxxxxxx`

## 2. Visão geral

Este trabalho implementa o **analisador léxico** da linguagem LALG **manualmente em
Python 3**, conforme permitido pela especificação ("O grupo pode decidir por implementar o
analisador de maneira manual, sem o uso das ferramentas mencionadas").

A entrada é um arquivo-fonte `.lalg` (ou `.pas`) e a saída é a lista de tokens reconhecidos
no formato `<lexema, token>`, junto com diagnósticos de erro. Há dois modos de saída:

- **modo padrão** — formato amigável `linha:coluna  TIPO  'lexema'`;
- **modo `--json`** — saída completa estruturada (tokens, erros, AST e tabela de símbolos);
- saída no estilo dos exemplos do PDF (`lexema - rótulo`) está disponível em
  [`saidas/lexico-valido-pdf.txt`](saidas/lexico-valido-pdf.txt) e
  [`saidas/lexico-invalido-pdf.txt`](saidas/lexico-invalido-pdf.txt).

O código-fonte está em [`analisador-lexico/src/lalg/`](../analisador-lexico/src/lalg).

## 3. Decisões de projeto e justificativas

### 3.1. Implementação manual em Python (sem lex/flex/JavaCC)

O enunciado permite implementação manual. Optamos por essa abordagem porque:

- evita dependências externas e build de C/Java na máquina do avaliador;
- torna o código auto-contido, legível e fácil de inspecionar em sala;
- permite reaproveitamento direto do mesmo módulo no Trabalho 2 (analisador sintático).

### 3.2. Representação dos tokens — `<palavra_reservada, simb_palavra_reservada>`

Conforme o item 1 das "decisões de projeto" do PDF:

> *<palavra_reservada, palavra_reservada> ou <palavra_reservada, simb_palavra_reservada>.
> Para facilitar o entendimento, não utilize códigos numéricos para os tokens.*

Adotamos **identificadores simbólicos** (`enum TokenType` em
[tokens.py](../analisador-lexico/src/lalg/tokens.py)), nunca códigos numéricos. Cada token
tem um nome textual descritivo (`PROGRAM`, `SEMICOLON`, `IDENTIFIER`, `INTEGER_LITERAL`
etc.). Uma camada de exibição mapeia esses nomes para os rótulos do PDF (`program`,
`simb_ponto_virgula`, `id`, `num_int`, …) — ver
[`saidas/lexico-valido-pdf.txt`](saidas/lexico-valido-pdf.txt).

### 3.3. Tabela de palavras reservadas — `dict` (hashing perfeito)

Conforme o item 2 das decisões de projeto:

> *Implementação da tabela de palavras reservadas: escolha da estrutura de dados e da função
> de busca. Note que a busca deve ser eficiente.*

A tabela é um `dict[str, TokenType]` (`KEYWORDS` em
[tokens.py](../analisador-lexico/src/lalg/tokens.py)), implementado em CPython com tabela
hash. A busca custa **O(1) em média** (e amortizado), o que atende ao requisito de
eficiência. Como a chave é normalizada para minúsculas com `unicodedata.normalize("NFC", …)`
antes da consulta, identificadores acentuados (`início`, `não`, `lógico`) são reconhecidos
de forma consistente.

A tabela contempla tanto as palavras em inglês/Pascal (`program`, `begin`, `end`, `if`,
`then`, `else`, `while`, `do`, `read`, `write`, …) quanto as variantes em português usuais
em LALG (`programa`, `inicio`, `fim`, `se`, `entao`, `senao`, `enquanto`, `faca`, `leia`,
`escreva`, `verdadeiro`, `falso`, `e`, `ou`, `nao`, `modulo`, …).

### 3.4. Estratégia de tratamento de erros — específica e não bloqueante

Conforme o item 3 das decisões de projeto:

> *Como lidar com erros? Erros genéricos ou mais específicos?*

Optamos por **mensagens específicas** e **modo "panic local"**: o analisador não
interrompe na primeira ocorrência — ele registra um diagnóstico (linha, coluna, mensagem)
e segue varrendo o arquivo. Assim conseguimos relatar **todos** os erros léxicos numa única
execução.

Erros distintos produzem mensagens distintas, por exemplo:

- `Caractere inesperado '@'.`
- `Número malformado '9x'. Identificadores não podem iniciar por dígito.`
- `Cadeia de caracteres não pode atravessar linha.`
- `Cadeia de caracteres não finalizada.`
- `Comentário de bloco não finalizado.`

A definição do diagnóstico vive em
[errors.py](../analisador-lexico/src/lalg/errors.py).

### 3.5. Tratamento de comentários

Suportamos os três formatos de comentário comuns em LALG/Pascal:

- bloco no estilo Pascal: `{ ... }`;
- bloco alternativo: `(* ... *)`;
- linha: `// ...` até o fim da linha.

Comentários **não geram tokens** e seu não-fechamento é reportado como erro léxico. Isso
atende o item de avaliação "tratamento de comentários".

### 3.6. Programa principal varrendo o arquivo inteiro

O CLI ([cli.py](../analisador-lexico/src/lalg/cli.py)) recebe o arquivo, chama
`Lexer.scan_tokens()` em loop interno (cada chamada ao método `_scan_token` retorna **um**
par `<lexema,token>`), imprime o resultado e termina com:

- código `0` se nenhum erro foi detectado;
- código `1` se houver erros léxicos.

Isso satisfaz o item de avaliação "presença de programa principal executando o analisador
léxico várias vezes".

## 4. Modelagem da tarefa léxica

### 4.1. Conjunto de tokens

Resumo das categorias (lista completa em
[especificacao-lexica.md](especificacao-lexica.md)):

| Categoria | Exemplos de lexema | Token |
|-----------|--------------------|-------|
| Palavras reservadas (canônicas) | `program`, `var`, `integer`, `real`, `boolean`, `procedure`, `begin`, `end`, `if`, `then`, `else`, `while`, `do`, `read`, `write`, `true`, `false`, `and`, `or`, `not`, `div`, `mod` | `PROGRAM`, `VAR`, `INTEGER`, … |
| Palavras reservadas (PT) | `programa`, `inteiro`, `booleano`, `inicio`, `fim`, `se`, `entao`, `senao`, `enquanto`, `faca`, `leia`, `escreva`, `verdadeiro`, `falso`, `e`, `ou`, `nao`, `modulo` | mapeadas para os mesmos tokens canônicos |
| Identificador | `x`, `media`, `minha_variavel` | `IDENTIFICADOR` |
| Número inteiro | `42`, `0`, `1` | `NUMERO_INTEIRO` |
| Número real | `2.0`, `3.14` | `NUMERO_REAL` |
| Cadeia | `"aprovado"`, `'oi'` | `CADEIA` |
| Operadores aritméticos | `+`, `-`, `*`, `/` | `MAIS`, `MENOS`, `MULTIPLICACAO`, `DIVISAO` |
| Operador de atribuição | `:=` | `ATRIBUICAO` |
| Operadores relacionais | `=`, `<>`, `!=`, `<`, `<=`, `>`, `>=` | `IGUAL`, `DIFERENTE`, `MENOR`, … |
| Delimitadores | `(`, `)`, `,`, `;`, `:`, `.` | `ABRE_PARENTESE`, … |

### 4.2. Expressões regulares utilizadas

```text
identificador  ::= [A-Za-z_][A-Za-z_0-9]*           (com Unicode NFC)
inteiro        ::= [0-9]+
real           ::= [0-9]+\.[0-9]+
cadeia         ::= "([^"\n]|\\.)*"  |  '([^'\n]|\\.)*'
atribuicao     ::= ":="
maior_igual    ::= ">="
menor_igual    ::= "<="
diferente      ::= "<>" | "!="
comentario_bloco_chaves    ::= "{" .* "}"
comentario_bloco_pascal    ::= "(*" .* "*)"
comentario_linha           ::= "//" [^\n]*
```

A especificação completa, no estilo lex, está em
[especificacao-lexica.md](especificacao-lexica.md).

### 4.3. Tratamento de erros (modelagem)

Cada erro léxico produz um `Diagnostic(message, line, column, offset, kind="erro léxico")`.
Estratégia:

- **caractere inesperado** → reporta e descarta apenas aquele caractere;
- **número malformado** (dígito seguido de letras, ex. `9x`, `1.a23`) → consome a sequência
  inteira, reporta e segue;
- **cadeia atravessando linha** ou **não finalizada** → reporta e segue;
- **comentário de bloco não finalizado** → reporta e segue até `EOF`.

## 5. Estrutura do código

```text
analisador-lexico/src/lalg/
  tokens.py    # TokenType (enum), Token, Position, KEYWORDS (dict hash)
  lexer.py     # classe Lexer; scan_tokens() devolve (tokens, erros)
  errors.py    # Diagnostic e exceções
  cli.py       # programa principal; argparse; impressão dos pares <lexema,token>
  parser.py    # (também aqui — usado no Trabalho 2)
  ast.py       # nós da AST (não é exigido pelo Trabalho 1)
  symbols.py   # tabela de símbolos (não é exigido pelo Trabalho 1)
```

## 6. Passo a passo: como compilar e executar

> Não há etapa de "compilação" — Python é interpretado.

```bash
# 1) Garanta Python >= 3.10
python3 --version

# 2) Entre na pasta do analisador léxico
cd analisador-lexico

# 3) Execute o analisador sobre um arquivo-fonte
PYTHONPATH=src python3 -m lalg.cli examples/valido.lalg

# 4) Variações úteis
PYTHONPATH=src python3 -m lalg.cli examples/valido.lalg --tokens   # só léxico
PYTHONPATH=src python3 -m lalg.cli examples/valido.lalg --json     # JSON completo
PYTHONPATH=src python3 -m lalg.cli examples/invalido.lalg          # mostra erros
```

Opcionalmente, é possível instalar como console-script:

```bash
python3 -m pip install -e .
lalg examples/valido.lalg
```

## 7. Exemplos de execução

### 7.1. Programa válido — [`exemplos-fonte/lexico-valido.lalg`](exemplos-fonte/lexico-valido.lalg)

```pascal
programa exemplo;
var
  x, y: inteiro;
  media: real;
  ok: logico;
inicio
  leia(x, y);
  media := (x + y) / 2.0;
  ok := media >= 6.0;
  se ok entao
    escreva("aprovado", media)
  senao
    escreva("reprovado", media)
fim.
```

Saída no estilo do PDF (trecho — completo em
[`saidas/lexico-valido-pdf.txt`](saidas/lexico-valido-pdf.txt)):

```text
programa - program
exemplo - id
; - simb_ponto_virgula
var - var
x - id
, - simb_virgula
y - id
: - simb_dois_pontos
inteiro - integer
; - simb_ponto_virgula
...
fim - end
. - simb_ponto
```

Saída amigável (trecho — completo em
[`saidas/lexico-valido.txt`](saidas/lexico-valido.txt)):

```text
   1:1   PROGRAM            'programa'
   1:10  IDENTIFICADOR      'exemplo'
   1:17  PONTO_E_VIRGULA    ';'
   2:1   VAR                'var'
   3:3   IDENTIFICADOR      'x'
...
```

### 7.2. Programa inválido — [`exemplos-fonte/lexico-invalido.lalg`](exemplos-fonte/lexico-invalido.lalg)

```pascal
programa exemplo;
var
  9x: inteiro;
inicio
  x := 10
  escreva(@)
fim
```

Erros léxicos detectados (saída completa em
[`saidas/lexico-invalido.txt`](saidas/lexico-invalido.txt)):

```text
Erros léxicos:
- Número malformado '9x'. Identificadores não podem iniciar por dígito. (linha 3, coluna 3)
- Caractere inesperado '@'. (linha 6, coluna 11)
```

Esse caso reproduz o cenário do segundo exemplo do PDF
(`@ - erro - simbolo nao pertencente a linguagem` e
`numero real mal formado`).

### 7.3. Saída JSON resumida (trecho)

```json
{
  "tokens": [
    {"tipo": "PROGRAM", "lexema": "programa", "linha": 1, "coluna": 1, ...},
    {"tipo": "IDENTIFICADOR", "lexema": "exemplo", "linha": 1, "coluna": 10, ...},
    ...
  ],
  "erros_lexicos": [
    {"tipo": "erro léxico",
     "mensagem": "Número malformado '9x'...",
     "linha": 3, "coluna": 3, ...}
  ]
}
```

JSON completo em [`saidas/lexico-valido.json`](saidas/lexico-valido.json) e
[`saidas/lexico-invalido.json`](saidas/lexico-invalido.json).

## 8. Testes automatizados

```bash
cd analisador-lexico
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Resultado (cópia em [`saidas/testes-lexico.txt`](saidas/testes-lexico.txt)):

```text
test_accepts_unicode_identifiers_bom_and_not_equal (test_lexer.LexerTest) ... ok
test_comments_are_ignored (test_lexer.LexerTest) ... ok
test_keywords_identifiers_numbers_and_operators (test_lexer.LexerTest) ... ok
test_reports_invalid_character_and_bad_number (test_lexer.LexerTest) ... ok
test_procedure_with_parameters_local_variables_and_call (test_parser.ParserTest) ... ok
test_reports_missing_declaration (test_parser.ParserTest) ... ok
test_reports_syntax_error (test_parser.ParserTest) ... ok
test_valid_program_parses_without_errors (test_parser.ParserTest) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.002s

OK
```

## 9. Itens da rubrica do PDF — onde cada um foi atendido

| Item da rubrica | Onde foi atendido |
|-----------------|-------------------|
| **10% — Relatório / especificação** | Este arquivo + [especificacao-lexica.md](especificacao-lexica.md). |
| **80% — Análise léxica e tratamento de erros** | [lexer.py](../analisador-lexico/src/lalg/lexer.py) + casos de teste em [tests/test_lexer.py](../analisador-lexico/tests/test_lexer.py) + saídas reais em [saidas/](saidas/). |
| **10% — Tabela de reservadas eficiente, programa principal, comentários** | `KEYWORDS` (`dict` hash) em [tokens.py](../analisador-lexico/src/lalg/tokens.py); programa principal em [cli.py](../analisador-lexico/src/lalg/cli.py); tratamento de `{}`, `(* *)` e `//` em [lexer.py](../analisador-lexico/src/lalg/lexer.py). |
