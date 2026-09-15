from flask import Flask, request, render_template, jsonify
import subprocess
import os
import ast
import re
from database import init_db, search_products
from auth import SECRET_KEY, hash_password, hash_token, verify_token

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Инициализация базы данных
init_db()

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
    expr = request.args.get('expr', '1+1')
    # Безопасное вычисление константных выражений через ast.literal_eval
    result = ast.literal_eval(expr)
    return jsonify({'result': result})

if __name__ == '__main__':
    # Запуск приложения без режима отладки и привязка к localhost
    app.run(debug=False, host='127.0.0.1', port=5000)
