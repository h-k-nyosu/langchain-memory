from app.utils.extract_web_content import extract_web_content
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings

def process_urls(urls: list, delay=1):
    extracted_texts = []

    for url in urls:
        text = extract_web_content(url, delay)
        extracted_texts.append(text)

    return extracted_texts

def process_urls_and_generate_embeddings(urls: list, delay=1):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=0)
    extracted_texts = process_urls(urls, delay)
    split_texts = []
    for text in extracted_texts:
        split_texts.extend(text_splitter.split_text(text))
    embeddings = OpenAIEmbeddings()
    return embeddings, split_texts
