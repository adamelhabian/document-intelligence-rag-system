from ..LLMinterface import LLMInterface
from ..LLMEnums import LLMEnums
from openai import OpenAI
import logging
from ..LLMEnums import OpenAIEnums

# The complete text generation flow                                      
# Create OpenAIProvider object
#           |
#           v
#        __init__()
#           |
#           v
# set_generation_model(model_id)
#           |
#           v
# generate_text(prompt, chat_history)
#           |
#           v
# Validate client and model
#           |
#           v
# Set generation parameters
#           |
#           v
# construct_prompt(prompt, role)
#           |
#           v
# process_text(prompt)
#           |
#           v
# Construct user message
#           |
#           v
# Append message to chat_history
#           |
#           v
# Call OpenAI Chat Completions API
#           |
#           v
# Validate response
#           |
#           v
# Return generated answer

# Embedding flow
# set_embedding_model()
#           |
#           v
#       embed_text()
#           |
#           v
# Validate client and model
#           |
#           v
# Call Embeddings API
#           |
#           v
# Receive embedding vector
#           |
#           v
# Return vector


class OpenAIProvider(LLMInterface):
    # api key for connection
    # api url if i deal with other provider support rules of openai provider
    def __init__(self, api_key: str, api_url: str=None,
                # input max : safe line if i by fault send all document i will consume all tokens i have
                    default_input_max_characters: int=1000,
                    default_generation_max_output_tokens: int=1000,
                    default_generation_temperature: float=0.1):
        
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key = self.api_key,
            api_url = self.api_url
        )

        # log messages help you understand what your application is doing while it runs
        # __name__ -> name of this file (OpenAiProvider.py)
        # They are especially useful for debugging errors and monitoring your RAG pipeline
        self.logger = logging.getLogger(__name__)



    # generation model can be changed during run time so i didn't but it in constracor
    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id




    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size




    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        # means this function doesn't have implementation 
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for OpenAI was not set")
            return None
        max_output_tokens = max_output_tokens   if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt,role=OpenAIEnums.USER.value)
        )
        response = self.client.chat.completions.create(
            model = self.generation_model_id,
            messages = chat_history,
            max_tokens = max_output_tokens,
            temperature = temperature
        )

        if not response or not response.choices or len(response.choices)==0 or not response.choices[0].message:
            self.logger.error("Error while generating text with OpenAI")
            return None
        return response.choices[0].message["content"]




        

    # third party : external partner (provider)  advice : focus on validation 
    def embed_text(self, text: str, document_type: str = None):
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None

        response=self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text
        )

        if not response or not response.data or len(response.data)==0 or not response.data[0].embedding:
            self.logger.error("Error while generating text with OpenAI")
            return None

        return response.data[0].embedding

    # i don't put it in interface because it's not mandatory for all llms models
    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    

    def construct_prompt(self, prompt: str, role: str):
        # system Sets the assistant's behavior and rules.
        # user	Provides questions or information.
        # assistant	Contains the assistant's previous responses or generated answers.
        return {
            "role": role,
            "content": self.process_text(prompt)
        }
    
        

    

        
