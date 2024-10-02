import json
from datetime import datetime
from abc import ABC, abstractmethod

# from duckduckgo_search import ddg                                             # type: ignore
from langchain.llms import OpenAI, AzureOpenAI                                  # type: ignore
from langchain.agents import initialize_agent, Tool                             # type: ignore
# from langchain.tools import PythonCalculator, SerpAPIWrapper, DuckDuckGoSearchRun # type: ignore
from langchain.memory import ConversationBufferMemory                           # type: ignore

from .llm import ILLM, LLMBuilder


def get_current_time(_: str) -> str:
    return datetime.now().strftime("%H:%M:%S")

def get_today_date(_: str) -> str:
        return str(datetime.now().date())

def sum_two_numbers(numbers: str) -> str:
    try:
        num1, num2 = map(float, numbers.split(","))
        result = num1 + num2
        return str(result)
    except ValueError:
        return "Invalid input, please provide two numbers separated by a comma."

def get_columns_descriptions(query: str) -> str:
    if query == 'clientes':
        columns_description = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "nome": "TEXT NOT NULL",
            "telefone": "TEXT",
            "endereco": "TEXT",
        }
    elif query == 'produtos':
        columns_description = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "nome": "TEXT NOT NULL",
            "preco": "REAL NOT NULL",
        }
    elif query == 'vendas':
        columns_description = {
            "id": "primary key of the database and unique identifier in the database. ",
            "cliente_id": "foreign key client",
            "produto_id": "foreign key product",
        }
    else:
        columns_description = { "message": "Option not implemented yet." }
    return json.dumps(columns_description)


class IAgent(ABC):

    @abstractmethod
    def __init__(self, llm_instance: ILLM):
        pass

    @abstractmethod
    def get_agent(self):
        pass

class ToolAgent(IAgent):

    def __init__(self, llm_instance: ILLM):
        self.llm_instance = llm_instance
        self.agent = None
        self.tools = [
            Tool(
                name="get_current_time",
                func=get_current_time,
                description="return hour now"
            ),
            Tool(
                name="get_today_date",
                func=get_today_date,
                description="Useful to get the date of today."
            ),
            Tool(
                name="sum_two_numbers",
                func=sum_two_numbers,
                description="sum two numbers, provide them separated by a comma (e.g., '5,3')"
            ),
            Tool(
                func=get_columns_descriptions,
                name="get_columns_descriptions",
                description="""
                    Useful to get the description of the columns in the table selected by user query.
                    Require an string as an argument with the name of table (can be: 'clientes', 'produtos' or 'vendas').
                """,
            )
        ]

    def get_agent(self):
        if self.agent is None:

            CUSTOM_SUFFIX = """
                Begin!

                Relevant pieces of previous conversation:
                {history}
                (Note: Only reference this information if it is relevant to the current query.)

                Question: {input}

                Thought Process: 
                It is imperative that I do not fabricate information not present in the database 
                or engage in hallucination; maintaining trustworthiness is crucial.
                Verify if the tools 'get_today_date', 'get_columns_descriptions' can help you.
                My final response must be delivered in the language of the user's query.

                {agent_scratchpad}
            """

            memory = ConversationBufferMemory(memory_key="history", input_key="input")

            self.agent = initialize_agent(
                tools=self.tools,
                llm=self.llm_instance,
                agent_type="zero-shot-react-description",
                verbose=True,
                max_iterations=100,
                handle_parsing_errors=True,
                suffix=CUSTOM_SUFFIX,
                input_variables=['history', 'input'],
                agent_executor_kwargs={ "memory": memory },
            )

        return self.agent

class AgentBuilder:
    
    def __init__(self, agent_type: str, illm: ILLM):
        self.llm_instance = illm
        self.agent_type = agent_type
        self.agent = None

    def build_agent(self):
        if self.agent_type == 'tool':
            self.agent = ToolAgent(self.llm_instance)
        # Outras implementações de agentes podem ser adicionadas aqui
        return self.agent

    def get_agent(self):
        if self.agent is None:
            self.build_agent()
        return self.agent.get_agent()
