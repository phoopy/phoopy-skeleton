from flask import jsonify, request


class AbstractController(object):
    def __init__(self, kernel):
        self.kernel = kernel

    def get_kernel(self):
        return self.kernel

    def get_input(self):
        return request.json

    def create_item_response(self, item, status=200):
        return jsonify({'data': item}), status

    def create_error_response(self, code, title, status=400):
        return jsonify({'code': code, 'title': title, 'status': status}), status
