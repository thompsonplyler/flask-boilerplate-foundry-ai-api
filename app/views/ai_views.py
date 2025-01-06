# Standard Library imports
import os
from pathlib import Path

# Core Flask imports
from flask import request, redirect, url_for, jsonify

# Third-party imports
from pydantic import ValidationError
from haystack import Pipeline, PredefinedPipeline
import urllib.request
from dotenv import dotenv_values

def get_dot_env():
    cwd = Path(os.getcwd())
    env_file = Path(cwd, ".flaskenv")
    values = dotenv_values(env_file)
    return values


def prompt_openai():
    env_values = get_dot_env()
    key = env_values["OPENAI_API_KEY"]
    os.environ["OPENAI_API_KEY"] = key
    query = request.json.get("query")
    print("Query:", query)

    urllib.request.urlretrieve("https://archive.org/stream/leonardodavinci00brocrich/leonardodavinci00brocrich_djvu.txt",
                           "davinci.txt")  

    indexing_pipeline =  Pipeline.from_template(PredefinedPipeline.INDEXING)
    indexing_pipeline.run(data={"sources": ["davinci.txt"]})

    rag_pipeline =  Pipeline.from_template(PredefinedPipeline.RAG)

    result = rag_pipeline.run(data={"prompt_builder": {"query":query}, "text_embedder": {"text": query}})
    reply = result["llm"]["replies"][0]
    return jsonify({"result": reply}), 200
