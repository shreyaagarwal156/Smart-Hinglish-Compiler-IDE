from flask import Flask, render_template, request, jsonify
import traceback
import subprocess
import sys

from compiler.lexer import HinglishLexer
from compiler.parser import HinglishParser
from compiler.semantic import SemanticAnalyzer
from compiler.optimizer import ASTOptimizer
from compiler.codegen.generator_python import PythonGenerator
from compiler.codegen.generator_cpp import CPPGenerator
from compiler.codegen.generator_c import CGenerator
from compiler.codegen.generator_java import JavaGenerator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    try:
        data = request.json
        source_code = data.get('code', '')
        std_input = data.get('stdin', '') # NAYA: Getting STDIN from frontend
        run_optimizer = data.get('optimize', True)

        if not source_code.strip():
            return jsonify({'status': 'error', 'console': 'Bhai, code toh likh de pehle!'})

        lexer = HinglishLexer()
        parser = HinglishParser()
        semantic = SemanticAnalyzer()
        optimizer = ASTOptimizer()

        tokens = lexer.tokenize(source_code)
        ast = parser.parse(tokens)

        if parser.errors:
            return jsonify({'status': 'error', 'console': "\n".join(parser.errors)})
        if ast is None:
            return jsonify({'status': 'error', 'console': 'Code parse nahi ho paya.'})

        semantic.analyze(ast)
        if semantic.errors:
            return jsonify({'status': 'error', 'console': "\n".join(semantic.errors)})

        if run_optimizer:
            ast = optimizer.optimize(ast)

        py_gen = PythonGenerator()
        cpp_gen = CPPGenerator()
        java_gen = JavaGenerator()
        c_gen = CGenerator()

        compiled_codes = {
            'python': py_gen.generate(ast),
            'cpp': cpp_gen.generate(ast),
            'java': java_gen.generate(ast),
            'c': c_gen.generate(ast)
        }

        # Step 5: Execute Python with STDIN!
        execution_output = ""
        try:
            # subprocess.run mein input=std_input pass kiya hai HackerRank style mein
            process = subprocess.run(
                [sys.executable, '-c', compiled_codes['python']],
                input=std_input,
                capture_output=True,
                text=True,
                timeout=5
            )
            execution_output = process.stdout
            if process.stderr:
                execution_output += "\n[Runtime Error]\n" + process.stderr
        except subprocess.TimeoutExpired:
            execution_output = "[Error] Execution Timeout: Infinite loop ya Input ka wait karte hue timeout ho gaya!"
        except Exception as exec_err:
            execution_output = f"[Error] Engine failed to run code: {str(exec_err)}"

        return jsonify({
            'status': 'success',
            'compiled_codes': compiled_codes,
            'execution_output': execution_output,
            'console': "Success! Smart Multi-Target Compilation Complete."
        })

    except Exception as e:
        error_trace = traceback.format_exc()
        return jsonify({'status': 'error', 'console': f"SYSTEM CRASH:\n{str(e)}\n\nTraceback:\n{error_trace}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)