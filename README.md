## CodeAccretion

> **A Bidirectional Compiler Visualization Platform for Java ↔ C++ Transpilation**

CodeAccretion is an educational compiler visualization platform and bidirectional transpiler that converts **Java ↔ C++** while exposing every internal compilation phase in real time.

Unlike traditional transpilers that only generate target code, CodeAccretion helps students and developers understand **how compilers work internally** — from tokenization and parsing to semantic analysis, intermediate code generation, and final target code emission.

---

## Project Goals

- Transpile code between Java and C++.
- Visualize each compilation phase in the UI.
- Let users run both source and generated code.
- Help learners understand how compiler internals transform source code.

---

## Tech Stack

### Backend
- Django 5 + Django REST Framework
- Custom transpiler pipelines:
  - `backend/transpiler/java_to_cpp/*`
  - `backend/transpiler/cpp_to_java/*`

### Frontend
- React + Vite
- Monaco editor for source/target editing
- Tailwind CSS
- Phase viewers for tokens, AST, semantic output, and intermediate code

---

## Repository Structure

```text
codeAccretion/
  backend/
    codeAccretion/          # Django config
    coreapp/                # API endpoints
    transpiler/
      java_to_cpp/          # Java -> C++ pipeline
      cpp_to_java/          # C++ -> Java pipeline
      output/               # JSON/target output artifacts
      config.py             # OUTPUT_DIR + TEMP_DIR
  frontend/
    src/
      pages/                # Home + Transpile screens
      components/           # Editors/viewers/UI pieces
      services/api.js       # API client
```

---

## Why This Project Matters

Most transpilers only focus on converting code from one language to another.

CodeAccretion goes much further.

It is designed as both:

- A practical transpilation engine
- An educational compiler-learning platform

The platform helps students visualize how modern compilers internally transform source code step-by-step.

---

## Features

### Compiler Phase Visualization
- Lexical Analysis
- Syntax Analysis (AST)
- Semantic Analysis
- Intermediate Code Generation
- Final Target Code Generation

### Interactive Editors
- Monaco-powered source editor
- Syntax highlighting
- Auto-formatting
- Read-only generated code editor

### Compiler Internals Exposure
- Token stream inspection
- AST visualization
- Symbol table visualization
- Semantic error tracking
- Three Address Code generation

## Code Execution Support
- Run original source code
- Run generated target code
- Java execution support
- C++ compilation and execution

---

## Architecture Diagram

```text
                           ┌───────────────────────┐
                           │      React Frontend   │
                           │   (Vite + Monaco)     │
                           └──────────┬────────────┘
                                      │
                                      ▼
                           ┌───────────────────────┐
                           │    Django Backend     │
                           │   Django REST API     │
                           └──────────┬────────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
             ▼                        ▼                        ▼
   ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
   │ Java → C++     │      │ Shared Output  │      │ C++ → Java     │
   │ Compiler Pipe  │      │ JSON Artifacts │      │ Compiler Pipe  │
   └────────────────┘      └────────────────┘      └────────────────┘
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │ Compiler Phases Engine │
                         ├────────────────────────┤
                         │ 1. Lexical Analysis    │
                         │ 2. Syntax Analysis     │
                         │ 3. Semantic Analysis   │
                         │ 4. Intermediate Code   │
                         │ 5. Code Generation     │
                         └────────────────────────┘
```

---

## Compiler Pipeline Visualization

```text
                Source Code (Java / C++)
                           │
                           ▼
                ┌──────────────────┐
                │ Lexical Analyzer │
                └──────────────────┘
                           │
                           ▼
                     Token Stream
                           │
                           ▼
                ┌──────────────────┐
                │ Syntax Analyzer  │
                └──────────────────┘
                           │
                           ▼
                    Abstract Syntax Tree
                           │
                           ▼
                ┌──────────────────┐
                │ Semantic Analyzer│
                └──────────────────┘
                           │
                           ▼
                    Validated AST
                           │
                           ▼
                ┌──────────────────┐
                │ Intermediate IR  │
                │ Three Address    │
                │ Code Generator   │
                └──────────────────┘
                           │
                           ▼
                ┌──────────────────┐
                │ Code Generator   │
                └──────────────────┘
                           │
                           ▼
                  Target Language Code
```

---

## Compiler Phases and Stored JSON Artifacts

Output folder: `backend/transpiler/output`

### 1) Lexical Analysis
- File: `tokens.json`
- Created by: `lexical_analyzer(...)`
- Stores: token list with:
  - `type`
  - `value`
  - `position`

### 2) Syntax Analysis
- File: `syntax_tree.json`
- Created by: `syntax_analyzer(tokens)`
- Stores: AST root object (`Program`) including `body`, `functions`, and optional `class_name`.

### 3) Semantic Analysis
- File: `semantic.json`
- Created by: `semantic_analyzer(tree)`
- Stores:
  - `status` (`Passed`/`Failed`)
  - `symbol_table`
  - `functions`
  - `errors`

### 4) Intermediate Code Generation
- File: `intermediate.json`
- Created by: `intermediate_code_generator(tree)`
- Stores:
  - `three_address_code`: list of TAC lines

### 5) Target Code Generation
- Files:
  - `generated_code.cpp` (Java -> C++)
  - `generated_code.java` (C++ -> Java)
  - `generated_code.json`
- `generated_code.json` stores:
  - `generated_code` (final target code string)

---

## API Endpoints

Base route (current backend config): root path.

### 1) `POST /transpile/`
Transpile source code and return phase outputs plus generated code.

Request body:

```json
{
  "source_language": "java",
  "target_language": "cpp",
  "code": "public class Main { ... }"
}
```

Supported conversions:
- `java` -> `cpp`
- `cpp` -> `java`

Success response (`200`):

```json
{
  "generated_code": {
    "success": true,
    "tokens": [],
    "syntax_tree": {},
    "semantic_result": {},
    "intermediate_code": {
      "three_address_code": []
    },
    "generated_code": "..."
  }
}
```

Failure response (`400`/`500`) examples:

```json
{ "error": "Missing required fields" }
```

```json
{ "generated_code": { "success": false, "stage": "semantic_analysis", "errors": ["..."] } }
```

### 2) `POST /run/`
Compile + execute code for selected language.

Request body:

```json
{
  "language": "cpp",
  "code": "#include <bits/stdc++.h> ..."
}
```

Success response (`200`):

```json
{
  "output": {
    "success": true,
    "output": "program stdout"
  }
}
```

Failure response (`200` from runner payload, or `400/500` from API-level validation):

```json
{
  "output": {
    "success": false,
    "stage": "compilation",
    "error": "..."
  }
}
```

Runner notes:
- C++ uses `g++` then executes binary (`timeout=5s`).
- Java uses `javac` + `java -cp temp <ClassName>` (`timeout=5s`).

## Language Support Matrix (Backend Transpilers)

The following constructs are implemented in parser/semantic/intermediate/codegen logic for both directions.

### Commonly Supported Constructs
- Variable declarations
- Multi-variable declarations (`int a=1, b=2;`)
- Assignments
- Arithmetic operators: `+ - * / %`
- Relational operators: `< > <= >=`
- Equality operators: `== !=`
- Logical operators: `&& || !`
- Unary operators: prefix/postfix `++ --`, unary `+ - !`
- Ternary operator: `condition ? a : b`
- Shorthand/compound assignments:
  - Java parser desugars `+= -= *= /= %=` to assignment expressions
  - C++ parser keeps explicit `CompoundAssignment`, Java generator emits `+=` etc.
- `if`, `if-else`, `else if`
- Loops:
  - `for`
  - `while`
  - `do-while`
- `switch-case-default`
- `break`, `continue`
- `return`
- Function/method declarations and calls
- Block statements `{ ... }`

