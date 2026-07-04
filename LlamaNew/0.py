import os
import sqlite3
import re
import unittest
from flask import Flask, request, render_template_string


app = Flask(__name__)
DATABASE = 'calculator_history.db'


HTML_TEMPLATE = 

def init_db():
    
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute()
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")

def validate_input(expression):
    
    if not expression or len(expression) > 100:
        return False
    
    
    return bool(re.match(r'^[0-9+\-*/().\s]+$', expression))

def secure_eval(expression):
    
    try:
        
        safe_dict = {"__builtins__": None}
        result = eval(expression, safe_dict, {})
        
        if isinstance(result, (int, float)):
            return round(result, 4)
        return None
    except Exception:
        return None

@app.route('/', methods=['GET'])
def index():
    
    history = []
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.execute("SELECT expression, result FROM history ORDER BY id DESC LIMIT 5")
            history = cursor.fetchall()
    except sqlite3.Error:
        pass
    return render_template_string(HTML_TEMPLATE, history=history, result=None, error=None)

@app.route('/calculate', methods=['POST'])
def calculate():
    
    expression = request.form.get('expression', '').strip()
    history = []
    
    
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.execute("SELECT expression, result FROM history ORDER BY id DESC LIMIT 5")
            history = cursor.fetchall()
    except sqlite3.Error:
        pass

    
    if not validate_input(expression):
        return render_template_string(HTML_TEMPLATE, history=history, result=None, error="Invalid input. Use only numbers and +, -, *, /, ().")

    
    result = secure_eval(expression)
    if result is None:
        return render_template_string(HTML_TEMPLATE, history=history, result=None, error="Math error or invalid expression.")

    
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (expression, str(result)))
            conn.commit()
            
            cursor = conn.execute("SELECT expression, result FROM history ORDER BY id DESC LIMIT 5")
            history = cursor.fetchall()
    except sqlite3.Error:
        return render_template_string(HTML_TEMPLATE, history=history, result=None, error="Database storage failed.")

    return render_template_string(HTML_TEMPLATE, history=history, result=result, error=None)


class TestSecureCalculator(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_input_validation(self):
        self.assertTrue(validate_input("1 + 1"))
        self.assertTrue(validate_input(" (2.5 * 3) / 4 "))
        self.assertFalse(validate_input("import os"))
        self.assertFalse(validate_input("print('hello')"))
        self.assertFalse(validate_input("1 + 1; DROP TABLE history"))
        self.assertFalse(validate_input("<script>alert(1)</script>"))

    def test_calculation(self):
        self.assertEqual(secure_eval("10 + 5 * 2"), 20)
        self.assertEqual(secure_eval("(10 + 5) * 2"), 30)
        self.assertEqual(secure_eval("1/0"), None) 

    def test_sql_injection_prevention(self):
        
        malicious_input = "1', '0'); DROP TABLE history; --"
        with sqlite3.connect(DATABASE) as conn:
            
            cursor = conn.cursor()
            cursor.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (malicious_input, "error"))
            conn.commit()
            cursor.execute("SELECT * FROM history WHERE expression = ?", (malicious_input,))
            self.assertIsNotNone(cursor.fetchone())

if __name__ == '__main__':
    init_db()
    
    
    app.run(host='0.0.0.0', port=5000, debug=False)