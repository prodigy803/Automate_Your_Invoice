import os
import pdftotext
import glob
import pprint
import yaml
import pandas as pd
import dateutil.parser
import re

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

        # print(template_txts)
        
        need_to_classify = False

        self.to_be_deleted_later_templates_yaml = [x.replace('.txt','.yml') for x in template_txts]


        if len(template_txts) > 1:
            need_to_classify = True
        
        for template_txt in template_txts:

            self.rule_base[template_txt] = {}

            with open(template_txt, "r+") as f:
                lines = f.readlines()
            f.close()

            lines = [x.replace('\n','') for x in lines]

            if need_to_classify:
                if not any(["Classification-Rules-Over-here" in x for x in lines]):
                    print("Please mention the classification words and mention Classification-Rules-Over-here in the template files")
                    return "Error-Please Enter the classification tags"

                else:
                    tags_classification_rules = ["Classification-Rules" in x for x in lines]
                    tags_classification_rules_2 = [i for i,x in enumerate(tags_classification_rules) if x]


                    if len(tags_classification_rules_2)>2:
                        print("Please check whether 'Classification-Rules' is coming only twice in the entire template")
                        return "Error-Correct your template"

                    elif len(tags_classification_rules_2) == 2:
                        lines_v2 = [x.split('-|-') for x in lines[tags_classification_rules_2[0]+1:tags_classification_rules_2[1]]]
                    
                    for line_v2 in lines_v2:

                        self.rule_base[template_txt][line_v2[0]] = {'keyword':line_v2[1],'Same_Line':line_v2[2],'Sequence':line_v2[3].split(',')}
                    
                    tags_body_rules = ["Body-Rules" in x for x in lines]
                    tags_body_rules_2 = [i for i,x in enumerate(tags_body_rules) if x]

                    if len(tags_body_rules_2)>2:
                        print("Please check whether 'Classification-Rules' is coming only twice in the entire template")
                        return "Error-Correct your template"

                    elif len(tags_body_rules_2) == 2:
                        lines_v2 = [x.split('-|-') for x in lines[tags_body_rules_2[0]+1:tags_body_rules_2[1]]]

                    # print(lines_v2)
                    for line_v2 in lines_v2:
                        self.rule_base[template_txt][line_v2[0]] = {'keyword':line_v2[1],'Position':line_v2[2],'Type':line_v2[3],'Free Floating':line_v2[4],'Delimiter':line_v2[5]}

            with open(template_txt.replace('txt','yml'), 'w') as outfile:
                yaml.dump(self.rule_base[template_txt], outfile, default_flow_style=False)


    def process_invoices(self,invoices_directory = ""):
        self.invoices_directory = invoices_directory

        ## OS.walk will be integrated later.
        invoice_pdfs = glob.glob(invoices_directory+'/*.pdf')

        # print(invoice_pdfs)
        self.to_be_deleted_later_invoices_txt = [x.replace('.pdf','.txt') for x in invoice_pdfs]

        for invoice_pdf in invoice_pdfs:
            text_file = open(invoice_pdf.replace('pdf','txt'), "w")            

            with open(invoice_pdf, "rb") as f:
                pdf = pdftotext.PDF(f)
                for page in pdf:
                    text_file.write(page)

            text_file.close()


    def process_yaml_file(self,):
        # since the yaml files have been stored to be deleted later, we can just access those files to delete later on.

        for file in self.to_be_deleted_later_templates_yaml:
            with open(file, 'r') as stream:
                try:
                    print(yaml.safe_load(stream))
                except yaml.YAMLError as exc:
                    print(exc)

    def delete_all_files(self):
        # we need to delete all the temporary files that we have built

        for file in self.to_be_deleted_later_invoices_txt:
            os.remove(file)

        for file in self.to_be_deleted_later_templates_yaml:
            os.remove(file)

    def type_converter(self,type_of_word = "Number", value=0):

        # print(value)

        dates = ['DD-MMM-YYYY']

        if type_of_word == "Number":
            return float(value.replace(',',''))
        
        elif (type_of_word == "Multiple Text") or (type_of_word == "Text"):
            return str(value)

        elif ("M" in type_of_word) or ("Y" in type_of_word) :
            print(value)
            return dateutil.parser.parse(value)

    def next_number_matcher(self,type_of_word="Number",value=0):
        if value.isdigit() and type_of_word == "Number":
            return True

        elif value.isalpha() and ((type_of_word == "Text") or (type_of_word=='Multiple Text')):
            return True
        
        elif ("M" or "Y" in type_of_word):
            return True
        else:
            return False


    def extract_data(self,value=0):
        templates = []

        for file in self.to_be_deleted_later_templates_yaml:
            with open(file, 'r') as stream:
                try:
                    templates.append(yaml.safe_load(stream))
                except yaml.YAMLError as exc:
                    print(exc)

        # Lets go through one by one template
        for template in templates:

            # lets look at the individual keys in the template
            for key in template.keys():

                # Lets extract the classification keyword from the template
                if "Keyword" in key:
                    
                    # Once the classification keyword has been highlighted, lets check where that is matching

                    # Now let us read the invoices one by one and check where that word is classifying

                    for invoice in self.to_be_deleted_later_invoices_txt:
                        counter =0
                        matching_dict = []
                        sub_matched_dict = {}
                        print(invoice)
                        with open(invoice, "r+") as f:
                            lines = f.readlines()

                        # This is checking if the classification keyword is coming in the invoice or not
                        # if it occurs, then go through the field keys one by one
                        if template[key]['keyword'] in " ".join(lines):

                            # Select one field key at a time
                            for field_key in template.keys():

                                # Filtering for field keys
                                if "Field" in field_key:
                                    
                                    # Parsing the template for the final extraction:
                                    word_to_be_searched = template[field_key]['keyword']
                                    where_is_the_word = template[field_key]['Position']
                                    type_of_word = template[field_key]['Type']
                                    any_delimiter = template[field_key]['Delimiter']

                                    # if "Y" in type_of_word:
                                    #     print(word_to_be_searched, type_of_word, where_is_the_word, any_delimiter)

                                    # now lets check where that word to be searched is coming
                                    for line in lines:
                                        
                                        if word_to_be_searched in line:
                                                                                        
                                            line = 'start_tag ' + line
                                            line = line.replace(any_delimiter," " + any_delimiter + " ")
                                            line = re.sub(' +', ' ', line)

                                            for character in ["₹","$"]:
                                                line = line.replace(character,'')
                                            
                                            print(word_to_be_searched)
                                            if len(word_to_be_searched.split()) == 1:
                                                
                                                line = line.split()

                                                if where_is_the_word == "Right":

                                                    if any_delimiter == "None":

                                                        word = line[line.index(word_to_be_searched)+1]
                                                        
                                                        sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]

                                                    elif any_delimiter != "None":
                                                        
                                                        if line[line.index(word_to_be_searched)+1] == any_delimiter:
                                                            
                                                            word = line[line.index(word_to_be_searched)+2]

                                                            sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]

                                                elif where_is_the_word == "Left":
                                                    
                                                    if any_delimiter == "None":
                                                        
                                                        word = line[line.index(word_to_be_searched)-1]

                                                        sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]

                                                    elif any_delimiter != "None":

                                                        if line[line.index(word_to_be_searched)-1] == any_delimiter:
                                                            word = line[line.index(word_to_be_searched)-2]

                                                            sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]

                                            elif len(word_to_be_searched.split()) > 1:

                                                print('Multiple words',word_to_be_searched,where_is_the_word,any_delimiter)

                                                if where_is_the_word == "Right":

                                                    if any_delimiter == "None":

                                                        word_len = len(word_to_be_searched)

                                                        line = line[line.index(word_to_be_searched)+ word_len:]

                                                        word = line.split()[0]

                                                        if self.next_number_matcher(type_of_word=type_of_word, value = word):
                                                            sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]

                                                    elif any_delimiter != "None":

                                                        word_len = len(word_to_be_searched)

                                                        if line[line.index(word_to_be_searched)+word_len + 1] == any_delimiter:

                                                            line = line[line.index(word_to_be_searched)+ word_len+2:]

                                                            word = line.split()[0]
                                                    
                                                            sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]


                                                elif where_is_the_word == "Left":
                                                    
                                                    if any_delimiter == "None":

                                                        word_len = len(word_to_be_searched)

                                                        line = line[:line.index(word_to_be_searched)]
                                                        
                                                        word = line.split()[-1]

                                                        sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]

                                                    elif any_delimiter != "None":

                                                        word_len = len(word_to_be_searched)

                                                        if line[line.index(word_to_be_searched)+word_len - 1] == any_delimiter:

                                                            line = line[:line.index(word_to_be_searched)]
                                                            
                                                            word = line.split()[-2]

                                                            sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]
                                

                        if bool(sub_matched_dict):
                            print(invoice)
                            print(pd.DataFrame.from_dict(sub_matched_dict))
        
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

        print('There was some problem processing the , are you sure you are following the guidelines?')
        print('Please note the use of @---------------Body-Rules-Rules-Over-here---------------------- in the template?')

    dataframe = autoyinvoice_instance.extract_data()

    # autoyinvoice_instance.process_yaml_file()

    # autoyinvoice_instance.delete_all_files()