from fastapi import HTTPException


def not_found() -> HTTPException:
    return HTTPException(404, 'Not found')


def bad_request(detail: str) -> HTTPException:
    return HTTPException(400, detail)


def unathorized() -> HTTPException:
    return HTTPException(401, 'Unathorized')
