class Document:
    def __init__(self, text: str):
        self.text = text

    def clean(self):
        return self.text.lower().strip()

    def word_count(self):
        return len(self.text.split())
    
class PDFDocument(Document):
    def __init__(self, text: str, pages: int):
        super().__init__(text)
        self.pages = pages

    def page_density(self):
        # words per page
        return self.word_count() / self.pages if self.pages > 0 else 0
    
class InvoiceDocument(Document):
    def extract_total(self):
            lines = self.text.splitlines()
            for line in lines:
                if "total" in line.lower():
                    parts = line.split()
                    for part in parts:
                        try:
                            amount = float(part.replace('$', '').replace(',', ''))
                            return amount
                        except ValueError:
                            continue
            return None

    def extract_invoice_id(self):
        lines = self.text.splitlines()
        for line in lines:
            if "invoice id" in line.lower():
                parts = line.split()
                for part in parts:
                    if part.isalnum() and len(part) > 3:
                        return part
        return None
