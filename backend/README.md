# Structure

Data folder consists of the primary csv datasource

LLM folder consists of the langchain config and the rag

Scripts folder is for the common data fetch scripts

# RAG pipeline Installation instructions

- Install Virtual Environment for python

Linux:

```bash
sudo apt install python3-venv -y        # Ubuntu/Debian

sudo dnf install python3-venv -y        # Fedora
```

Windows:

```bash
pip install virtualenv
```

- Activate the virtual environment

Linux:

```bash
python -m venv your_env_name

or

python3 -m venv your_env_name

source your_env_name/bin/activate
```

Windows:

```bash
python -m venv your_env_name

# Command Prompt
your_env_name\Scripts\activate.bat

# Powershell
your_env_name\Scripts\Activate.ps1
```

- First we install all the dependencies required for the pipeline
```bash
pip install -r requirements.txt

or

pip3 install -r requirements.txt
```

- Please make sure you have the 'NEBIUS_API_KEY' setup in the .env file in the backend folder. Use .env.example for reference

- First run the fetchData script under the scripts directory (This scrapes the web page for you and stores it under data/fetched_texts)

```bash
python scripts/fetchData.py

or

python3 scripts/fetchData.py
```

- Once that is done to generate the embeddings run the llm/embeddings_builder script this will generate the vector DB stored under the vector_store directory (created upon the run)

```bash
python llm/embeddings_builder.py

or

python3 llm/embeddings_builder.py
```

- Mind that the previous step uses a local run model so might take up quite some resources and will take its sweet time depending on device

- <b>The embeddings dont need to be always run it needs only when its a first time run or there is new data to ingest</b>

- Now you can import the query method from the llm_rag.py and pass in the query message!

```python
from llm.llm_rag import query

# Use the query call
query("Describe the effects of microgravity on plant growth")
```
