from lexer_folder.lexer import Lexer
from parser_folder.parser import Parser
from semantic_analyzer_folder.semantic_analyzer import SemanticAnalyzer
from interpreter_folder.interpreter import Interpreter

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

INVALID_TEST_CASE = """
buong_numero bilang = 1;
ipakita(bilang);
"""

def run_code(code):
    try:
        # 1. Lexical Analysis
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # 2. Syntax Analysis (Parser)
        parser = Parser(tokens)
        ast = parser.parse()

        # 3. Semantic Analysis (Type Checking)
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)

        # 4. Runtime Execution
        interpreter = Interpreter()
        interpreter.interpret(ast)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    print("=== TEST 1 ===")
    run_code(VALID_TEST_CASE)

    print("\n=== TEST 2 ===")
    run_code(INVALID_TEST_CASE)