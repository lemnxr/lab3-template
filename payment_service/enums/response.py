from enum import Enum

from schemas.response import ErrorResponse, ValidationErrorResponse


class ResponseClassPayment(Enum):
    GetAll = {
        "description": "All Payments",
    }
    GetByID = {
        "description": "Payment by ID",
    }
    Add = {
        "description": "Add new Payment",
        "headers": {
            "Location": {
                "description": "Path to new Payment",
                "style": "simple",
                "schema": {
                    "type": "string"
                }
            }
        },
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }
    Delete = {
        "description": "Payment by ID was deleted",
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }
    Patch = {
        "description": "Payment by ID was updated",
    }


    InvalidData = {
        "model": ValidationErrorResponse,
        "description": "Invalid data",
    }
    NotFound = {
        "model": ErrorResponse,
        "description": "Not found Payment by ID",
    }
    Conflict = {
        "model": ErrorResponse,
        "description": "Conflict",
    }
    
class ResponseClassHealth(Enum):
    Health = {
        "description": "Payment server is ready to work",
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }
    