### Java -> C++ Specific Handling
- `System.out.print` / `System.out.println` -> `cout << ...` (with optional `<< endl`)
- Java type mapping includes:
  - `boolean -> bool`
  - `String -> string`
  - `byte -> char`

### C++ -> Java Specific Handling
- Preprocessor lines (`#include`, etc.) are removed before tokenization.
- `cout << ... << endl;` parsed as print chain and emitted to `System.out.print/println(...)`.
- Scoped call conversion in generator:
  - `TestAll::add(...)` -> `TestAll.add(...)`
- Type mapping includes:
  - `bool -> boolean`
  - `string -> String`
  - `char* -> String`
  - some pointer forms to arrays (e.g., `int* -> int[]`)

## Frontend: Complete Structured Details

### Routing
- `/` -> Home page
- `/java-to-cpp` -> Java to C++ transpilation page
- `/cpp-to-java` -> C++ to Java transpilation page

Main route config:
- `frontend/src/App.jsx`

### Layout Layer
- `MainLayout.jsx`
  - Navbar
  - page container (`<main>`)
  - Footer
  - global toast
- Theme mode persists in `localStorage` (`dark`/`light`).

### Page: Home (`HomePage.jsx`)
- Hero section introducing compiler visualization.
- Feature cards.
- Compiler phase cards rendered from `PHASES` constant.

### Page: Transpile (`TranspilePage.jsx`)
Core workspace includes:
- Source editor (Monaco)
- Target output editor (read-only)
- Run source button
- Run target button
- Transpile button
- Tabs for phase outputs:
  - Tokens
  - Syntax Tree
  - Semantic
  - Intermediate

Behavior:
- Loads sample code per language.
- Clears and resets state when switching route/language.
- Uses `/transpile/` for compile phases + generated code.
- Uses `/run/` to execute source or generated code.

### Core UI Components
- `CodeEditor.jsx`
  - Monaco integration
  - paste formatting + `Ctrl/Cmd+S` formatting
- `OutputConsole.jsx`
  - Displays run response output
- `TokenTable.jsx`
  - token type/value/position table
- `SyntaxTreeViewer.jsx`
  - recursive AST visualization
- `SemanticViewer.jsx`
  - status panel + tabs:
    - symbol table
    - function definitions
    - semantic errors
- `IntermediateViewer.jsx`
  - 3-address-code viewer with line numbers
- `Navbar.jsx`
  - navigation links + theme toggle

### Frontend API Client
- File: `frontend/src/services/api.js`
- Axios base URL from `VITE_API_BASE_URL`
- Methods:
  - `transpileCode(payload)` -> `POST /transpile/`
  - `runCode(payload)` -> `POST /run/`

## Setup and Run

### Backend
From `backend/`:

```bash
python -m venv venv
venv/Scripts/activate or source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Required env vars used by settings:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `OUTPUT_FOLDER`
- `TEMP_FOLDER`

### Frontend
From `frontend/`:

```bash
npm install
npm audit fix or npm audit fix --force
npm run dev
```

Required env vars used by api client:
- `VITE_API_BASE_URL` (example: `http://127.0.0.1:8000`)

---

## Runtime Artifacts

### Persistent phase artifacts
- `backend/transpiler/output/tokens.json`
- `backend/transpiler/output/syntax_tree.json`
- `backend/transpiler/output/semantic.json`
- `backend/transpiler/output/intermediate.json`
- `backend/transpiler/output/generated_code.json`
- `backend/transpiler/output/generated_code.cpp`
- `backend/transpiler/output/generated_code.java`

### Temporary execution artifacts
- `backend/temp/main.cpp`
- `backend/temp/main.exe` (Windows)
- `backend/temp/<ClassName>.java`
- corresponding Java `.class` files

---

## Summary

CodeAccretion is a learning-focused transpiler platform that combines:
- Practical bidirectional Java/C++ transpilation
- Phase-by-phase compiler introspection
- Executable validation of both source and generated code

This makes it useful both as an educational compiler visualization tool and as a hands-on transpilation playground.
