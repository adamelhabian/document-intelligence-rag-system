
# ABC class is used to build an Abstract Class in Python, which can also define an interface-like contract.
from abc import ABC,abstractmethod

class LLMInterface(ABC):

    @abstractmethod # to inforce any class inherit the interface to implement abstract method
    def set_generation_model(self,model_id:str):
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass


    # temperature for example [0,1] if num close to 0 creativity is small 
    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: str = None):
        pass

    # change prompt to specific format to different between prompts types 
    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass

