from fastapi import FastAPI
from dotenv import load_dotenv
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient # class that allows Python to connect to MongoDB asynchronously
from helpers.config import get_settings
from stores.LLM.LLMProviderFactory import LLMProviderFactory



app=FastAPI()


# connects a FastAPI application to MongoDB when the application starts and closes
# An event is something that happens during the application's lifecycle.

@app.on_event("startup")
# FastAPI initializes the application and runs its startup handlers before serving requests
async def startup_db_client():
    settings=get_settings()
    # creates a client object that your Python application can use to communicate with MongoDB asynchronously
    app.mongo_conn=AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client=app.mongo_conn[settings.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(settings)

    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)


    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()



app.include_router(base.base_router)
app.include_router(data.data_router)




