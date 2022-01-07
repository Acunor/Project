import spacy
from spacy.matcher import Matcher
import re
import nltk
import re
import spacy
from nltk.corpus import stopwords

import sys
sys.path.append(r"C:\Users\admin\Projects\ResumeParser\model")
from acunor_rp_employee_details import EmployeeDetails

class Parser(object):
         
    def __init__(self):
        pass
    
    def parse_text(self,text):
        name=self.extract_name(text)
        mobile=self.extract_mobile_number(text)
        email=self.extract_email(text)
        skills=self.extract_skills(text)
        education=self.extract_education(text)
        #print(name,mobile,email,skills,education) 
        employeedetails=EmployeeDetails(name,mobile,email,skills,education)         
        return employeedetails
        
    
    def extract_name(self,name):   
        nlp = spacy.load('en_core_web_sm') # load pre-trained model
        matcher = Matcher(nlp.vocab)       # initialize matcher with a vocab
        nlp_text = nlp(name)
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]  # First name and Last name are always Proper Nouns
        matcher.add('NAME',[pattern])       
        matches = matcher(nlp_text)
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text
        
    def extract_mobile_number(self,mobile):
        phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), mobile)
        if phone:
            number = ''.join(phone[0])
            if len(number) > 10:
                return '+' + number
            else:
                return number
            
    def extract_email(self,email):
        email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None
       
    def extract_skills(self,skills):
        SKILLS_DB = ['linq','sql server','agile','scrun','waterfall','jams','azure','sql','jira','spotlight']
        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(skills)
        # remove the stop words
        filtered_tokens = [w for w in word_tokens if w not in stop_words]
        # remove the punctuation
        filtered_tokens = [w for w in word_tokens if w.isalpha()]
        # generate bigrams and trigrams (such as artificial intelligence)
        bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
        # we create a set to keep the results in.
        found_skills = set()
        # we search for each token in our skills database
        for token in filtered_tokens:
            if token.lower() in SKILLS_DB:
                found_skills.add(token)
        # we search for each bigram and trigram in our skills database
        for ngram in bigrams_trigrams:
            if ngram.lower() in SKILLS_DB:
                found_skills.add(ngram)
        return found_skills
    
    def extract_education(self,edu):
        nlp = spacy.load('en_core_web_sm')  # load pre-trained model
        STOPWORDS = set(stopwords.words('english'))  # Grad all general stop words
        EDUCATION = ['BE','B.E.','B.E','BS','B.S','ME','M.E','M.E.','MS','M.S','BTECH','B.TECH','M.TECH','MTECH','SSC','HSC','CBSE','ICSE','X','XII']
        nlp_text = nlp(edu)
        # Sentence Tokenizer
        #nlp_text = [sent.string.strip() for sent in nlp_text.sents]
        nlp_text = [sent.text.strip() for sent in nlp_text.sents]
        edu = {}
        # Extract education degree
        for index, text in enumerate(nlp_text):
            for tex in text.split():
                # Replace all special symbols
                tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                if tex.upper() in EDUCATION and tex not in STOPWORDS:
                    edu[tex] = text + nlp_text[index + 1]
        # Extract year
        education = []
        for key in edu.keys():
            year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
            if year:
                education.append((key, ''.join(year[0])))
            else:
                education.append(key)
        return education
    