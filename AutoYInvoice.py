from Support_Functions import * 

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

    autoyinvoice_instance.consolidate_and_delete_all()

    print('Invoices Converted Successfully')