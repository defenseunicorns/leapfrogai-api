from backends.lfai.rag_utils import (
    process_file,
    process_query as do_query,
    process_files_by_extension_from_urls,
    process_file_attachments,
    process_files_from_urls,
)

from backends.lfai import router

from backends.lfai.types import (
    FilesByURLRequest,
    Query,
    URLRequest,
)

from fastapi import UploadFile

##########
# RAG/VECTORDB
##########

@router.put("/rag/ingest/files/from/urls")
def ingest_files_from_urls(payload: FilesByURLRequest):
    return process_files_from_urls(payload.urls)

@router.put("/rag/ingest/files/from/page_links")
def ingest_files_from_links(payload: URLRequest):
    return process_files_by_extension_from_urls(payload)

@router.post("/rag/ingest/files/from/form_attachments/")
async def ingest_files_from_form_attachments(files: list[UploadFile]):
    return process_file_attachments(files)

@router.put("/rag/query")
def process_query(q: Query):
    return do_query(q.query)