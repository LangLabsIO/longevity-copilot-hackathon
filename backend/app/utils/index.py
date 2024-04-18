import logging
import os
from scipy.spatial.distance import cosine
from llama_index import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    ServiceContext,
)
from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.together import TogetherEmbedding

# Replace 'your_api_key' with the actual API key obtained from Together AI
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY", "your_api_key")

STORAGE_DIR = "./storage"  # directory to cache the generated index
DATA_DIR = "./data"  # directory containing the documents to index

# Setup LLM and Embedding Model from Together AI
service_context = ServiceContext.from_defaults(
    llm=TogetherLLM(api_key=TOGETHER_API_KEY, model="mistralai/Mixtral-8x7B-Instruct-v0.1"),
    embed_model=TogetherEmbedding(api_key=TOGETHER_API_KEY, model_name="togethercomputer/m2-bert-80M-8k-retrieval")
)

def get_index():
    logger = logging.getLogger("uvicorn")
    if not os.path.exists(STORAGE_DIR):
        logger.info("Creating new index")
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        index.storage_context.persist(STORAGE_DIR)
        logger.info(f"Finished creating new index. Stored in {STORAGE_DIR}")
    else:
        logger.info(f"Loading index from {STORAGE_DIR}...")
        storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
        index = load_index_from_storage(storage_context, service_context=service_context)
        logger.info(f"Finished loading index from {STORAGE_DIR}")
    return index

def get_relevant_response(query):
    index = get_index()
    query_embedding = service_context.embed_model.get_text_embedding(query)
    # Retrieve document embeddings and compute similarity
    similarities = [(doc, 1 - cosine(query_embedding, service_context.embed_model.get_text_embedding(doc.content)))
                    for doc in index.documents]
    # Sort by similarity
    most_relevant_document = max(similarities, key=lambda x: x[1])[0]
    prompt = f"You are an longevity assistant that helps the user gain relevent info about longevity. They will ask a question and you will recieve context. If they are just greeting you then say hello back instead.Context: {most_relevant_document.content}\nQuestion: {query}\nAnswer:"
    response = service_context.llm.complete(prompt)
    return response
