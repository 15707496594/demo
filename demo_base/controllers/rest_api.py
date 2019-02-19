# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import logging
import json
import hashlib
import datetime
import base64

_logger = logging.getLogger(__name__)


class DemoBaseRestApi(http.Controller):

    @http.route(['/<string:db>/api/user/get_token'], type="json", auth="public", csrf=False, methods=['POST'])
    def auth_token(self, **request_data):
        """
        根据数据库、用户名和密码返回用户token
        :param request_data:
        :return:
        """
        authorization = request.httprequest.authorization
        json_request = request.jsonrequest
        db = request_data.get('db')
        # 判断是否传了数据库名称参数，没有则返回错误信息
        if not db:
            return self._rest_json_response({'error': 'request not bound to a database'})
        try:
            login = authorization.username
            password = authorization.password
            uid = request.session.authenticate(db, login, password)
            if not uid:  # 判断是否传登陆成功，没有则返回错误信息
                return json.dumps({'error': 'Access Denied'})
        except Exception as e:
            return json.dumps({'error': str(e)})
        token_obj = request.env['demo.base.token']
        # 判断是否需要刷新token，参数值为true则执行生成token方法
        if json_request.get('refresh'):
            token, expires_in = self._generate_token(login, password, token_obj)
        else:
            # 查询是否有旧的token记录
            old_token_record = token_obj.sudo().search([('user_id', '=', uid)], order='create_date desc', limit=1)
            if old_token_record:
                # 有旧的token记录则判断是否过期
                if old_token_record.is_expired():
                    # 过期则生成新的token
                    token, expires_in = self._generate_token(login, password, token_obj)
                else:
                    # 没有则取旧的token和剩余过期时间（单位：秒）
                    token = old_token_record.token
                    expires_in = old_token_record.get_expires_in().seconds
            else:
                # 没有旧的token记录则生成新的token
                token, expires_in = self._generate_token(login, password, token_obj)
        return self._rest_json_response({
            'token': token,
            'expires_in': expires_in
        })

    @http.route(['/<string:db>/api/<string:model>/read'], type="json", auth="public", csrf=False, methods=['POST'])
    def read_record(self, **request_data):
        """
        url中<string:db>为db的名称，<string:model>为模型名称
        标准查询接口，主要是调用search_read方法，根据json给search_read传相应参数
        :param request_data:
        example: {
                    "fields": ["name", "type"],
                    "offset": 0,
                    "limit": 7,
                    "order": "id",
                    "domain": [
                        {
                            "field": "name",
                            "operator": "ilike",
                            "value": "data"
                        }
                    ]
                }
        :return: search_read的结果
        """
        # 鉴权
        db = request_data.get('db')
        auth_result = self._user_authentication()
        if not auth_result['success']:
            return self._rest_json_response({'error': auth_result['message']})
        else:
            login, password = auth_result['login'], auth_result['password']
        # 根据json数据生成search_read的参数，返回结果
        try:
            request.session.authenticate(db, login, password)
            json_data = request.jsonrequest
            fields = json_data.get('fields')
            offset = json_data.get('offset', 0)
            limit = json_data.get('limit')
            order = json_data.get('order')
            domain = self._get_domain(json_data.get('domain'))
            result = request.env[request_data['model']].search_read(domain, fields, offset, limit, order)
        except Exception as e:
            return self._rest_json_response({'error': str(e)})
        return self._rest_json_response(result)

    @http.route(['/<string:db>/api/<string:model>/create'], type="json", auth="public", csrf=False, methods=['POST'])
    def create_record(self, **request_data):
        """
        url中<string:db>为db的名称，<string:model>为模型名称
        标准创建接口，主要是调用create方法，把json传给create方法创建记录
        :param request_data:
        :return:
        """
        # 鉴权
        db = request_data.get('db')
        auth_result = self._user_authentication()
        if not auth_result['success']:
            return self._rest_json_response({'error': auth_result['message']})
        else:
            login, password = auth_result['login'], auth_result['password']
        # 创建数据，返回数据的id
        try:
            request.session.authenticate(db, login, password)
            json_data = request.jsonrequest
            result = request.env[request_data['model']].create(json_data)
        except Exception as e:
            request.cr.rollback()
            return self._rest_json_response({'error': str(e)})
        return self._rest_json_response({"success": True, "id": result.id})

    @http.route(['/<string:db>/api/<string:model>/update'], type="json", auth="public", csrf=False, methods=['POST'])
    def update_record(self, **request_data):
        """
        url中<string:db>为db的名称，<string:model>为模型名称
        标准更新接口，主要是调用write方法，把json传给write方法更新记录
        :param request_data:
        :return:
        """
        # 鉴权
        db = request_data.get('db')
        auth_result = self._user_authentication()
        if not auth_result['success']:
            return self._rest_json_response({'error': auth_result['message']})
        else:
            login, password = auth_result['login'], auth_result['password']
        # 更新数据，返回write方法的结果
        try:
            request.session.authenticate(db, login, password)
            json_data = request.jsonrequest
            result = request.env[request_data['model']].search([("id", "=", json_data["id"])]).write(json_data)
        except Exception as e:
            request.cr.rollback()
            return self._rest_json_response({'error': str(e)})
        return self._rest_json_response({"success": result})

    @http.route(['/<string:db>/api/<string:model>/delete'], type="json", auth="public", csrf=False, methods=['POST'])
    def delete_record(self, **request_data):
        """
        url中<string:db>为db的名称，<string:model>为模型名称
        标准删除接口，主要是调用unlink方法，根据json中的domain查询出相应的记录做删除
        :param request_data:
        :return:
        """
        # 鉴权
        db = request_data.get('db')
        auth_result = self._user_authentication()
        if not auth_result['success']:
            return self._rest_json_response({'error': auth_result['message']})
        else:
            login, password = auth_result['login'], auth_result['password']
        # 删除记录，染回unlink的结果
        try:
            request.session.authenticate(db, login, password)
            json_data = request.jsonrequest
            domain = self._get_domain(json_data.get('domain'))
            result = request.env[request_data['model']].search(domain).unlink()
        except Exception as e:
            request.cr.rollback()
            return self._rest_json_response({'error': str(e)})
        return self._rest_json_response({"success": result})

    def _generate_token(self, login, password, token_obj):
        """
        生成新token方法，把用户名和登录时间用md5加密返回
        :param login: 登录用户名
        :param token_obj: token对象
        :return:
        """
        md5 = hashlib.md5()
        token_str = login + str(datetime.datetime.now())
        token_str_encode = token_str.encode(encoding='utf-8')
        md5.update(token_str_encode)
        expires_in = 7200
        token = md5.hexdigest()
        token_obj.sudo().create({
            'token': token,
            'expired_time': datetime.datetime.now() + datetime.timedelta(seconds=expires_in),
            'user_id': request.uid,
            'login': login,
            'password': base64.b64encode(password.encode('utf-8'))
        })
        return token, expires_in

    def _get_domain(self, domain_list):
        """
        根据json中的domain生成能供search和search_read使用的domain
        :param domain_list:
        :return:
        """
        domain = []
        if not domain_list:
            return domain
        for item in domain_list:
            domain.append((item['field'], item['operator'], item['value']))
        return domain

    def _rest_json_response(self, result):
        """
        格式化response，这里对应的修改了源码的_json_response，生成不带jsonrpc的json返回
        :param result:
        :return:
        """
        return {
            'rest_api': True,
            'result': result
        }

    def _user_authentication(self):
        """
        根据请求中的token对该次请求进行鉴权，返回鉴权后的结果
        :return:
        """
        url_param_str = request.httprequest.query_string.decode()
        token = url_param_str.split('=')[-1]
        token_record = request.env['demo.base.token'].sudo().search([('token', '=', token)], limit=1)
        if token_record:
            if token_record.is_expired():
                return {
                    'success': False,
                    'message': 'Token Is Expired'
                }
            else:
                return {
                    'success': True,
                    'login': token_record.login,
                    'password': base64.b64decode(token_record.password)
                }
        else:
            return {
                'success': False,
                'message': 'Invalid Token'
            }
