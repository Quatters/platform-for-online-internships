from fastapi import HTTPException


def not_found() -> HTTPException:
    return HTTPException(404, 'Not found.')


def bad_request(detail: str) -> HTTPException:
    return HTTPException(400, detail)


def unauthorized() -> HTTPException:
    return HTTPException(401, 'Unauthorized.')


def no_permission() -> HTTPException:
    return HTTPException(403, 'Operation not permitted.')
