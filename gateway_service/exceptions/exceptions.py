from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(
        self,
        prefix: str,
        headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{prefix}: объекта с таким id не существует", 
            headers=headers
        )

class ConflictException(HTTPException):
    def __init__(
        self,
        prefix: str,
        headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"{prefix}: объект с указанными атрибутами уже существует", 
            headers=headers
        )

class ServiceUnavailableException(HTTPException):
    def __init__(
        self,
        message: str,
        headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=message, 
            headers=headers
        )

class InvalidRequestException(HTTPException):
    def __init__(
        self,
        prefix: str,
        status_code: int,
        message: str | None = None,
        headers: dict[str, str] | None = None
    ) -> None:
        if message == None:
            message = f"Запрос вернул ошибку {status_code}"

        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY, 
            detail=f"{prefix}: {message}", 
            headers=headers
        )
        