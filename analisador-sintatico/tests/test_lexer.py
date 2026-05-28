import unittest

from lalg_sintatico.lexer import Lexer
from lalg_sintatico.tokens import TokenType


class LexerTest(unittest.TestCase):
    def test_unicode_bom_keywords_and_not_equal(self):
        tokens, diagnostics = Lexer("\ufeffprograma p; var ação: booleano; inicio ação := 1 != 2 fim.").scan_tokens()
        self.assertEqual(diagnostics, [])
        types = [token.type for token in tokens]
        self.assertIn(TokenType.PROGRAM, types)
        self.assertIn(TokenType.BOOLEAN, types)
        self.assertIn(TokenType.NOT_EQUAL, types)
        self.assertTrue(any(token.lexeme == "ação" for token in tokens))

    def test_reports_lexical_errors(self):
        _, diagnostics = Lexer("9abc @").scan_tokens()
        self.assertEqual(len(diagnostics), 2)
        self.assertIn("Número malformado", diagnostics[0].message)
        self.assertIn("Caractere inesperado", diagnostics[1].message)


if __name__ == "__main__":
    unittest.main()
