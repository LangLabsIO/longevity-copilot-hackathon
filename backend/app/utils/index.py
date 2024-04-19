import logging
import os
from llama_index.core import (
    # SimpleDirectoryReader,
    StorageContext,
    # VectorStoreIndex,
    load_index_from_storage,
    ServiceContext,
)
from llama_index.llms.together import TogetherLLM

from llama_index.indices.managed.vectara import VectaraIndex
from llama_index.indices.managed.vectara import VectaraAutoRetriever


from llama_index.embeddings.together import TogetherEmbedding

# from llama_index.indices.managed.vectara import VectaraIndex

# Vectara Configuration
VECTARA_CORPUS_ID = os.getenv("VECTARA_CORPUS_ID")
VECTARA_CUSTOMER_ID = os.getenv("VECTARA_CUSTOMER_ID")
VECTARA_API_KEY = os.getenv("VECTARA_API_KEY")


# Replace 'your_api_key' with the actual API key obtained from Together AI
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

STORAGE_DIR = "./storage"  # directory to cache the generated index
DATA_DIR = "./data"  # directory containing the documents to index

# Setup LLM and Embedding Model from Together AI
service_context = ServiceContext.from_defaults(
    llm=TogetherLLM(api_key=TOGETHER_API_KEY, model="meta-llama/Llama-2-70b-chat-hf"),
    embed_model=TogetherEmbedding(
        api_key=TOGETHER_API_KEY, model_name="togethercomputer/m2-bert-80M-8k-retrieval"
    ),
)


def get_index():
    logger = logging.getLogger("uvicorn")
    # check if storage already exists
    if not os.path.exists(STORAGE_DIR):
        # logger.info("Creating new index")
        # load the documents and create the index
        # documents = SimpleDirectoryReader(DATA_DIR).load_data()
        index = VectaraIndex()
        # store it for later
        # index.storage_context.persist(STORAGE_DIR)
        # logger.info(f"Finished creating new index. Stored in {STORAGE_DIR}")
    else:
        # load the existing index
        logger.info(f"Loading index from {STORAGE_DIR}...")
        # storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
        index = VectaraIndex()
        # index = VectaraIndex.as_chat_engine(
        # llm=TogetherLLM(
        # api_key=TOGETHER_API_KEY, model="meta-llama/Llama-2-70b-chat-hf"
        # ),
        # )
        logger.info(f"Finished loading index from {STORAGE_DIR}")
    return index


# def setup_vectara_retriever():
#     # Setup the LLM
#     llm = TogetherLLM(api_key=TOGETHER_API_KEY, model="meta-llama/Llama-2-70b-chat-hf")
#     # setup index
#     index = VectaraIndex(
#         vectara_api_key=VECTARA_API_KEY,
#         vectara_customer_id=VECTARA_CUSTOMER_ID,
#         vectara_corpus_id="2",
#     )

#     # Setup the retriever
#     retriever = VectaraAutoRetriever(
#         index=index,
#         llm=llm,
#         verbose=False,
#     )

#     return retriever

# Be sure to set your TOGETHER_API_KEY in your environment or directly in the code before running it.
