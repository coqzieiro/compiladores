# Especificação léxica — LALG

Listagem da especificação léxica no estilo lex/flex. A implementação real, em Python, está
em [`analisador-lexico/src/lalg/lexer.py`](../analisador-lexico/src/lalg/lexer.py); este
documento é a versão "papel" pedida pelo enunciado do Trabalho 1.

## 1. Definições regulares

```text
letra            ::= [A-Za-z_]   (com Unicode NFC: aceita á é í ó ú ç …)
digito           ::= [0-9]
identificador    ::= letra (letra | digito)*
inteiro          ::= digito+
real             ::= digito+ '.' digito+
cadeia_aspas2    ::= '"' ([^"\n\\] | \\.)* '"'
cadeia_aspas1    ::= "'" ([^'\n\\] | \\.)* "'"
ws               ::= [ \t\r\n\ufeff]+        (BOM UTF-8 tratado como ws)
comentario_chav  ::= '{' ... '}'
comentario_pasc  ::= '(*' ... '*)'
comentario_lin   ::= '//' [^\n]*
```

## 2. Regras lex (estilo flex)

```lex
%{
#include "tokens.h"
%}

LETRA       [A-Za-z_]
DIGITO      [0-9]
ID          {LETRA}({LETRA}|{DIGITO})*
INTEIRO     {DIGITO}+
REAL        {DIGITO}+\.{DIGITO}+

%%

[ \t\r\n\xEF\xBB\xBF]+     { /* whitespace e BOM UTF-8 — descartar */ }

"//"[^\n]*                 { /* comentário de linha — descartar */ }
"{"[^}]*"}"                { /* comentário { ... } */ }
"(*"([^*]|\*+[^*)])*"*)"   { /* comentário (* ... *) */ }

"program"|"programa"       { return PROGRAM; }
"var"                      { return VAR; }
"integer"|"inteiro"        { return INTEGER; }
"real"                     { return REAL; }
"boolean"|"booleano"|"logico"|"bool" { return BOOLEAN; }
"procedure"|"procedimento" { return PROCEDURE; }
"begin"|"inicio"           { return BEGIN; }
"end"|"fim"                { return END; }
"if"|"se"                  { return IF; }
"then"|"entao"             { return THEN; }
"else"|"senao"             { return ELSE; }
"while"|"enquanto"         { return WHILE; }
"do"|"faca"                { return DO; }
"read"|"readln"|"leia"|"ler" { return READ; }
"write"|"writeln"|"escreva"|"escrever" { return WRITE; }
"true"|"verdadeiro"        { return TRUE; }
"false"|"falso"            { return FALSE; }
"and"|"e"                  { return AND; }
"or"|"ou"                  { return OR; }
"not"|"nao"                { return NOT; }
"div"                      { return DIV; }
"mod"|"modulo"             { return MOD; }

":="                       { return ATRIBUICAO; }
"<="                       { return MENOR_IGUAL; }
">="                       { return MAIOR_IGUAL; }
"<>"|"!="                  { return DIFERENTE; }
"="                        { return IGUAL; }
"<"                        { return MENOR; }
">"                        { return MAIOR; }
"+"                        { return MAIS; }
"-"                        { return MENOS; }
"*"                        { return MULTIPLICACAO; }
"/"                        { return DIVISAO; }
"("                        { return ABRE_PARENTESE; }
")"                        { return FECHA_PARENTESE; }
","                        { return VIRGULA; }
";"                        { return PONTO_E_VIRGULA; }
":"                        { return DOIS_PONTOS; }
"."                        { return PONTO; }

{ID}                       { return IDENTIFICADOR; }
{REAL}                     { return NUMERO_REAL; }
{INTEIRO}                  { return NUMERO_INTEIRO; }
\"([^"\n\\]|\\.)*\"        { return CADEIA; }
\'([^'\n\\]|\\.)*\'        { return CADEIA; }

{DIGITO}+\.[A-Za-z_].*     { erro("numero real mal formado"); }
{DIGITO}+{LETRA}+          { erro("identificador nao pode iniciar por digito"); }

.                          { erro("simbolo nao pertencente a linguagem"); }

%%
```

