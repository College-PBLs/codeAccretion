export const PHASES = [
  {
    title: "Lexical Analysis",
    jsonArtifact: "tokens.json",
    desc: "Breaks input into tokens by scanning source code character by character.",
    input: "Source code string (Java/C++)",
    output: "List of tokens with type, value, and column position",
    details: [
      "Identifies keywords (class, public, int, if, while, etc.)",
      "Recognizes operators (+, -, *, /, =, ==, !=, &&, ||, etc.)",
      "Detects literals (integers, strings, characters, booleans)",
      "Handles identifiers (variable and function names)",
      "Skips whitespace and comments",
      "Reports lexical errors for invalid characters"
    ]
  },
  {
    title: "Syntax Analysis",
    jsonArtifact: "syntax_tree.json",
    desc: "Builds Abstract Syntax Tree (AST) from token stream based on grammar rules.",
    input: "Token stream from lexical analysis",
    output: "AST root object representing program structure",
    details: [
      "Validates grammatical structure of the code",
      "Builds hierarchical tree representation (Program → Statements → Expressions)",
      "Handles nested structures (if-else, loops, blocks)",
      "Manages function/method declarations and calls",
      "Tracks operator precedence and associativity",
      "Reports syntax errors (missing semicolons, unmatched braces, etc.)"
    ]
  },
  {
    title: "Semantic Analysis",
    jsonArtifact: "semantic.json",
    desc: "Validates symbol tables, type checking, and semantic rules.",
    input: "AST from syntax analysis",
    output: "Annotated AST with symbol table and type information",
    details: [
      "Builds symbol tables",
      "Performs type checking and type inference",
      "Validates variable declarations before use",
      "Checks function call signatures (parameters and return types)",
      "Ensures type compatibility in assignments and operations",
      "Detects semantic errors (type mismatches, undeclared variables, etc.)"
    ]
  },
  {
    title: "Intermediate Code Generation",
    jsonArtifact: "intermediate.json",
    desc: "Produces Three Address Code (3AC) or other IR representation.",
    input: "Annotated AST from semantic analysis",
    output: "Three Address Code (3AC) instructions",
    details: [
      "Converts AST to linear sequence of instructions",
      "Generates temporary variables for complex expressions",
      "Produces Three Address Code format: result = arg1 op arg2",
      "Handles control flow with labels and jumps",
      "Makes language features explicit (array indexing, object access)",
      "Prepares for target code generation"
    ]
  },
  {
    title: "Code Generation",
    jsonArtifact: "generated_code.json",
    desc: "Outputs final target code in Java or C++.",
    input: "Intermediate Code (3AC) or annotated AST",
    output: "Target language source code (Java/C++)",
    details: [
      "Maps IR to target language syntax (but in this uses syntax tree to build)",
      "Generates appropriate data type declarations",
      "Handles language-specific features (System.out.println vs cout)",
      "Generates boilerplate code (main function, includes)"
    ]
  }
];

export const SAMPLE = {
  java: `public class Main {\n    public static void main(String[] args) {\n      int sum = 0;\n      for (int i = 0; i < 3; i++) {\n        sum = sum + i;\n      }\n      System.out.println(sum);\n    }\n}`,
  cpp: `#include <iostream>\nusing namespace std;\nint main(){\n    int sum=0;\n    for(int i=0;i<3;i++){\n      sum = sum + i;\n    }\n    cout << sum << endl;\n}`,
};
