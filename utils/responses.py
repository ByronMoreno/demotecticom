from flask import jsonify

def json_success(data=None, message=None, status_code=200):
    response = {
        'status': 'success'
    }
    if message is not None:
        response['message'] = message
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def json_error(message, status_code=400, errors=None):
    response = {
        'status': 'error',
        'message': message
    }
    if errors is not None:
        response['errors'] = errors
    return jsonify(response), status_code
