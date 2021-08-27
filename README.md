# Automate_Your_Invoice

It is a Python Library / Framework that aims to simplify the process of extracting information from invoices and other forms of structured PDFs. The main goal of the library is to make the entire process of automation of information extraction as accessible as possible. While the project may seem like a extension of Invoice2Data, the idea is to make it more beginner friendly and make the idea of "Automation" accessible to everyone. 

---

| Index                                  |
| ---------------------------------------|
| [What is what in this Project?] (#what-is-what-in-this-Project? )         |
| [What are the requirements?] (#what-are-the-requirements?)             |
| [Instructions for Creating the Template] (# -instructions-for-creating-the-template:) |
| [Ending Output] (#ending-output:)                          |
| [Future Developement] (#future-developement:)                    |

---

# What is what in this Project?

While the ultimate goal is to have a convenient .exe file, for the purposes of "this" version, we will stick a basic command line interface and give the users options to set the template path either as a individual template or a series of templates (as part of a folder). Next we will then allow the users to set the path of the invoices and then use the templates as a sort of rule-engine to extract the information from the invoices.

# What are the requirements?

The phase 1 of the project will work on pure system generated invoices. In my professional career as a auditor I described those as "Downloaded from the internet invoices" and not "Scanned invoices". Or in other words, you should be able to select the text from your daily PDF editor (Adobe Acrobat, PDF Xchange etc.). For the "Python" Requirements, please refer to the "Requirements.txt".

<b>Libraries that are needed:</b>
1. Poppler - I am using Conda for my package management so I just did conda install poppler
2. Pdf2txt - pip install pdftotext
3. Regex - For all those complex patterns (and probably left for the advanced users)
4. Dateparse - For Dates - pip install daterparse
5. FuzzyWuzzy - For those fields that we arent sure about - Just did pip install fuzzywuzzy
6. Python Levenstein - This just speeds us the FuzzyWuzzy Library - pip install python-levenstein

<b>Libraries that are always good to have:</b>
1. Numpy - Numerical Computing Library
2. Pandas - Enables handling of tabular type data and manipulating them in various ways.

The project is being developed in a MacOS requirements so windows users will find that the Requirements.txt doesnt quite work out-of-box for them. I have a work around for that. Please refer to the "Windows Requirements.txt" file for specific instructions on how to get the project running for their systems.

***

# Instructions for Creating the Template:

You may use a excel file or a simple ".txt" file to create a template file.

Please refer to "Templates/Sample_Template.txt" for a sample format of how a template should be. 

Here is a reference for what the key-words mean inside in the template:

- **Keyword 1** - This is just index and you just need to add "Keyword 1", "Keyword 2" while adding an additional rule.

    - **Classification_word_1** - Say incase you have multiple formats of the invoices and you want to adapt "Automate Your Invoice" too all the formats, then you would need to identify specific keywords for the individual formats and create specific templates for them. For eg. you have two invoices from two vendors, then you need to create two templates for both of them and incase you feel both of them have same formats (or all of different invoices have same format) then you can skip out on the classification words part of things.

    - **Same_line_as_any_other_keyword** - If you have 2 or more keywords, you have a choice of defining which "Keyword" (for our sample whether its "Keyword 1" or "Keyword 2" like that) is that particular keyword in the same line with. For eg if Keyword 1 and Keyword 2 are in the same line then you need to mention that. If there are multiple keywords, then you need to encapsulate them as a list like ['Keyword 1','Keyword 3','Keyword 3',].

    - **Order_of_keywords** - Incase the "Same_line_as_any_other_keyword" is not None, then you need to mention how the keywords are appearing in the docs like if Keyword 2 is appearing before Keyword 1, then Order_of_keywords = [Keyword 2, Keyword 1].

- **Field 1** - This is just index and you just need to add "Field 1", "Field 2" while adding an additional rule.

    - **Keyword_as_appearing_in_PDF** - This will be placeholder text around which the information you need to extract exists. For example you want to capture 1000 in Total Amount 1,000.00, then the keyword will be "Total Amount".

    - **Where_is_the_target_information** - This is another crucial piece of information as sometimes we need access to information on the left of the keyword. For our previous example of "Total Amount 1,000.00", the Where_is_the_target_information = 'Right'. Incase the example was 1000 Total Amount, then you would use "Left". Here are all the different tags that you can mention:

        - Left - Currently Working
        - Right - Currently Working
        - Above - To be integrated in V2
        - Below - To be integrated in V2
        - Leftmost - incase the word is on the first item in the row.  - To be integrated in V2
        - Rightmost - incase the word is on the last item in the row.  - To be integrated in V2


    - **Type_of_information** - You need to specify whether the information we are extracting is a number, text or a date. For example in our example we were extracting "1000" so its a number. The different types of information that you can specify is:
        - Number
        - Text
        - Multiple Text
        - Date - Then you need to enter the format of the date (DD/MM/YYYY) or (DD/MM/YY) or whatever the actual format is .

    - **Any_Free_Floating_Text_Inbetween** - This tells me whether there is any free floating text between the "Keyword *" and the required information that is to be extracted. Please note that if the targeted information is a text and there is presence of free floating text in the document, it can cause incorrect data to be extracted so you need to be careful with that. Also note that if a number / date is to be extracted and if a number and the specified dateformat comes in the floating text, that might also cause incorrect information to be extracted.

    - **Any_Special_Character_delimiting_Keyword_**&_Target_information - if Any_Free_Floating_Text_Inbetween is None, then you can specific if there any special delimiter that is seperating the keyword and the targetd information. For our example, there is no special delimiter, but if our example becomes this "Total Amount = 1000", then the delimiter is "=".

# Ending Output:
- As of now the output is being delivered "Invoice Wise" into individual excel files. Later on the plan is to consolidate the invoices based on the template and give a consolidated excel instead of standalone excel files.

- As of now you may use a simple pandas based script to consolidate the excel files as per your need.

# Future Developement:
- As of now I am planning for letting users consume this service via multiple ways:
    - Publish on Pypi
    - Create a .exe
    - Create a website - This will open up a huge set of possibilities and I can actually expand the product into multiple things
        - Create a containerized application using Docker.
        - Use Cloud ML capabilities for my future features.
        - Make the solution more accessible.
    - Create a mobile application for people to upload the doc and get the best results (however this will require a big redesign.)

- Ultimate goal of this project is to contribute to the community in any way possible and learn a lot at the same time.

Footnote:
There are still some bugs in the code that will be ironed out by v1.2. Please be assured that the demo is worked correct as expected and you will be able to see the raw output in the invoice folder of "Demo/Demo_1" or "Demo/Demo_2".

Thanks,
PJ