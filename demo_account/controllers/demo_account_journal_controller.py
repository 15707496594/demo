# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class DemoAccountJournalController(http.Controller):

    @http.route(['/oauth/token'], type="json", auth="public", csrf=False, website=False)
    def oauth_token(self, **request_data):
        authorization = request.httprequest.authorization
        db = request.httprequest.values.get('db')
        login = authorization.username
        password = authorization.password
        response = {}
        if authorization is None:
            response["success"] = False
            response["message"] = "Need authorization"
        else:
            if authorization.type != 'basic':
                response["success"] = False
                response["message"] = "Authorization type need be basic"
            else:
                if login == "" or login is None or password == "" or password is None:
                    response["success"] = False
                    response["message"] = "Authorization info is not complete"
                else:
                    if db is None or db == "":
                        response["success"] = False
                        response["message"] = "Request must have attribute db"
                    else:
                        if isinstance(db, str):
                            response["success"] = True
                        else:
                            response["success"] = False
                            response["message"] = "The value of attribute db have error data type"
        if response.get("success"):
            request.session.authenticate(db, authorization.username, authorization.password)
            return {
                "token": '无尽'
            }
        else:
            return response

    @http.route(['/api/account/journal/query'], type="http", auth="public", csrf=False, website=True)
    def account_journal_query(self, **request_data):
        authorization = request.httprequest.authorization
        json_request = request.jsonrequest
        db = request.httprequest.values.get('client')
        login = authorization.username
        password = authorization.password
        response = {}
        if authorization is None:
            response["success"] = False
            response["message"] = "Need authorization"
        else:
            if authorization.type != 'basic':
                response["success"] = False
                response["message"] = "Authorization type need be basic"
            else:
                if login == "" or login is None or password == "" or password is None:
                    response["success"] = False
                    response["message"] = "Authorization info is not complete"
                else:
                    if db is None or db == "":
                        response["success"] = False
                        response["message"] = "Request must have attribute db"
                    else:
                        if isinstance(db, str):
                            response["success"] = True
                        else:
                            response["success"] = False
                            response["message"] = "The value of attribute db have error data type"
        if response.get("success"):
            request.session.authenticate(db, authorization.username, authorization.password)
            return {
                "success": True,
                "data": request.env["demo.account.journal"].search_read([])
            }
        else:
            return response
