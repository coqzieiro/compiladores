import unittest

from lalg_sintatico.lexer import Lexer
from lalg_sintatico.parser import Parser


def parse(source: str):
    tokens, lexical_errors = Lexer(source).scan_tokens()
    assert lexical_errors == []
    return Parser(tokens).parse()


class ParserTest(unittest.TestCase):
    def test_valid_complete_program(self):
        ast, diagnostics, symbols = parse(
            """
            programa exemplo;
            var
              total: inteiro;
              media: real;
              aprovado: booleano;

            procedimento calcula(a, b: inteiro; mostrar: booleano);
            var
              soma: inteiro;
            inicio
              soma := a + b;
              media := soma / 2.0;
              aprovado := media >= 6.0;
              se mostrar entao
                escreva("media", media)
              senao
                escreva("oculto")
            fim;

            inicio
              total := 10;
              calcula(total, 8, verdadeiro);
              enquanto aprovado faca
              inicio
                escreva("ok");
                aprovado := falso
              fim
            fim.
            """
        )
        self.assertEqual(diagnostics, [])
        self.assertIsNotNone(ast)
        self.assertIsNotNone(symbols.lookup("calcula"))
        self.assertIsNotNone(symbols.lookup("calcula.a"))
        self.assertIsNotNone(symbols.lookup("calcula.soma"))

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


if __name__ == "__main__":
    unittest.main()
