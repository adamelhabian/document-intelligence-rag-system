from fastapi import FastAPI , APIRouter, Depends
from dotenv import load_dotenv
import os
from helpers.config import get_settings,Settings

# Reads variables from your .env file and loads them into the process environment.
# load_dotenv(".env")

# group related endpoints together

base_router=APIRouter(
    # every route registered through this router
    prefix='/api/v1',
    # groups these endpoints under api_v1 in the Swagger documentation
    tags={"api_v1"}
)


@base_router.get('/')
async def welcome(app_settings:Settings=Depends(get_settings)):
    # use os to retreive enviroment vaiables
    # app_settings=get_settings()
    app_name=app_settings.APP_NAME
    app_version=app_settings.APP_VERSION
    return { "app name":app_name,
            "app version":app_version}