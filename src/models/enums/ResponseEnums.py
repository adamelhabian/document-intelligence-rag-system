from enum import Enum


class ResponseSignal(Enum):
    

    FILE_TYPE_NOT_SUPPORTED= "file_type_not_support"
    FILE_SIZE_EXCEEDED="file_size_exceeded"
    FILE_UPLOAD_SUCCESS="Success"
    FILE_UPLOAD_FAILED="file_upload_failed"