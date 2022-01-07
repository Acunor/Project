import PyPDF2 
import docx
import docx2txt
import os
from acunor_rp_parse import Parser

class FileFetcher(object):
    
    def __init__(self):
        self.parser=Parser()
                                      
    
    def fetch_and_parse_file(self):     
        split_tup = os.path.splitext('resume.pdf')
        file_extension = split_tup[1]
        if file_extension=='.pdf':
            text=self.fetch_pdf_file()
            return self.parser.parse_text(text)
        elif file_extension=='.docx':
            text=self.fetch_docx_file()
            return self.parser.parse_text(text)
        else:
            print("Invalid Formate") 
#         text=self.fetch_pdf_file()
#         self.parser.parse_text(text)
#         text=self.fetch_docx_file()
#         self.parser.parse_text(text)

           
    
    def fetch_pdf_file(self):
        filename ='resume.pdf'
        pdfFileObj = open(filename,'rb')               #open allows you to read the file
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)   #The pdfReader variable is a readable object that will be parsed
        num_pages = pdfReader.numPages                 #discerning the number of pages will allow us to parse through all the pages
        count = 0
        text = ""
        while count < num_pages:                       #The while loop will read each page
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText()
        return text
    
    def fetch_docx_file(self):
        temp = docx2txt.process('Bhargavi Angular JS Developer.docx')
        text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
        return ' '.join(text)
    
    def fetch_doc_file(self):
        pass
    


           