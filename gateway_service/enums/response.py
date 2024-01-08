from enum import Enum

from schemas.response import ErrorResponse, ValidationErrorResponse


class ResponseClassGateway(Enum):
    InvalidData = {
        "model": ValidationErrorResponse,
        "description": "Ошибка валидации данных"
    }

    GetAllHotels = {
        "description": "Список отелей",
    }

    GetUserInfo = {
        "description": "Полная информация о пользователе",
    }

    GetUserReservations = {
        "description": "Информация по всем бронированиям пользователя"
    }

    ReserveHotel = {
        "description": "Информация о бронировании отеля"
    }

    HotelNotFound = {
        "model": ErrorResponse,
        "description": "Отель не найден"
    }

    GetReservationInfo = {
        "description": "Информация по конкретному билету"
    }

    ReservationNotFound = {
        "model": ErrorResponse,
        "description": "Бронирование не найдено"
    }

    ReservationCancel = {
        "description": "Бронирование отменено",
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }

    GetLoyalty = {
        "description": "Информация о статусе в программе лояльности"
    }