## 3. Mapa lexema → rótulo (estilo do PDF)

| Lexema(s) | Token canônico | Rótulo no PDF |
|-----------|---------------|---------------|
| `program`, `programa` | `PROGRAM` | `program` |
| `var` | `VAR` | `var` |
| `integer`, `inteiro` | `INTEGER` | `integer` |
| `real` | `REAL` | `real` |
| `boolean`, `booleano`, `logico`, `bool` | `BOOLEAN` | `boolean` |
| `procedure`, `procedimento` | `PROCEDURE` | `procedure` |
| `begin`, `inicio` | `BEGIN` | `begin` |
| `end`, `fim` | `END` | `end` |
| `if`, `se` | `IF` | `if` |
| `then`, `entao` | `THEN` | `then` |
| `else`, `senao` | `ELSE` | `else` |
| `while`, `enquanto` | `WHILE` | `while` |
| `do`, `faca` | `DO` | `do` |
| `read`, `readln`, `leia`, `ler` | `READ` | `read` |
| `write`, `writeln`, `escreva`, `escrever` | `WRITE` | `write` |
| `true`, `verdadeiro` | `TRUE` | `true` |
| `false`, `falso` | `FALSE` | `false` |
| `and`, `e` | `AND` | `and` |
| `or`, `ou` | `OR` | `or` |
| `not`, `nao` | `NOT` | `not` |
| `div` | `DIV` | `div` |
| `mod`, `modulo` | `MOD` | `mod` |
| `+` | `MAIS` | `simb_mais` |
| `-` | `MENOS` | `simb_menos` |
| `*` | `MULTIPLICACAO` | `simb_multiplicacao` |
| `/` | `DIVISAO` | `simb_divisao` |
| `:=` | `ATRIBUICAO` | `simb_atribuicao` |
| `=` | `IGUAL` | `simb_igual` |
| `<>` / `!=` | `DIFERENTE` | `simb_diferente` |
| `<` | `MENOR` | `simb_menor` |
| `<=` | `MENOR_IGUAL` | `simb_menor_igual` |
| `>` | `MAIOR` | `simb_maior` |
| `>=` | `MAIOR_IGUAL` | `simb_maior_igual` |
| `(` | `ABRE_PARENTESE` | `simb_abre_parentese` |
| `)` | `FECHA_PARENTESE` | `simb_fecha_parentese` |
| `,` | `VIRGULA` | `simb_virgula` |
| `;` | `PONTO_E_VIRGULA` | `simb_ponto_virgula` |
| `:` | `DOIS_PONTOS` | `simb_dois_pontos` |
| `.` | `PONTO` | `simb_ponto` |
| identificador | `IDENTIFICADOR` | `id` |
| literal inteiro | `NUMERO_INTEIRO` | `num_int` |
| literal real | `NUMERO_REAL` | `num_real` |
| literal de cadeia | `CADEIA` | `cadeia` |

## 4. Erros léxicos reconhecidos

| Situação | Mensagem |
|----------|----------|
| Caractere fora do alfabeto | `Caractere inesperado '<c>'.` |
| Sequência dígito+letra | `Número malformado '<lex>'. Identificadores não podem iniciar por dígito.` |
| Cadeia que atravessa linha | `Cadeia de caracteres não pode atravessar linha.` |
| Cadeia sem aspas finais até EOF | `Cadeia de caracteres não finalizada.` |
| Comentário de bloco sem fechamento | `Comentário de bloco não finalizado.` |

Cada erro produz um `Diagnostic(message, line, column, offset, kind="erro léxico")` —
ver [errors.py](../analisador-lexico/src/lalg/errors.py).
