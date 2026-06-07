# Pasta `docs/` — Materiais de relatório

Esta pasta concentra todos os artefatos prontos para montar os relatórios dos dois trabalhos
da disciplina **SCC0217 — Linguagens de Programação e Compiladores** (Prof. Diego Raphael
Amancio), referentes à linguagem **LALG**.

Cada trabalho possui um relatório específico, escrito de acordo com o que é pedido no
respectivo PDF de especificação:

| Documento | Trabalho | Conteúdo |
|-----------|----------|----------|
| [relatorio-lexico.md](relatorio-lexico.md) | Trabalho 1 — Analisador léxico | Decisões de projeto, especificação dos tokens, tabela de palavras reservadas, tratamento de erros, passo a passo de execução e exemplos. |
| [relatorio-sintatico.md](relatorio-sintatico.md) | Trabalho 2 — Analisador sintático | Decisões de projeto, gramática, modo pânico para recuperação de erros, integração com o léxico, passo a passo de execução e exemplos. |
| [especificacao-lexica.md](especificacao-lexica.md) | Trabalho 1 | Listagem da especificação léxica (no estilo lex/flex), expressões regulares utilizadas, mapa lexema→token. |
| [especificacao-sintatica.md](especificacao-sintatica.md) | Trabalho 2 | Listagem da gramática (no estilo YACC/JavaCC) com todas as produções implementadas. |

## Estrutura

```text
docs/
  README.md                       # este índice
  relatorio-lexico.md             # Relatório do Trabalho 1
  relatorio-sintatico.md          # Relatório do Trabalho 2
  especificacao-lexica.md         # ER/listagem do léxico
  especificacao-sintatica.md      # Gramática/listagem do sintático
  exemplos-fonte/                 # Cópias dos arquivos .lalg de exemplo
    lexico-valido.lalg
    lexico-invalido.lalg
    sintatico-valido.lalg
    sintatico-invalido.lalg
  saidas/                         # Saídas reais coletadas dos analisadores
    lexico-valido.txt
    lexico-valido-tokens.txt
    lexico-valido.json
    lexico-valido-pdf.txt         # estilo "lexema - rótulo" do PDF
    lexico-invalido.txt
    lexico-invalido.json
    lexico-invalido-pdf.txt
    sintatico-valido.txt
    sintatico-valido-tokens.txt
    sintatico-valido.json
    sintatico-valido-pdf.txt
    sintatico-invalido.txt
    sintatico-invalido.json
    sintatico-invalido-pdf.txt
    testes-lexico.txt             # saída do unittest do módulo léxico
    testes-sintatico.txt          # saída do unittest do módulo sintático
```

## Como reproduzir as saídas

A partir da raiz do repositório, com Python ≥ 3.10 instalado:

```bash
# Analisador léxico
cd analisador-lexico
PYTHONPATH=src python3 -m lalg.cli examples/valido.lalg
PYTHONPATH=src python3 -m lalg.cli examples/invalido.lalg
PYTHONPATH=src python3 -m lalg.cli examples/valido.lalg --tokens
PYTHONPATH=src python3 -m lalg.cli examples/valido.lalg --json

# Analisador sintático
cd ../analisador-sintatico
PYTHONPATH=src python3 -m lalg_sintatico.cli examples/valido.lalg
PYTHONPATH=src python3 -m lalg_sintatico.cli examples/invalido.lalg
PYTHONPATH=src python3 -m lalg_sintatico.cli examples/valido.lalg --json
```

Os arquivos em [saidas/](saidas/) foram gerados exatamente com esses comandos.

## Como reproduzir os testes

```bash
# Léxico
cd analisador-lexico
PYTHONPATH=src python3 -m unittest discover -s tests -v

# Sintático
cd ../analisador-sintatico
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Resumo das execuções armazenadas:

- [saidas/testes-lexico.txt](saidas/testes-lexico.txt) — 8 testes, `OK`.
- [saidas/testes-sintatico.txt](saidas/testes-sintatico.txt) — 5 testes, `OK`.
