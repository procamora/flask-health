#!/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from http import HTTPStatus  # https://docs.python.org/3/library/http.html
from typing import NoReturn, Text, Dict

import colorlog
from flask import Flask, Response, request

# Use:
# curl --header "Content-Type: application/json" \
#   --request POST \
#   --data '{"token":"RG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"}' \
#   http://localhost:8888/health

app = Flask(__name__)
MIME_TYPE_JSON: Text = 'application/json'
MIME_TYPE_FORM: Text = 'application/x-www-form-urlencoded'
# colorize.colorize_werkzeug()
TOKEN: Text = 'RG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ'  # Doesn't apply security only prevents false positives


def update_logger(verbose: bool, name: Text = 'flask.app') -> NoReturn:
    # Desabilita log de modulos
    # for _ in ("boto", "elasticsearch", "urllib3"):
    #    logging.getLogger(_).setLevel(logging.CRITICAL)

    log_format = '%(levelname)s - %(module)s -%(funcName)s- %(message)s'

    bold_seq = '\033[1m'
    colorlog_format = (
        f'{bold_seq} '
        '%(log_color)s '
        f'{log_format}'
    )

    colorlog.basicConfig(format=colorlog_format)
    # logging.basicConfig(format=colorlog_format)
    log = logging.getLogger(name)

    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    return log


logger = update_logger(False)


@app.route('/health', methods=['POST'])
def post_is_alive():
    response_json: Dict = {'status': 'error'}
    response_status: int = HTTPStatus.FORBIDDEN

    logger.info(request.content_type)
    if request.content_type == MIME_TYPE_JSON:
        request_json = request.get_json()
        logger.debug(request_json)
        if 'token' in request_json.keys():
            if request_json['token'] == TOKEN:
                response_json = {'status': 'ok'}
                response_status = HTTPStatus.OK
            else:
                response_json = {'status': 'token invalid'}
                response_status = HTTPStatus.UNAUTHORIZED
        else:
            response_json = {'status': 'json requieres key token'}
            response_status = HTTPStatus.NOT_IMPLEMENTED
        logger.debug(f"{response_json}")
        logger.debug(f"{response_status}")
        return Response(response=json.dumps(response_json), status=response_status, mimetype=MIME_TYPE_JSON)
    else:
        return Response(response=json.dumps(response_json), status=HTTPStatus.BAD_REQUEST, mimetype=MIME_TYPE_JSON)


@app.errorhandler(404)
def not_found(error):
    return Response(response=json.dumps({'status': 'error 404'}), status=HTTPStatus.NOT_ACCEPTABLE,
                    mimetype=MIME_TYPE_JSON)


if __name__ == "__main__":
    app.run(debug=True, port=8888, host='0.0.0.0')
