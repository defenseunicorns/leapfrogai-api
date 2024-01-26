import requests
from bs4 import BeautifulSoup
from io import BytesIO
from llama_index import (
    Document,
    VectorStoreIndex,
    StorageContext,
)

from pypdf import PdfReader

from utils import get_model_config

from vectordb.vector_stores import (
    ChromaDB,
    LLamaIndex,
    Weaviate,
)

from utils.logging import log, now, get_elapsed

from fastapi import UploadFile


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def get_filename(url):
    return url.split('/')[-1]


def process_pdf(url):
    start = now()
    file = get_filename(url)
    log(f'processing file: {get_filename(url)}')
    r = requests.get(url)
    text = extract_text_from_pdf(BytesIO(r.content))
    docs = [Document(text=text)]
    vdbs = get_model_config().rag.vector_stores
    vdbs_processed = LLamaIndex.vectorize_docs(docs, vdbs)
    elapsed = get_elapsed(start)
    return {'result': f'PDF {file} processed successfully', 'vdbs_processed': vdbs_processed, 'elapsed': elapsed}


def process_text(url):
    start = now()
    file = get_filename(url)
    log(f'processing file: {get_filename(url)}')
    r = requests.get(url)
    docs = [Document(text=r.content)]
    vdbs = get_model_config().rag.vector_stores
    vdbs_processed = LLamaIndex.vectorize_docs(docs, vdbs)
    elapsed = get_elapsed(start)
    return {'result': f'file {file} processed successfully', 'vdbs_processed': vdbs_processed, 'elapsed': elapsed}


def process_file(url, filetype):
    if filetype == 'pdf':
        return process_pdf(url)
    elif filetype == 'txt':
        return process_text(url)


def process_query(prompt):
    return LLamaIndex.process_query(prompt)


def fetch_extension(url):
    try:
        return url.split('.')[-1].lower()
    except Exception as e:
        log(e)


def process_files_from_urls(urls):
    start = now()
    filecount = len(urls)
    log(f'i will start processing {filecount} files')
    docs = []
    for url in urls:
        extension = fetch_extension(url)
        r = requests.get(url)

        if extension not in get_model_config().rag.file_extensions:
            log(f'invalid extension: {extension}')                        
            text = None
        elif extension in ('pdf'):
            text = extract_text_from_pdf(BytesIO(r.content))
        elif extension in ('txt'):
            text = r.content

        if text:
            docs.append(Document(text=text))

    if len(docs) > 0:
        vdbs = get_model_config().rag.vector_stores
        vdbs_processed = LLamaIndex.vectorize_docs(docs, vdbs)   
        files_processed = len(docs)
    else:
        vdbs_processed = None
        files_processed = None
        
    elapsed = get_elapsed(start) 
    return {'files_processed': files_processed, 'vdbs_processed': vdbs_processed, 'elapsed': elapsed}

def process_file_attachments(files: list[UploadFile]):
    start = now()

    docs = []
    for file in files:
        extension = fetch_extension(file.filename)
        file_bytes = file.file.read()
        if extension in ('pdf'):
            text = extract_text_from_pdf(BytesIO(file_bytes))
        elif extension in ('txt'):
            text = file_bytes
        else:
            log(f'invalid extension: {extension}')
            text = None
            docs = []

        docs.append(Document(text=text))
    
    vdbs = get_model_config().rag.vector_stores
    vdbs_processed = LLamaIndex.vectorize_docs(docs, vdbs)   
    files_processed = len(docs)
    elapsed = get_elapsed(start) 
    return {'files_processed': files_processed, 'vdbs_processed': vdbs_processed, 'elapsed': elapsed}


def process_files_by_extension_from_urls(payload):
    start = now()
    urls = payload.urls
    extensions = payload.extensions
    url_base = payload.url_base
    limit = payload.limit

    filecount = 0
    for url in urls[:1]:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features="html.parser")
        a_tags = soup.find_all('a')
        # links = [tag.get('href') for tag in a_tags if fetch_extension(tag.get('href')) in extensions]
        links = [tag.get('href') for tag in a_tags if fetch_extension(tag.get('href')) in extensions]
        links_subset = links[:limit]
        urls = [f'{url_base}/{link}' for link in links_subset]
        log(urls)
        filecount = len(urls)
        log(urls)
        process_files_from_urls(urls)

    elapsed = get_elapsed(start)
    return {'files_processed': filecount, 'elapsed': elapsed}
