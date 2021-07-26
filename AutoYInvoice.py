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

        # this variable is required for storing the address of converted invoices(PDF2Text) and for deleting those later.
        self.to_be_deleted_later_invoices_txt = []

        # this variable is required for storing the address of processed templates in yaml files and for deleting those later.
        # another idea for a future release is that this can be probably left as a choice to the end user, however that will make it
        # closer to Invoice2Data than I intended to be.
        self.to_be_deleted_later_templates_yaml = []

        # stores an internal copy of the yaml files in this variable. Can be removed after storing the yaml files.
        self.rule_base = {}

        # Once set, we dont need to change the following variables.
        self.invoices_directory = ""
        self.templates_directory = ""

        # This variable tells us whether there is one template or multiple ones
        self.need_to_classify = False

    def process_templates(self,templates_directory = ""):
        self.templates_directory = templates_directory

        # glob is library that retrieves all the files/folders that fit the end description (.txt) in our case.
        template_txts = glob.glob(templates_directory+'/*.txt')

        # This variable is set incase there are multiple templates for all the invoices. 
        # As of now this is more of a critical functionality hence I have included it.
        # v1.1 will have support for just one template.
        self.need_to_classify = False

        # Set the to_be_deleted_later_templates_yaml over here:
        self.to_be_deleted_later_templates_yaml = [x.replace('.txt','.yml') for x in template_txts]


        # If there are multiple templates, set the need-to-classify variable here:
        if len(template_txts) > 1:
            self.need_to_classify = True
        
        # lets go through the templates one by one
        if len(template_txts) == 0:
            print('Are you sure u have entered the right directory where the templates reside.')

        elif len(template_txts)>=1:
            for template_txt in template_txts:
                
                # Initialize the internal rule-dict for that particular template.
                self.rule_base[template_txt] = {}

                # Read the template file one by one.
                with open(template_txt, "r+") as f:
                    lines = f.readlines()
                f.close()

                # There are some "\n" at the end of the lines so we need to replace that or it will create an issue while creating the final
                # yaml files.
                lines = [x.replace('\n','') for x in lines]

                if self.need_to_classify:

                    # if there are multiple templates and the phrase "Classification-Rules-Over-here" is not mentioned, prompt the user to correct the template
                    if not any(["Classification-Rules-Over-here" in x for x in lines]):
                        print("Please mention the classification words and mention Classification-Rules-Over-here in the template files")
                        return "Error-Please Enter the classification tags"

                    else:
                        # Get the tags(True or False) for the lines of template that have the phrase Classification-Rules
                        tags_classification_rules = ["Classification-Rules" in x for x in lines]

                        # Get the indexs of the tags that are True
                        tags_classification_rules_2 = [i for i,x in enumerate(tags_classification_rules) if x]

                        # if there is a collision of phrases, we need to prompt the user and tell them that the phrase needs to be unique.
                        if len(tags_classification_rules_2)>2:
                            print("Please check whether 'Classification-Rules' is coming only twice in the entire template")
                            return "Error-Correct your template"
                        
                        # if there are two tags only, then proceed.
                        elif len(tags_classification_rules_2) == 2:
                            # get the individual classification tags.
                            lines_v2 = [x.split('-|-') for x in lines[tags_classification_rules_2[0]+1:tags_classification_rules_2[1]]]
                        
                        # lets go through the individual classification rules.
                        for line_v2 in lines_v2:
                            # Here we are setting individual classification tags.

                            self.rule_base[template_txt][line_v2[0]] = {'keyword':line_v2[1],'Same_Line':line_v2[2],'Sequence':line_v2[3].split(',')}
                        
                        # Lets go through the Body Rules
                        tags_body_rules = ["Body-Rules" in x for x in lines]

                        # Get the indexs of the tags that are True
                        tags_body_rules_2 = [i for i,x in enumerate(tags_body_rules) if x]

                        # similarly if there are more than 2 body tags, prompt the user to correct that mistake.
                        if len(tags_body_rules_2)>2:
                            print("Please check whether 'Classification-Rules' is coming only twice in the entire template")
                            return "Error-Correct your template"

                        # lets go through the individual body rules.
                        elif len(tags_body_rules_2) == 2:
                            # Here we are getting individual body tags.

                            lines_v2 = [x.split('-|-') for x in lines[tags_body_rules_2[0]+1:tags_body_rules_2[1]]]
                        
                        for line_v2 in lines_v2:
                            # Here we are setting individual body tags.
                            self.rule_base[template_txt][line_v2[0]] = {'keyword':line_v2[1],'Position':line_v2[2],'Type':line_v2[3],'Free Floating':line_v2[4],'Delimiter':line_v2[5]}
                elif self.need_to_classify==False:
                    # Lets go through the Body Rules
                    tags_body_rules = ["Body-Rules" in x for x in lines]

                    # Get the indexs of the tags that are True
                    tags_body_rules_2 = [i for i,x in enumerate(tags_body_rules) if x]

                    # similarly if there are more than 2 body tags, prompt the user to correct that mistake.
                    if len(tags_body_rules_2)>2:
                        print("Please check whether 'Classification-Rules' is coming only twice in the entire template")
                        return "Error-Correct your template"

                    # lets go through the individual body rules.
                    elif len(tags_body_rules_2) == 2:
                        # Here we are getting individual body tags.

                        lines_v2 = [x.split('-|-') for x in lines[tags_body_rules_2[0]+1:tags_body_rules_2[1]]]
                    
                    for line_v2 in lines_v2:
                        # Here we are setting individual body tags.
                        self.rule_base[template_txt][line_v2[0]] = {'keyword':line_v2[1],'Position':line_v2[2],'Type':line_v2[3],'Free Floating':line_v2[4],'Delimiter':line_v2[5]}
                    
                # lets write down the internal rule-dicts into yaml file for better debugging and processing.
                with open(template_txt.replace('txt','yml'), 'w') as outfile:
                    yaml.dump(self.rule_base[template_txt], outfile, default_flow_style=False)


    def process_invoices(self,invoices_directory = ""):
        self.invoices_directory = invoices_directory

        ## OS.walk will be integrated later.
        invoice_pdfs = glob.glob(invoices_directory+'/*.pdf')

        ## if there are no pdfs, then u need to prompt the user telling them to point the correct folder
        if len(invoice_pdfs) == 0:
            print('Are you sure you have mentioned the correct invoices directory (containing .pdf files)')

        ## if there are more than zero pdfs process them and convert them into text files.
        elif len(invoice_pdfs)>=1:

            # store the file names so that we can delete the temporary files later on.
            self.to_be_deleted_later_invoices_txt = [x.replace('.pdf','.txt') for x in invoice_pdfs]

            for invoice_pdf in invoice_pdfs:
                text_file = open(invoice_pdf.replace('pdf','txt'), "w")            

                with open(invoice_pdf, "rb") as f:
                    pdf = pdftotext.PDF(f)
                    for page in pdf:
                        text_file.write(page)

                text_file.close()

    # This function is for purely checking out the content of the yaml files.
    def process_yaml_file(self,):
        # since the yaml files have been stored to be deleted later, we can just access those files to delete later on.

        for file in self.to_be_deleted_later_templates_yaml:
            with open(file, 'r') as stream:
                try:
                    print(yaml.safe_load(stream))
                except yaml.YAMLError as exc:
                    print(exc)

    # this one sort of cleans up all the intermediate files that were processed earlier.
    def delete_all_files(self):
        # we need to delete all the temporary files that we have built

        for file in self.to_be_deleted_later_invoices_txt:
            os.remove(file)

        for file in self.to_be_deleted_later_templates_yaml:
            os.remove(file)
    
    # This function ensures that the word that is extracted from the invoice matches the type that it is mentioned as in the template.
    def type_converter(self,type_of_word = "Number", value=0):

        if type_of_word == "Number":
            try:
                return float(value.replace(',',''))

            except:
                print("{} is not a number/float".format(value))
                return None
        
        elif (type_of_word == "Multiple Text") or (type_of_word == "Text"):
            try:
                return str(value)

            except:
                print("{} is not a string".format(value))
                return None

        elif ("M" in type_of_word) or ("Y" in type_of_word) :
            try:
                return dateutil.parser.parse(value)

            except:
                print("some issue with the date time for {}".format(value))
                return None
    
    # checking if the next value/word matches the format mentioned in the template.
    def next_number_matcher(self,type_of_word="Number",value=0):

        if value.isdigit() and type_of_word == "Number":
            return True

        elif value.isalpha() and ((type_of_word == "Text") or (type_of_word=='Multiple Text')):
            return True
        
        elif ("M" or "Y" in type_of_word):
            return True

        else:
            return False

    # this is the refactored code, initially it was stored under extract_data
    # this is essentially accepting a template(matched in case of classificaiton),
    # the lines of the invoice and the invoice name for storing the data in a excel file.
    def extract_final_data(self,template="",lines="",invoice_name=""):
        
        # this will store all the hits that we get in a particular invoice.
        sub_matched_dict = {}

        # Select one field key at a time
        for field_key in template.keys():

            # Filtering for field keys
            if "Field" in field_key:
                
                # Parsing the template for the final extraction:
                word_to_be_searched = template[field_key]['keyword']
                where_is_the_word = template[field_key]['Position']
                type_of_word = template[field_key]['Type']
                any_delimiter = template[field_key]['Delimiter']

                # Now lets check where that word to be searched is coming
                for line in lines:
                    
                    if word_to_be_searched in line:
                        # In case the word is on the left most, i want to avoid errors that might come during processing.                                 
                        line = 'start_tag ' + line

                        # This is because sometimes the delimiters are actually stuck to the words and i have to have proper spacing
                        # This is for making the .split() function work as desired and not have unintended consequences.
                        line = line.replace(any_delimiter," " + any_delimiter + " ")

                        # This removes all the spaces from the doc.
                        line = re.sub(' +', ' ', line)

                        # These characters maybe stuck in the words too or they maybe unnecessarily coming in the doc which is reduce
                        # the accuracy of the final output.
                        for character in ["₹","$"]:
                            line = line.replace(character,'')
                        
                        # Once the line has been processed, we will check if the word to be searched is one word or multi word.
                        # If the word_to_be_seached is one word, a simple -> str(line).split().index('word_to_be_seached') will give 
                        # us the position of the word in a particular line.

                        # However if there are multiple words we need to sort of track the length of the word and search the string(line of invoice) for it,
                        # rather than converting the string into a list. One we get the start index, we need to do 
                        # str(line)[str(line).index('word_to_be_seached) : str(line).index('word_to_be_seached) + len(word_to_be_seached)] to get the matched word.

                        if len(word_to_be_searched.split()) == 1:
                            
                            line = line.split()

                            if where_is_the_word == "Right":

                                if any_delimiter == "None":

                                    word = line[line.index(word_to_be_searched)+1]
                                    
                                    sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]
                                    break

                                elif any_delimiter != "None":
                                    
                                    if line[line.index(word_to_be_searched)+1] == any_delimiter:
                                        
                                        word = line[line.index(word_to_be_searched)+2]

                                        sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]
                                        break
                            elif where_is_the_word == "Left":
                                
                                if any_delimiter == "None":
                                    
                                    word = line[line.index(word_to_be_searched)-1]

                                    sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]
                                    break
                                elif any_delimiter != "None":

                                    if line[line.index(word_to_be_searched)-1] == any_delimiter:
                                        word = line[line.index(word_to_be_searched)-2]

                                        sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]
                                        break
                            
                        elif len(word_to_be_searched.split()) > 1:

                            if where_is_the_word == "Right":

                                if any_delimiter == "None":

                                    word_len = len(word_to_be_searched)

                                    line = line[line.index(word_to_be_searched)+ word_len:]

                                    word = line.split()[0]

                                    if self.next_number_matcher(type_of_word=type_of_word, value = word):
                                        sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]
                                        break
                                elif any_delimiter != "None":

                                    word_len = len(word_to_be_searched)

                                    if line[line.index(word_to_be_searched)+word_len + 1] == any_delimiter:

                                        line = line[line.index(word_to_be_searched)+ word_len+2:]

                                        word = line.split()[0]
                                
                                        sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]
                                        break

                            elif where_is_the_word == "Left":
                                
                                if any_delimiter == "None":

                                    word_len = len(word_to_be_searched)

                                    line = line[:line.index(word_to_be_searched)]
                                    
                                    word = line.split()[-1]

                                    sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]
                                    break
                                
                                elif any_delimiter != "None":

                                    word_len = len(word_to_be_searched)

                                    if line[line.index(word_to_be_searched)+word_len - 1] == any_delimiter:

                                        line = line[:line.index(word_to_be_searched)]
                                        
                                        word = line.split()[-2]

                                        sub_matched_dict[word_to_be_searched] = [self.type_converter(type_of_word = type_of_word, value = word)]
                                        break
        if bool(sub_matched_dict):
            # print(sub_matched_dict)
            print(invoice_name.replace('.txt','.xlsx'))
            pd.DataFrame.from_dict(sub_matched_dict).to_excel(invoice_name.replace('.txt','.xlsx'),index=False)

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
                if self.need_to_classify:
                    if "Keyword" in key:

                        # Now let us read the invoices one by one and check where that word is classifying
                        for invoice in self.to_be_deleted_later_invoices_txt:

                            with open(invoice, "r+") as f:
                                lines = f.readlines()

                            # This is checking if the classification keyword is coming in the invoice or not
                            # if it occurs, then go through the field keys one by one
                            if template[key]['keyword'] in " ".join(lines):
                                self.extract_final_data(template=template,lines=lines,invoice_name=invoice)

                else:
                    # Now let us read the invoices one by one and check where that word is classifying
                        for invoice in self.to_be_deleted_later_invoices_txt:

                            with open(invoice, "r+") as f:
                                lines = f.readlines()
                            
                            self.extract_final_data(template=template,lines=lines,invoice_name=invoice)

        
if __name__ == '__main__':
    print('Please enter the path to the invoices')
    input1 = str(input())

    print('Please enter the path to the templates')
    input2 = str(input())

    autoyinvoice_instance = AutoYInvoice()

    try:
        autoyinvoice_instance.process_invoices(invoices_directory = '/Users/pushkarajjoshi/Desktop/Projects/Automate_Your_Invoice/Demo/Demo_2/Invoices')

    except:
        print('There was some problem processing the invoice, are you sure you are following the guidelines?')
        print('Please note the framework requires soft-copy challans and not scanend ones.')

    try:
        autoyinvoice_instance.process_templates(templates_directory = '/Users/pushkarajjoshi/Desktop/Projects/Automate_Your_Invoice/Demo/Demo_2/Templates')

    except:

        print('There was some problem processing the , are you sure you are following the guidelines?')
        print('Please note the use of @---------------Body-Rules-Rules-Over-here---------------------- in the template?')

    dataframe = autoyinvoice_instance.extract_data()

    # autoyinvoice_instance.process_yaml_file()

    autoyinvoice_instance.delete_all_files()

    print('Invoices Converted Successfully')