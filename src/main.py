from fastapi import FastAPI
from dotenv import load_dotenv
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient # class that allows Python to connect to MongoDB asynchronously
from helpers.config import get_settings



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

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()



app.include_router(base.base_router)
app.include_router(data.data_router)




