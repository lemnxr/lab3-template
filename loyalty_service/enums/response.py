from enum import Enum

from schemas.response import ErrorResponse, ValidationErrorResponse


class ResponseClassLoyalty(Enum):
    GetAll = {
        "description": "All Loyaltys",
    }
    GetByID = {
        "description": "Loyalty by ID",
    }
    GetByUsername = {
        "description": "Loyalty by Username",
    }
    Add = {
        "description": "Add new Loyalty",
        "headers": {
            "Location": {
                "description": "Path to new Loyalty",
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
        "description": "Loyalty by ID was deleted",
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }
    Patch = {
        "description": "Loyalty by ID was updated",
    }


    InvalidData = {
        "model": ValidationErrorResponse,
        "description": "Invalid data",
    }
    NotFound = {
        "model": ErrorResponse,
        "description": "Not found Loyalty by ID",
    }
    Conflict = {
        "model": ErrorResponse,
        "description": "Conflict",
    }
    
class ResponseClassHealth(Enum):
    Health = {
        "description": "Loyalty server is ready to work",
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }
    