from abc import ABC, abstractmethod

import langchain_community.llms as llms                                         # type: ignore
from langchain_openai import ChatOpenAI, AzureChatOpenAI                        # type: ignore

class ILLM(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def build_instance(self):
        pass

    @abstractmethod
    def get_instance(self):
        pass

class OpenAI(ILLM):

    def __init__(self, model_name: str, temperature: float) -> None:
        self.instance: ILLM = None
        self.model_name = model_name
        self.temperature = temperature if temperature else 0

    def build_instance(self):
        self.instance: ILLM = ChatOpenAI(
            model_kwargs={
                "deployment": self.model_name
            },
            temperature=self.temperature
        )

    def get_instance(self) -> ChatOpenAI:
        if self.instance is None:
            self.build_instance()
        return self.instance

class Azure(ILLM):

    def __init__(self, model_name: str, temperature: float) -> None:
        self.instance: ILLM = None
        self.model_name = model_name
        self.temperature = temperature if temperature else 0

    def build_instance(self):
        self.instance: ILLM = AzureChatOpenAI(
            deployment_name=self.model_name,
            temperature=self.temperature
        )

    def get_instance(self) -> AzureChatOpenAI:
        if self.instance is None:
            self.build_instance()
        return self.instance

class Ollama(ILLM):
    
    def __init__(self, model_name: str, temperature: float) -> None:
        self.instance: ILLM = None
        self.model_name = model_name
        self.temperature = temperature if temperature else 0

    def build_instance(self) -> None:
        self.instance: ILLM = llms.Ollama(
            model=self.model_name,
            temperature=self.temperature
        )

    def get_instance(self) -> llms.Ollama:
        if self.instance is None:
            self.build_instance()
        return self.instance
    
    # def invoke(self, prompt: str):
    #     print('class: Ollama - method: invoke - prompt:', prompt)
    #     return self.instance.call(prompt)

class LLMBuilder:

    def __init__(self, 
                 llm_type: str, 
                 model_name: str, 
                 temperature: float) -> None:
        self.instance: ILLM = None
        self.llm_type: str = llm_type
        self.model_name: str = model_name
        self.temperature: float = temperature if temperature else 0

    def build_instance(self) -> None:
        instance: ILLM = None
        if self.llm_type == 'ollama':
            instance = Ollama(
                model_name=self.model_name,
                temperature=self.temperature
            )
        elif self.llm_type == 'azure':
            instance = Azure(
                model_name=self.model_name,
                temperature=self.temperature
            )
        elif self.llm_type == 'openai':
            instance = OpenAI(
                model_name=self.model_name,
                temperature=self.temperature
            )
        self.instance = instance

    def get_instance(self) -> ILLM:
        if self.instance is None:
            self.build_instance()
        return self.instance.get_instance()
