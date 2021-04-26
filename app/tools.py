from random import choice
from sdamgia import SdamGIA
from os.path import exists
from os import mkdir
from string import ascii_letters
from shutil import rmtree
import fitz


class FMath:
    __slots__ = ['sdamgia', 'subject', 'pdf', 'test_id']

    def __init__(self, file_stream, subject: str, exam: str):
        # Define some variables
        self.sdamgia: SdamGIA = self.gen_api(subject, exam)
        self.subject: str = subject
        # Setup folders
        if not exists('./temp'):
            mkdir('./temp')
        # Setup files
        name = self.setup_file(file_stream)
        self.pdf = fitz.open(f'./temp/{name}.pdf')

    def setup_file(self, file_stream) -> str:
        name: str = self.random_name()
        with open(f'./temp/{name}.pdf', 'wb') as pdf:
            pdf.write(file_stream.stream.read())
        return name

    def random_name(self) -> str:
        return ''.join(choice(ascii_letters) for _ in range(15))

    def gen_api(self, subject, exam) -> SdamGIA:
        api = SdamGIA()
        api._SUBJECT_BASE_URL[
            subject] = f'https://{subject}-{exam}.{api._BASE_DOMAIN}'
        return api

    def get_test_id(self):
        for page_number in range(0, self.pdf.pageCount):
            page = self.pdf.loadPage(page_number)
            text = page.getText('text')
            if 'Вариант' in text:
                index = text.index('Вариант №') + 9
                return text[index: index + 9].strip()

    def exit(self) -> None:
        self.pdf.close()
        rmtree('./temp/')

    def solution(self) -> str:
        return self.sdamgia.generate_pdf(
            self.subject, testid=self.test_id, pdf='h', answers='true')


