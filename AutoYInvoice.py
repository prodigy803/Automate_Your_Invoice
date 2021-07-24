import os
import pdftotext
import glob
import pprint
import yaml

class AutoYInvoice:

    def __init__(self):
        self.to_be_deleted_later_invoices_txt = []
        self.to_be_deleted_later_templates_yaml = []
        self.rule_base = {}
        self.invoices_directory = ""
        self.templates_directory = ""

    def process_templates(self,templates_directory = ""):
        self.templates_directory = templates_directory

        template_txts = glob.glob(templates_directory+'/*.txt')
        
        need_to_classify = False

        
        if len(template_txts) > 1:
            need_to_classify = True
        
        for template_txt in template_txts:

            self.rule_base[template_txt] = {}

            print(template_txt)

            with open(template_txt, "r+") as f:
                lines = f.readlines()
            f.close()

            if need_to_classify:
                if not any(["Classification-Rules-Over-here" in x for x in lines]):
                    print("Please mention the classification words and mention Classification-Rules-Over-here in the template files")
                    return "Error-Please Enter the classification tags"

                else:
                    tags = ["Classification-Rules" in x for x in lines]
                    tags2 = [i for i,x in enumerate(tags) if x]

                    if len(tags2)>2:
                        print("Please check whether 'Classification-Rules' is coming only twice in the entire template")
                        return "Error-Correct your template"

                    elif len(tags2) == 2:
                        lines_v2 = [x.split('-|-') for x in lines[tags2[0]+1:tags2[1]]]

                        for line_v2 in lines_v2:
                            self.rule_base[template_txt][line_v2[0]] = {'keyword':line_v2[1],'Same_Line':line_v2[2],'Sequence':line_v2[3].split(',')}
                        
            with open(template_txt.replace('txt','yml'), 'w') as outfile:
                yaml.dump(self.rule_base[template_txt], outfile, default_flow_style=False)

                self.to_be_deleted_later_templates_yaml.append(template_txt.replace('txt','yml'))

        
    def process_invoices(self,invoices_directory = ""):
        self.invoices_directory = invoices_directory

        ## OS.walk will be integrated later.
        invoice_pdfs = glob.glob(invoices_directory+'/*.pdf')
        
        for invoice_pdf in invoice_pdfs:
            text_file = open(invoice_pdf.replace('pdf','txt'), "w")
            
            self.to_be_deleted_later_invoices_txt.append(invoice_pdf.replace('pdf','txt'))
            

            with open(invoice_pdf, "rb") as f:
                pdf = pdftotext.PDF(f)
                for page in pdf:
                    print(page)
                    text_file.write(page)

            text_file.close()

        
if __name__ == '__main__':
    print('Please enter the path to the invoices')
    input1 = str(input())

    print('Please enter the path to the templates')
    input2 = str(input())

    autoyinvoice_instance = AutoYInvoice()

    try:

        autoyinvoice_instance.process_invoices(invoices_directory = '/Users/pushkarajjoshi/Desktop/Projects/Automate_Your_Invoice/Demo/Demo_1/Invoices')

    except:
        print('There was some problem processing the invoice, are you sure you are following the guidelines?')
        print('Please note the framework requires soft-copy challans and not scanend ones.')

    try:

        autoyinvoice_instance.process_templates(templates_directory = '/Users/pushkarajjoshi/Desktop/Projects/Automate_Your_Invoice/Demo/Demo_1/Templates')

    except:

        print('There was some problem processing the template, are you sure you are following the guidelines?')
        print('Please note the use of @---------------Classification-Rules-Over-here---------------------- in the template?')
