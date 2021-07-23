import os
import pdftotext
import glob

class AutoYInvoice:
    def __init__(self):
        self.counter = 0

    def get_templates(self,templates_directory = ""):
        pass

    def process_invoices(self,invoices_directory = ""):

        for invoice_pdf in glob.glob(invoices_directory+'/*.pdf'):
            print(invoice_pdf)
            with open(invoice_pdf, "rb") as f:
                pdf = pdftotext.PDF(f)
                for page in pdf:
                    print(page)

        
if __name__ == '__main__':
    print('Please enter the path to the invoices')
    input1 = str(input())

    print('Please enter the path to the templates')
    input2 = str(input())

    autoyinvoice_instance = AutoYInvoice()

    autoyinvoice_instance.process_invoices(invoices_directory = input1)

    