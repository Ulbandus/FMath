from traceback import print_exc
from .tools import FMath
from app import app
from flask import render_template, request, redirect, send_file


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/solution', methods=['POST', 'GET'])
def solution():
    if request.method == 'POST':
        try:
            file = request.files['file']
            subject = request.form['subject']
            exam = request.form['exam']
            fmath = FMath(file, subject, exam)
            fmath.test_id = fmath.get_test_id()
            solution_path = fmath.solution()
            fmath.exit()
        except Exception:
            print_exc()
            return redirect('/?action=error_alert')
        return render_template('solution.html', file=solution_path)
    else:
        return redirect('/')


@app.route('/favicon.ico')
def favicon():
    return send_file('static/images/favicon.ico')


@app.errorhandler(404)
def error(error):
    return redirect('/')
