import logging
import os
from llama_index import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    ServiceContext,
)
from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.indices.managed.vectara import VectaraIndex

# Vectara Configuration
VECTARA_CORPUS_ID = os.getenv("VECTARA_CORPUS_ID")
VECTARA_CUSTOMER_ID = os.getenv("VECTARA_CUSTOMER_ID")
VECTARA_API_KEY = os.getenv("VECTARA_API_KEY")


# Replace 'your_api_key' with the actual API key obtained from Together AI
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY", "your_api_key")

STORAGE_DIR = "./storage"  # directory to cache the generated index
DATA_DIR = "./data"  # directory containing the documents to index

# Setup LLM and Embedding Model from Together AI
service_context = ServiceContext.from_defaults(
    llm=TogetherLLM(api_key=TOGETHER_API_KEY, model="meta-llama/Llama-2-70b-chat-hf"),
    embed_model=TogetherEmbedding(api_key=TOGETHER_API_KEY, model_name="togethercomputer/m2-bert-80M-8k-retrieval")
)

def get_index():
    logger = logging.getLogger("uvicorn")
    # check if storage already exists
    if not os.path.exists(STORAGE_DIR):
        logger.info("Creating new index")
        # load the documents and create the index
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        # store it for later
        index.storage_context.persist(STORAGE_DIR)
        logger.info(f"Finished creating new index. Stored in {STORAGE_DIR}")
    else:
        # load the existing index
        logger.info(f"Loading index from {STORAGE_DIR}...")
        storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
        index = load_index_from_storage(storage_context, service_context=service_context)
        logger.info(f"Finished loading index from {STORAGE_DIR}")
    return index

# Be sure to set your TOGETHER_API_KEY in your environment or directly in the code before running it.
