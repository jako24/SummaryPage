import os
import streamlit as st 
import requests
import openai
from docx import Document
import PyPDF2
from bs4 import BeautifulSoup

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(url):
    doc = Document(url)
    return '\n'.join([para for para in doc.paragraphs])

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

def main(): 
    st.title("Page Sumamrizer")
    
    input_type = st.radio('Choose input type', ["URL", "Document Upload"])
    
    
    

if __name__ == "__main__":
    main()