# Turnify - 2025 Mahin Ltd alright receipt

from flask import jsonify


def success_response(message="Success", data=None, status_code=200):
    """Standardized success response"""
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code


def error_response(message="An error occurred", data=None, status_code=400):
    """Standardized error response"""
    response = {
        "success": False,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code


def validation_error(errors):
    """Validation error response"""
    return error_response(
        message="Validation failed",
        data={"errors": errors},
        status_code=422
    )
