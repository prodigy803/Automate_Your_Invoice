# Automate_Your_Invoice

It is a Python Library / Framework that aims to simplify the process of extracting information from invoices and other forms of structured PDFs. The main goal of the library is to make the entire process of automation of information extraction as accessible as possible. While the project may seem like a extension of Invoice2Data, the idea is to make it more beginner friendly and make the idea of "Automation" accessible to everyone. 

What is what in this Project?

While the ultimate goal is to have a convenient .exe file, for the purposes of "this" version, we will stick a basic command line interface and give the users options to set the template path either as a individual template or a series of templates (as part of a folder). Next we will then allow the users to set the path of the invoices and then use the templates as a sort of rule-engine to extract the information from the invoices.

What are the requirements?

The phase 1 of the project will work on pure system generated invoices. In my professional career as a auditor I described those as "Downloaded from the internet invoices" and not "Scanned invoices". Or in other words, you should be able to select the text from your daily PDF editor (Adobe Acrobat, etc.). For the "Python" Requirements, please refer to the "Requirements.txt".

The project is being developed in a MacOS requirements so windows users will find that the Requirements.txt doesnt quite work out-of-box for them. I have a work around for that. Please refer to the "Windows Requirements.txt" file for specific instructions on how to get the project running for their systems.

Libraries that are needed:
1. Poppler - I am using Conda for my package management so I just did conda install poppler
2. Pdf2txt - pip install pdftotext
3. Regex - For all those complex patterns (and probably left for the advanced users)
4. Dateparse - For Dates
5. FuzzyWuzzy - For those fields that we arent sure about.
6. Python Levenstein - This just speeds us the FuzzyWuzzy Library.

Libraries that are always good to have:
1. Numpy - Numerical Computing Library
2. Pandas - Enables handling of tabular type data and manipulating them in various ways.

# Instructions for Creating the Template:
You may use a excel file or a simple ".txt" file to create a template file:
