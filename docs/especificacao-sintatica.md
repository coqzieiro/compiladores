# Especificação sintática — LALG

Listagem da gramática implementada, no estilo YACC. A implementação real, manual em
Python, está em
[`analisador-sintatico/src/lalg_sintatico/parser.py`](../analisador-sintatico/src/lalg_sintatico/parser.py);
este documento é a versão "papel" pedida pelo enunciado do Trabalho 2.

## 1. Tokens declarados (cabeçalho YACC)

```yacc
%token PROGRAM VAR PROCEDURE BEGIN END IF THEN ELSE WHILE DO READ WRITE
%token INTEGER REAL BOOLEAN
%token TRUE FALSE AND OR NOT DIV MOD
%token IDENTIFICADOR NUMERO_INTEIRO NUMERO_REAL CADEIA
%token MAIS MENOS MULTIPLICACAO DIVISAO
%token ATRIBUICAO IGUAL DIFERENTE MENOR MENOR_IGUAL MAIOR MAIOR_IGUAL
%token ABRE_PARENTESE FECHA_PARENTESE VIRGULA PONTO_E_VIRGULA DOIS_PONTOS PONTO
```

## 2. Gramática (estilo YACC)

```yacc
programa
    : PROGRAM IDENTIFICADOR PONTO_E_VIRGULA bloco PONTO
    ;

bloco
    : declaracoes lista_procedimentos comando_composto
    ;

declaracoes
    : /* vazio */
    | VAR lista_declaracoes
    ;

lista_declaracoes
    : declaracao
    | lista_declaracoes declaracao
    ;

declaracao
    : lista_ids DOIS_PONTOS tipo PONTO_E_VIRGULA
    ;

lista_ids
    : IDENTIFICADOR
    | lista_ids VIRGULA IDENTIFICADOR
    ;

tipo
    : INTEGER
    | REAL
    | BOOLEAN
    ;

lista_procedimentos
    : /* vazio */
    | lista_procedimentos procedimento
    ;

procedimento
    : PROCEDURE IDENTIFICADOR parametros_opt PONTO_E_VIRGULA bloco PONTO_E_VIRGULA
    ;

parametros_opt
    : /* vazio */
    | ABRE_PARENTESE lista_parametros FECHA_PARENTESE
    ;

lista_parametros
    : grupo_parametro
    | lista_parametros PONTO_E_VIRGULA grupo_parametro
    ;

grupo_parametro
    : lista_ids DOIS_PONTOS tipo
    ;

comando_composto
    : BEGIN sequencia_comandos END
    ;

sequencia_comandos
    : comando
    | sequencia_comandos PONTO_E_VIRGULA comando
    ;

comando
    : atribuicao
    | chamada_procedimento
    | comando_composto
    | comando_se
    | comando_enquanto
    | comando_leia
    | comando_escreva
    ;

atribuicao
    : IDENTIFICADOR ATRIBUICAO expressao
    ;

chamada_procedimento
    : IDENTIFICADOR
    | IDENTIFICADOR ABRE_PARENTESE argumentos_opt FECHA_PARENTESE
    ;

argumentos_opt
    : /* vazio */
    | lista_argumentos
    ;

lista_argumentos
    : expressao
    | lista_argumentos VIRGULA expressao
    ;

comando_se
    : IF expressao THEN comando
    | IF expressao THEN comando ELSE comando
    ;

comando_enquanto
    : WHILE expressao DO comando
    ;

comando_leia
    : READ ABRE_PARENTESE lista_ids FECHA_PARENTESE
    ;

comando_escreva
    : WRITE ABRE_PARENTESE argumentos_opt FECHA_PARENTESE
    ;

expressao
    : expressao_simples
    | expressao_simples op_relacional expressao_simples
    ;

op_relacional
    : IGUAL | DIFERENTE
    | MENOR | MENOR_IGUAL
    | MAIOR | MAIOR_IGUAL
    ;

expressao_simples
    : termo
    | sinal termo
    | expressao_simples op_aditivo termo
    ;

sinal
    : MAIS | MENOS
    ;

op_aditivo
    : MAIS | MENOS | OR
    ;

termo
    : fator
    | termo op_multiplicativo fator
    ;

op_multiplicativo
    : MULTIPLICACAO | DIVISAO | DIV | MOD | AND
    ;

fator
    : IDENTIFICADOR
    | NUMERO_INTEIRO
    | NUMERO_REAL
    | CADEIA
    | TRUE
    | FALSE
    | NOT fator
    | ABRE_PARENTESE expressao FECHA_PARENTESE
    ;
```

## 3. Recuperação em modo pânico

Conjuntos de sincronização (definidos no `Parser`):

```python
STATEMENT_START   = {BEGIN, IF, WHILE, READ, WRITE, IDENTIFIER}
DECLARATION_START = {VAR, PROCEDURE, BEGIN}
TYPE_TOKENS       = {INTEGER, REAL, BOOLEAN}
REL_OPS           = {EQUAL, NOT_EQUAL, LESS, LESS_EQUAL, GREATER, GREATER_EQUAL}
ADD_OPS           = {PLUS, MINUS, OR}
MUL_OPS           = {STAR, SLASH, DIV, MOD, AND}
```

Procedimentos:

- `_synchronize_declaration()` — consome tokens até encontrar
  `DECLARATION_START ∪ {;}` e descarta o `;` quando presente.
- `_synchronize_statement()` — consome tokens até encontrar
  `STATEMENT_START ∪ {;, end, else}`.

Em todos os pontos onde uma produção falha, o erro é registrado com mensagem específica
(linha/coluna), e o parser sincroniza com base nesses conjuntos antes de tentar reconhecer
a próxima estrutura.

## 4. Mensagens de erro mais comuns

| Mensagem | Quando ocorre |
|----------|---------------|
| `Esperado 'programa'/'program' no início do programa.` | falta de cabeçalho |
| `Esperado identificador do programa.` | nome do programa ausente/inválido |
| `Esperado ';' após o cabeçalho do programa.` | `;` faltando depois do nome |
| `Esperado identificador na declaração de variável.` | `var` sem ID |
| `Esperado ':' antes do tipo da declaração.` | `:` faltando |
| `Esperado tipo: inteiro, real ou lógico.` | tipo inválido |
| `Esperado ';' após declaração.` | `;` faltando |
| `Esperado 'início'/'begin' para iniciar bloco de comandos.` | bloco mal aberto |
| `Esperado 'fim'/'end' para encerrar bloco de comandos.` | bloco mal fechado |
| `Esperado ';' entre comandos.` | `;` faltando entre comandos |
| `Esperado 'então'/'then' após condição do se/if.` | `then` faltando |
| `Esperado 'faça'/'do' após condição do enquanto/while.` | `do` faltando |
| `Esperado ')' após argumentos.` | parêntese não fechado |
| `Esperado '.' ao final do programa.` | falta o `.` final |
| `Identificador '<x>' não declarado.` | uso de nome desconhecido |
| `Identificador '<x>' já declarado neste escopo.` | redeclaração |
| `Identificador '<x>' usado como <esperado>, mas declarado como <real>.` | uso incoerente (ex.: chamar variável como procedimento) |
