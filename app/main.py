from flask import Flask, request, render_template, jsonify
import subprocess
import os
import ast
import operator
import re
from database import init_db, search_products
from auth import SECRET_KEY, hash_password, hash_token, verify_token

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Инициализация базы данных
init_db()

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}

def safe_calc(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](safe_calc(node.left), safe_calc(node.right))
    raise ValueError

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '')
    products = search_products(q)
    return jsonify({'products': products})

@app.route('/api/ping')
def api_ping():
    host = request.args.get('host', '127.0.0.1')
    # Безопасный вызов subprocess с валидацией ввода и shell=False
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        return jsonify({'error': 'Invalid host'}), 400
    output = subprocess.check_output(['ping', '-c', '1', host], shell=False).decode('utf-8', errors='ignore')
    return jsonify({'output': output})

@app.route('/api/calc')
def api_calc():
    expr = request.args.get('expr', '1+1').replace(' ', '+')
    # Безопасное вычисление арифметических выражений через разбор AST-дерева
    try:
        result = safe_calc(ast.parse(expr, mode='eval').body)
        return jsonify({'result': result})
    except Exception:
        return jsonify({'error': 'Invalid expression'}), 400

if __name__ == '__main__':
    # Запуск приложения без режима отладки и привязка к localhost
    app.run(debug=False, host='127.0.0.1', port=5000)
