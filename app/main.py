from flask import Flask, request, render_template, jsonify
import subprocess
import os
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
    # Уязвимость 5: Внедрение команд операционной системы (Command Injection, CWE-77)
    cmd = f"ping -c 1 {host}"
    output = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
    return jsonify({'output': output})

@app.route('/api/calc')
def api_calc():
    expr = request.args.get('expr', '1+1')
    # Уязвимость 6: Выполнение произвольного кода через eval (CWE-94)
    result = eval(expr)
    return jsonify({'result': result})

if __name__ == '__main__':
    # Уязвимость 7: Запуск с включенным отладчиком и привязка к 0.0.0.0 (CWE-489)
    app.run(debug=True, host='0.0.0.0', port=5000)
