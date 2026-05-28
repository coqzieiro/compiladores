# Compiladores - Analisadores para LALG

Este repositório reúne implementações em Python de analisadores para uma linguagem **LALG/Pascal-like**, desenvolvidas como projeto de Compiladores.

O objetivo é demonstrar as etapas iniciais de um compilador: leitura do código-fonte, reconhecimento de tokens, validação da estrutura gramatical, construção de uma AST simples e registro de símbolos declarados no programa.

## Módulos do projeto

O repositório está organizado em duas pastas principais:

```text
analisador-lexico/
	Implementação do analisador léxico e sintático no pacote lalg.

analisador-sintatico/
	Implementação do analisador sintático descendente recursivo no pacote lalg_sintatico.
```

Cada módulo possui seus próprios exemplos, testes, configuração de pacote Python e README com detalhes específicos.

## Linguagem suportada

A linguagem analisada segue uma sintaxe inspirada em Pascal/LALG, com suporte a:

- declaração de programa;
- declaração de variáveis;
- tipos básicos `inteiro`, `real` e `booleano`;
- comandos compostos com `inicio` e `fim`;
- atribuições;
- chamadas de procedimento;
- estruturas condicionais `se`/`senao`;
- laços `enquanto`;
- comandos de entrada e saída;
- expressões aritméticas, relacionais e lógicas;
- comentários e cadeias de caracteres.

Também são aceitas algumas palavras reservadas equivalentes em inglês, como `program`, `begin`, `end`, `if`, `then`, `else`, `while`, `do`, `read` e `write`.

## Funcionalidades implementadas

- Análise léxica com identificação de tokens.
- Tratamento de identificadores, números inteiros, números reais e strings.
- Reconhecimento de operadores, delimitadores e palavras reservadas.
- Suporte a comentários `{ ... }`, `(* ... *)` e `// ...`.
- Relatório de erros com linha e coluna.
- Análise sintática descendente recursiva.
- Geração de AST serializável em JSON.
- Tabela de símbolos com escopos simples.
- Validações básicas de declaração e uso de identificadores.
- Testes automatizados para léxico e sintático.

## Estrutura geral

```text
compiladores/
	README.md
	pyrightconfig.json

	analisador-lexico/
		README.md
		pyproject.toml
		examples/
			valido.lalg
			invalido.lalg
		src/lalg/
			lexer.py
			parser.py
			ast.py
			symbols.py
			tokens.py
			errors.py
			cli.py
		tests/
			test_lexer.py
			test_parser.py

	analisador-sintatico/
		README.md
		pyproject.toml
		examples/
			valido.lalg
			invalido.lalg
		src/lalg_sintatico/
			lexer.py
			parser.py
			ast.py
			symbols.py
			tokens.py
			errors.py
			cli.py
		tests/
			test_lexer.py
			test_parser.py
```

## Requisitos

- Python 3.10 ou superior.
- Não há dependências obrigatórias externas para executar os analisadores.
- `pytest` é opcional; os testes também podem ser executados com `unittest`.

## Como executar o analisador léxico

Entre na pasta do analisador léxico:

```bash
cd analisador-lexico
```

Execute um exemplo válido:

```bash
PYTHONPATH=src python -m lalg.cli examples/valido.lalg
```

Para exibir apenas os tokens:

```bash
PYTHONPATH=src python -m lalg.cli examples/valido.lalg --tokens
```

Para gerar saída em JSON:

```bash
PYTHONPATH=src python -m lalg.cli examples/valido.lalg --json
```

## Como executar o analisador sintático

Entre na pasta do analisador sintático:

```bash
cd analisador-sintatico
```

Execute um exemplo válido:

```bash
PYTHONPATH=src python -m lalg_sintatico.cli examples/valido.lalg
```

Para exibir apenas os tokens:

```bash
PYTHONPATH=src python -m lalg_sintatico.cli examples/valido.lalg --tokens
```

Para gerar saída em JSON:

```bash
PYTHONPATH=src python -m lalg_sintatico.cli examples/valido.lalg --json
```

## Executando os testes

Em cada pasta de módulo, os testes podem ser executados com `unittest`:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Se `pytest` estiver instalado, também é possível usar:

```bash
PYTHONPATH=src pytest
```

## Exemplos

Cada módulo contém dois arquivos de exemplo:

- `examples/valido.lalg`: programa aceito pela gramática implementada.
- `examples/invalido.lalg`: programa com erros para testar os diagnósticos.

## Objetivo acadêmico

Este projeto tem finalidade didática e serve para estudar, implementar e testar conceitos fundamentais de compiladores, como:

- especificação de tokens;
- análise léxica;
- gramáticas livres de contexto;
- parsing descendente recursivo;
- árvore sintática abstrata;
- tabela de símbolos;
- detecção e relatório de erros.
