import unittest

from lalg.lexer import Lexer
from lalg.tokens import TokenType


def token_types(source: str):
    tokens, diagnostics = Lexer(source).scan_tokens()
    assert diagnostics == []
    return [token.type for token in tokens]


class LexerTest(unittest.TestCase):
    def test_keywords_identifiers_numbers_and_operators(self):
        types = token_types("programa teste; var x: inteiro; inicio x := 10 + 2.5 fim.")
        self.assertEqual(types, [
            TokenType.PROGRAM,
            TokenType.IDENTIFIER,
            TokenType.SEMICOLON,
            TokenType.VAR,
            TokenType.IDENTIFIER,
            TokenType.COLON,
            TokenType.INTEGER,
            TokenType.SEMICOLON,
            TokenType.BEGIN,
            TokenType.IDENTIFIER,
            TokenType.ASSIGN,
            TokenType.INTEGER_LITERAL,
            TokenType.PLUS,
            TokenType.REAL_LITERAL,
            TokenType.END,
            TokenType.DOT,
            TokenType.EOF,
        ])


    def test_comments_are_ignored(self):
        types = token_types("programa p; { comentario } (* outro *) inicio fim.")
        self.assertIn(TokenType.BEGIN, types)
        self.assertIn(TokenType.END, types)


    def test_reports_invalid_character_and_bad_number(self):
        _, diagnostics = Lexer("9abc @").scan_tokens()
        self.assertEqual(len(diagnostics), 2)
        self.assertIn("Número malformado", diagnostics[0].message)
        self.assertIn("Caractere inesperado", diagnostics[1].message)

    def test_accepts_unicode_identifiers_bom_and_not_equal(self):
        tokens, diagnostics = Lexer("\ufeffprograma p; var ação: booleano; inicio ação := 1 != 2 fim.").scan_tokens()
        self.assertEqual(diagnostics, [])
        types = [token.type for token in tokens]
        self.assertIn(TokenType.BOOLEAN, types)
        self.assertIn(TokenType.NOT_EQUAL, types)
        self.assertTrue(any(token.lexeme == "ação" for token in tokens))


if __name__ == "__main__":
    unittest.main()
