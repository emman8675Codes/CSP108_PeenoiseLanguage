from lexer.lexer import Lexer
from parser.parser import Parser
from project.semanticanalyzer.semantic_analyzer import SemanticAnalyzer

# Valid Code Test Case
VALID_TEST_CASE = """
buong_numero edad = 20;
lutang_numero marka = 88.5;
katotohanan pasado = totoo;
salita bati = "Maligayang Pagdating";

// Conditionals (kung / kundi_kung / kundi)
kung (edad >= 18 && pasado == totoo) {
    ipakita(bati);
} kundi_kung (edad == 17) {
    ipakita("Kulang ng isang taon.");
} kundi {
    ipakita("Bata pa.");
}

// Switch Statement (pihitan / kaso / likas)
pihitan (edad) {
    kaso 18:
        ipakita("Bagong adulto");
        hinto;
    kaso 20:
        ipakita("Saktong dalawampu");
        hinto;
    likas:
        ipakita("Ibang edad");
        hinto;
}
"""

# Invalid Code Test Case (Type Mismatch)
INVALID_TEST_CASE = """
buong_numero bilang = "Hindi Numero";
"""

def test_compiler(code: str, test_name: str):
    print(f"\n=================== {test_name} ===================")
    try:
        # Step 1: Lexical Analysis
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print("[1. LEXER]: Success! Tokens generated.")

        # Step 2: Parsing (AST Creation)
        parser = Parser(tokens)
        ast = parser.parse()
        print("[2. PARSER]: Success! Abstract Syntax Tree (AST) generated.")

        # Step 3: Semantic Analysis (Type Checking)
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print("[3. SEMANTIC ANALYZER]: Success! No type errors or scope issues found.")

    except Exception as error:
        print(f"[FAIL]: {error}")

if __name__ == "__main__":
    test_compiler(VALID_TEST_CASE, "TEST CASE 1: Valid Code")
    test_compiler(INVALID_TEST_CASE, "TEST CASE 2: Semantic Error Code")