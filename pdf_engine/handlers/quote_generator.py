from pdf_engine.handlers.pdf_engine import PDFTemplateEngine


class QuoteGenerator:

    def __init__(self, name: str):
        self.quote = PDFTemplateEngine(name)

    def generate_quote(self):
        quote = self.quote
