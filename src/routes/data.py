from fastapi import FastAPI , APIRouter, Depends ,UploadFile,status
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController
import aiofiles
from models  import ResponseSignal
import logging
from schemes import ProcessRequest

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
    file_path,file_id=data_controller.generate_unique_filepath(org_file_name=file.filename,project_id=project_id)

    try:
        async with aiofiles.open(file_path,'wb') as f :
            # The operator := is called the walrus operator 
            # assigns a value to a variable and evaluates to that value in the same expression
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
            "signal":ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id":file_id
        }
    )
        



@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,process_request:ProcessRequest):

    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    overlap_size=process_request.overlap_size
    processController=ProcessController(project_id=project_id)

    file_content=processController.get_file_content(file_id=file_id)
    file_chunks=processController.process_file_content(file_content=file_content,file_id=file_id,
                                                    chunk_size=chunk_size,overlap_size=overlap_size)

    if file_chunks is None or len(file_chunks)==0:

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    return file_chunks


    


