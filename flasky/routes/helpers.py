from flask import json, Response


def response(content: dict, status: int = 200) -> Response:
    return Response(json.dumps(content), status=status, mimetype="application/json")
