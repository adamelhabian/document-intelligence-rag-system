from enum import Enum


class ResponseSignal(Enum):
    

    FILE_TYPE_NOT_SUPPORTED= "file_type_not_support"
    FILE_SIZE_EXCEEDED="file_size_exceeded"
    FILE_UPLOAD_SUCCESS="Success"
    FILE_UPLOAD_FAILED="file_upload_failed"
    PROCESSING_FAILED="processing_failed"
    PROCESSING_SUCCESS="processing_success"
    NO_FILES_ERROR="not found files"
    FILE_ID_ERROR="no_file_found_with_this_id"