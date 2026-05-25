import json
from .lexical import lexical_analyzer
from .parser import syntax_analyzer
from .semantic import semantic_analyzer
from .intermediate import intermediate_code_generator
from .codegen import JavaGenerator
from ..config import OUTPUT_DIR

def cpp_to_java(code):
    # 1. Lexical Analysis
    try:
        tokens = lexical_analyzer(code)
    except Exception as e:
        return {
            "success": False,
            "stage": "lexical_analysis",
            "errors": [str(e)]
        }

    
    # 2. Syntax Analysis
    try:
        syntax_tree = syntax_analyzer(tokens)
    except Exception as e:
        return {
            "success": False,
            "stage": "syntax_analysis",
            "errors": [str(e)]
        }

    
    # 3. Semantic Analysis
    semantic_result = semantic_analyzer(syntax_tree)
    # Stop if semantic errors exist
    if semantic_result["status"] == "Failed":
        return {
            "success": False,
            "stage": "semantic_analysis",
            "errors": semantic_result["errors"]
        }

    
    # 4. Intermediate Code Generation
    intermediate_code = intermediate_code_generator(syntax_tree)


    # 5. Target Code Generation
    # Generate Java code from syntax tree
    generator = JavaGenerator()
    generated_code = generator.generate(syntax_tree)


    # SAVE GENERATED CODE
    with open(f"{OUTPUT_DIR}/generated_code.java", "w") as file:
        file.write(generated_code)
    with open(f"{OUTPUT_DIR}/generated_code.json", "w") as file:
        json.dump({"generated_code": generated_code}, file, indent=4)

    
    # FINAL RESPONSE
    return {
        "success": True,
        "tokens": tokens,
        "syntax_tree": syntax_tree,
        "semantic_result": semantic_result,
        "intermediate_code": intermediate_code,
        "generated_code": generated_code
    }