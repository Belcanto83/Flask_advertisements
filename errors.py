# from flask import jsonify
# from server import app
#
#
# class HttpError(Exception):
#     def __init__(self, status_code: int, message: str | dict | list):
#         self.status_code = status_code
#         self.message = message
#
#
# @app.errorhandler(HttpError)
# def error_handler(error: HttpError):
#     response = jsonify({'status': 'error', 'message': error.message})
#     response.status_code = error.status_code
#     return response


class ForeignKeyError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
