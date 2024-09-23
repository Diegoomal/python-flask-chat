import os
from datetime import timedelta

from dotenv import load_dotenv                                                  # type: ignore
load_dotenv()

from flask import Flask                                                         # type: ignore
def create_app():
    app = Flask(__name__)
    return app
app = create_app()


from .core.llm import ILLM, LLMBuilder
def init_llm():
    illm: ILLM = LLMBuilder(llm_type='ollama', model_name='llama3', temperature=0)
    return illm.get_instance()
illm = init_llm()