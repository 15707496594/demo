# -*- coding: utf-8 -*-

from odoo import fields, models, api


class DemoBaseToken(models.Model):
    _name = 'demo.base.token'
    _description = 'Demo Base Token'

    user_id = fields.Integer()
    login = fields.Char()
    password = fields.Char()
    token = fields.Char(index=True)
    expired_time = fields.Datetime()

    @api.multi
    def is_expired(self):
        """
        判断token是否过期
        :return: True or False
        """
        self.ensure_one()
        return fields.Datetime.now() > self.expired_time

    @api.multi
    def get_expires_in(self):
        """
        获取token剩余时间
        :return:
        """
        self.ensure_one()
        return self.expired_time - fields.Datetime.now()

