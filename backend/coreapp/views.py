from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from transpiler.java_to_cpp.transpiler import java_to_cpp
from transpiler.cpp_to_java.transpiler import cpp_to_java
from transpiler.java_to_cpp.compiler import run_cpp
from transpiler.cpp_to_java.compiler import run_java


@api_view(['POST'])
def transpile_code(request):
    source_language = request.data.get("source_language")
    target_language = request.data.get("target_language")
    code = request.data.get("code")

    if not source_language or not target_language or not code:
        return Response(
            {"error": "Missing required fields"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        if source_language == "java" and target_language == "cpp":
            generated = java_to_cpp(code)
        elif source_language == "cpp" and target_language == "java":
            generated = cpp_to_java(code)
        else:
            return Response(
                {"error": "Unsupported Conversion"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"generated_code": generated},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def run_code(request):
    language = request.data.get("language")
    code = request.data.get("code")

    if not language or not code:
        return Response(
            {"error": "Missing required fields"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        if language == "cpp":
            output = run_cpp(code)
        elif language == "java":
            output = run_java(code)
        else:
            return Response(
                {"error": "Unsupported Language"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"output": output},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )