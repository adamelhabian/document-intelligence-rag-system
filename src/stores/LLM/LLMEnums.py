from enum import Enum


class LLMEnums(Enum):

    OPENAI="OPENAI"
    COHERE="COHERE"
    GEMINI="GEMINI"

# Different providers can have different API formats and conventions
class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CoHereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"

    DOCUMENT = "search_document"
    QUERY = "search_query"

class GeminiEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "model"


# in genral not for cohere
class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"