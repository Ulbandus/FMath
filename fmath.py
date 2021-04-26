from sdamgia import SdamGIA
import fitz
from flask import Flask, render_template, request
from os import mkdir, environ
from shutil import rmtree
from random import choice

app = Flask(__name__, template_folder='./templates/')


class FMath:
    def __init__(self, file_stream, subject, exam):
        self.sdamgia = self.gen_api(subject, exam)
        self.subject = subject

        mkdir('./temp')

        with open('./temp/file.pdf', 'wb') as pdf:
            pdf.write(file_stream.stream.read())
        self.name = self.gen_name()
        self.pdf = fitz.open(f'./temp/{name}.pdf')

    def gen_name(self):
        letters = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        return ''.join(choice(letters) for _ in range(10))

    def gen_api(self, subject, exam):
        api = SdamGIA()
        api._SUBJECT_BASE_URL[subject] = f'https://{subject}-{exam}.{api._BASE_DOMAIN}'
        return api

    def read(self):
        for page_number in range(0, self.pdf.pageCount):
            page = self.pdf.loadPage(page_number)
            text = page.getText('text')
            if 'Вариант' in text:
                index = text.index('Вариант №') + 9
                return text[index: index + 9].strip()

    def exit(self):
        self.pdf.close()
        rmtree('./temp/')

    def solution(self):
        return self.sdamgia.generate_pdf(
            self.subject, testid=self.test_id, pdf='h', answers='true')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/solution', methods=['POST', 'GET'])
def solution():
    if request.method == 'POST':
        file = request.files['file']
        subject = request.form['subject']
        exam = request.form['exam']
        fmath = FMath(file, subject, exam)
        fmath.test_id = fmath.read()
        solution_path = fmath.solution()
        fmath.exit()
        return render_template('solution.html', file=solution_path)


app.run(port=environ.get('PORT', 5000), host='0.0.0.0')

