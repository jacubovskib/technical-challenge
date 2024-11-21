from src.domain.exceptions import BadRequestException, NotFoundException, IntegrityException
from src.infra.api.presentation.http_types.http_response import HttpResponse
from sqlite3 import IntegrityError
import re


class HandleException:

    @staticmethod
    def handle(exception: Exception) -> HttpResponse:
        if isinstance(exception, (NotFoundException, BadRequestException, IntegrityException)):
            return HandleException.__handle_domain_exception(exception)

        if isinstance(exception, IntegrityError) and "UNIQUE constraint failed" in str(exception):
            return HandleException.__handle_sqlite_integrity_error(exception)

        return HandleException.__handle_generic_error(exception)

    @staticmethod
    def __handle_domain_exception(exception: Exception) -> HttpResponse:
        return HttpResponse(a_status_code=exception.status_code, a_body={
            "title": exception.name,
            "details": exception.message
        })

    @staticmethod
    def __handle_sqlite_integrity_error(exception: IntegrityError) -> HttpResponse:
        field_match = re.search(r'UNIQUE constraint failed: \w+\.(\w+)', str(exception))
        field_name = field_match.group(1) if field_match else 'field'
        raise IntegrityException(f"This {field_name} already exists in the system")

    @staticmethod
    def __handle_generic_error(exception: Exception) -> HttpResponse:
        return HttpResponse(a_status_code=500, a_body={
            "title": "Server Error",
            "details": str(exception)
        })
