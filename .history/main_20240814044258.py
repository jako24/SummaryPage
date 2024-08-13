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

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
        ]
    )
    return response.choices[0].message['content']

def main(): 
    st.title("Page Sumamrizer")
    
    input_type = st.radio('Choose input type', ["URL", "Document Upload"])
    
    if input_type == "URL":
        url = st.text_input("Enter a URL:")
        if url:
            text = extract_text_from_url(url)
    else:
        uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx", "pdf"])
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                text = uploaded_file.read().decode()
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = extract_text_from_docx(uploaded_file)
            elif uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)

    if 'text' in locals():
        if st.button("Summarize"):
            summary = summarize_text(text)
            st.subheader("Summary")
            st.write(summary)

            st.subheader("Ask a question")
            question = st.text_input("Enter your question:")
            if question:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions based on the given context."},
                        {"role": "user", "content": f"Context: {text}\n\nQuestion: {question}"}
                    ]
                )
                st.write("Answer:", response.choices[0].message['content'])

if __name__ == "__main__":
    main()
    
    
    

if __name__ == "__main__":
    main()