from fastapi import FastAPI , APIRouter, Depends ,UploadFile,status
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController
import aiofiles
from models  import ResponseSignal
import logging

logger=logging.getLogger('uvicorn.error')

data_router=APIRouter(
    # every route registered through this router
    prefix='/api/v1/data',
    # groups these endpoints under api_v1 in the Swagger documentation
    tags={"api_v1"}
)


@data_router.post('/upload/{project_id}')
async def upload_data(project_id:str,file:UploadFile,app_settings:Settings=Depends(get_settings)):

    data_controller=DataController()

    # validate the file properties
    is_valid,result_signal=data_controller.validate_uploaded_file(file=file)



    if not is_valid:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "signal":result_signal
        }
        )
# behind the sence the file stored on temp file once it completed it put in the target folder (not efficeint way)
# the efficient way file cut to chunks once each chunk complete put in the target folder

    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path=data_controller.generate_unique_filename(org_file_name=file.filename,project_id=project_id)

    try:
        async with aiofiles.open(file_path,'wb') as f :
            while chunk:= await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"error while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(
        content={
            "signal":ResponseSignal.FILE_UPLOAD_SUCCESS.value
        }
    )
        



