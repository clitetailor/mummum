# -*- coding: utf-8 -*-

from flask import abort, redirect, url_for, jsonify, session, render_template
from flask_wtf.csrf import CsrfProtect
# from utils.csrf_test import CsrfProtect
from functools import wraps

csrf_protect = CsrfProtect()


@csrf_protect.error_handler
def csrf_error(reason):
    return abort(400, {'code': 400, 'message': reason})


