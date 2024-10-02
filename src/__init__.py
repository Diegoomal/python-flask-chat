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

def init_llm_vision():
    illm: ILLM = LLMBuilder(llm_type='ollama', model_name='llava', temperature=0)
    return illm.get_instance()
illm_vision = init_llm_vision()

from .core.agent import AgentBuilder
def init_agent():
    illm: ILLM = LLMBuilder(llm_type='ollama', model_name='llama3', temperature=0)
    agent = AgentBuilder(agent_type='tool', illm=illm.get_instance())
    return agent.get_agent()
agent = init_agent()
