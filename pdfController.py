import requests
import regex as re

# import pdfMiner
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

class pdf_controller():
    def __init__(self, pdf_path) -> None:
        # mongodb://localhost:27017/
        # scraperGoogleScholar
        self.pdf = pdf_path
        self.pdf_text = None
        pass

    def extract_text_from_pdf(self):
        # Open the PDF file
        with open(self.pdf, 'rb') as file:
            # Create a PDF resource manager object
            resource_manager = PDFResourceManager()

            # Set up a StringIO object to hold the text
            text_io = StringIO()

            # Create a PDF device object
            device = TextConverter(resource_manager, text_io, laparams=LAParams())

            # Create a PDF interpreter object
            interpreter = PDFPageInterpreter(resource_manager, device)

            # Process each page
            for page in PDFPage.get_pages(file):
                interpreter.process_page(page)

            # Extract the text
            text = text_io.getvalue()

            # Clean up
            device.close()
            text_io.close()

            # Return the text
            self.pdf_text = text

    def extract_abstract_from_pdf(self):
        if(self.pdf_text == None):
            self.extract_text_from_pdf()

        for combination in ['Abstract', 'abstract', 'ABSTRACT']:
            if(combination in self.pdf_text):
                index_of_first_abstract = self.pdf_text.index('Abstract')+len('Abstract\n')
                text_after_word_abstract_before_newline = self.pdf_text[index_of_first_abstract:].find('\n\n')
                return ' '.join(self.pdf_text[index_of_first_abstract : index_of_first_abstract+text_after_word_abstract_before_newline].splitlines())

    def save_pdf(self, pdf_url):
        chunk_size = 2000
        r = requests.get(pdf_url, stream=True)
        try:
            with open(self.pdf, 'wb') as f:
                for chunk in r.iter_content(chunk_size):
                    f.write(chunk)
            f.close()
            return True
        except:
            return False    