import unittest

from lalg.lexer import Lexer
from lalg.parser import Parser


def parse(source: str):
    tokens, lexical_errors = Lexer(source).scan_tokens()
    assert lexical_errors == []
    return Parser(tokens).parse()


class ParserTest(unittest.TestCase):
    def test_valid_program_parses_without_errors(self):
        ast, diagnostics, symbols = parse(
            """
            programa exemplo;
            var
              x, y: inteiro;
              ok: logico;
            inicio
              x := 1;
              y := x + 2;
              ok := y > 2;
              se ok entao escreva(y) senao escreva(0)
            fim.
            """
        )
        self.assertEqual(diagnostics, [])
        self.assertIsNotNone(ast)
        self.assertIsNotNone(symbols.lookup("x"))
        self.assertIsNotNone(symbols.lookup("ok"))

    def test_reports_missing_declaration(self):
        _, diagnostics, _ = parse(
            """
            programa exemplo;
            inicio
              x := 1
            fim.
            """
        )
        self.assertTrue(any("não declarado" in diagnostic.message for diagnostic in diagnostics))

    def test_reports_syntax_error(self):
        _, diagnostics, _ = parse(
            """
            programa exemplo
            inicio
            fim.
            """
        )
        self.assertTrue(any("Esperado ';'" in diagnostic.message for diagnostic in diagnostics))

    def test_procedure_with_parameters_local_variables_and_call(self):
        ast, diagnostics, symbols = parse(
            """
            programa exemplo;
            var
              total: inteiro;

            procedimento soma(a, b: inteiro; aprovado: booleano);
            var
              local: inteiro;
            inicio
              local := a + b;
              se aprovado entao
                escreva(local)
              senao
                escreva(0)
            fim;

            inicio
              total := 10;
              soma(total, 20, verdadeiro)
            fim.
            """
        )
        self.assertEqual(diagnostics, [])
        self.assertIsNotNone(ast)
        self.assertIsNotNone(symbols.lookup("soma"))
        self.assertIsNotNone(symbols.lookup("soma.a"))
        self.assertIsNotNone(symbols.lookup("soma.local"))


if __name__ == "__main__":
    unittest.main()
