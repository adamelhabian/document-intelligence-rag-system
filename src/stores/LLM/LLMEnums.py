from enum import Enum


class LLMEnums(Enum):

    OPENAI="OPENAI"
    COHERE="COHERE"

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


# in genral not for cohere
class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"