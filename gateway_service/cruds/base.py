import inspect
from fastapi import status

from exceptions.exceptions import InvalidRequestException, ServiceUnavailableException


class BaseCRUD():
    def _check_status_code(self, status_code: int, service_name: int):
        method = inspect.stack()[1][3]
        method = " ".join(method.split('_')).title()

        if status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
            raise ServiceUnavailableException(
                message=f"{service_name} unavailable"
            )
        elif status_code >= 400:
            raise InvalidRequestException(
                prefix=method,
                status_code=status_code
            )
        