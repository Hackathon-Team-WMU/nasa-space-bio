add flask and langchain folders in here :)

# Structure

Data folder consists of the primary csv datasource

LLM folder consists of the langchain config and the rag

Scripts folder is for the common data fetch scripts

# RAG pipeline

- First run the fetchData script under the scripts directory (This scrapes the web page for you and stores it under data/fetched_texts)
- Once that is done to generate the embeddings run the llm/embeddings_builder script this will generate the vector DB
- Mind that the previous step uses a local run model so might take up quite some resources and will take its sweet time depending on device
- Now you can import the query method from the llm_rag.py and pass in the query message!
