import os
import streamlit as st 
import requests
import openai
from docx import Document
import PyPDF2
from bs4 import BeautifulSoup

openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")


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

def translate_to_english(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates text to English."},
            {"role": "user", "content": f"Translate the following text to English:\n\n{text}"}
        ]
    )
    return response.choices[0].message['content']

def answer_question(context, question):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the given context. Always answer in English."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message['content']

def main():
    st.title("Page Summarizer")

    if 'text' not in st.session_state:
        st.session_state.text = ""
    if 'summary' not in st.session_state:
        st.session_state.summary = ""

    input_type = st.radio("Choose input type:", ["URL", "Document Upload"])

    if input_type == "URL":
        url = st.text_input("Enter a URL:")
        if url and st.button("Summarize"):
            with st.spinner("Extracting and summarizing text..."):
                st.session_state.text = extract_text_from_url(url)
                st.session_state.text = translate_to_english(st.session_state.text)
                st.session_state.summary = summarize_text(st.session_state.text)
            print("Extracted text:", st.session_state.text)  # Print to terminal
    else:
        uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx", "pdf"])
        if uploaded_file and st.button("Summarize"):
            with st.spinner("Extracting and summarizing text..."):
                if uploaded_file.type == "text/plain":
                    st.session_state.text = uploaded_file.read().decode()
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    st.session_state.text = extract_text_from_docx(uploaded_file)
                elif uploaded_file.type == "application/pdf":
                    st.session_state.text = extract_text_from_pdf(uploaded_file)
                st.session_state.text = translate_to_english(st.session_state.text)
                st.session_state.summary = summarize_text(st.session_state.text)
            print("Extracted text:", st.session_state.text)  # Print to terminal

    if st.session_state.summary:
        st.subheader("Summary")
        st.write(st.session_state.summary)

    st.subheader("Ask a question")
    question = st.text_input("Enter your question:")
    if question and st.button("Get Answer"):
        with st.spinner("Generating answer..."):
            answer = answer_question(st.session_state.text, question)
        st.write("Answer:", answer)

if __name__ == "__main__":
    main()
