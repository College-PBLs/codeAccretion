from transpiler.cpp_to_java.transpiler import cpp_to_java
from transpiler.cpp_to_java.compiler import run_java

# Read CPP code
with open("testing/main.cpp", "r") as file:
    cpp_code = file.read()

# Transpile
result = cpp_to_java(cpp_code)

if result["success"]:
    print("✓ Transpilation successful!")
    print("\n--- Generated Java Code ---")
    print(result["generated_code"])
    
    # Compile and run
    compile_result = run_java(result["generated_code"])
    
    if compile_result["success"]:
        print("\n--- Program Output ---")
        print(compile_result["output"])
    else:
        print(f"\n✗ Compilation/Runtime Error: {compile_result.get('error')}")
else:
    print(f"✗ Transpilation failed at {result['stage']}:")
    for error in result["errors"]:
        print(f"  - {error}")

# from transpiler.java_to_cpp.transpiler import java_to_cpp
# from transpiler.java_to_cpp.compiler import run_cpp

# # Read Java code
# with open("testing/Main.java", "r") as file:
#     java_code = file.read()

# # Transpile
# result = java_to_cpp(java_code)

# if result["success"]:
#     print("✓ Transpilation succe/ssful!")
#     print("\n--- Generated CPP Code ---")
#     print(result["generated_code"])
    
#     # Compile and run
#     compile_result = run_cpp(result["generated_code"])
    
#     if compile_result["success"]:
#         print("\n--- Program Output ---")
#         print(compile_result["output"])
#     else:
#         print(f"\n✗ Compilation/Runtime Error: {compile_result.get('error')}")
# else:
#     print(f"✗ Transpilation failed at {result['stage']}:")
#     for error in result["errors"]:
#         print(f"  - {error}")