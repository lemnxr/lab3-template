from enum import Enum

from schemas.response import ErrorResponse, ValidationErrorResponse


class ResponseClassReservation(Enum):
    GetAll = {
        "description": "All Reservations",
    }
    GetByID = {
        "description": "Reservation by ID",
    }
    Add = {
        "description": "Add new Reservation",
        "headers": {
            "Location": {
                "description": "Path to new Reservation",
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
        "description": "Reservation by ID was deleted",
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }
    Patch = {
        "description": "Reservation by ID was updated",
    }


    InvalidData = {
        "model": ValidationErrorResponse,
        "description": "Invalid data",
    }
    NotFound = {
        "model": ErrorResponse,
        "description": "Not found Reservation by ID",
    }
    Conflict = {
        "model": ErrorResponse,
        "description": "Conflict",
    }

class ResponseClassHotel(Enum):
    GetAll = {
        "description": "All Hotels",
    }
    GetByID = {
        "description": "Hotel by ID",
    }
    Add = {
        "description": "Add new Hotel",
        "headers": {
            "Location": {
                "description": "Path to new Hotel",
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
        "description": "Hotel by ID was deleted",
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }
    Patch = {
        "description": "Hotel by ID was updated",
    }


    InvalidData = {
        "model": ValidationErrorResponse,
        "description": "Invalid data",
    }
    NotFound = {
        "model": ErrorResponse,
        "description": "Not found Hotel by ID",
    }
    Conflict = {
        "model": ErrorResponse,
        "description": "Conflict",
    }
    
class ResponseClassHealth(Enum):
    Health = {
        "description": "Reservation server is ready to work",
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }
    