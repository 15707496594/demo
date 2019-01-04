# -*- coding: utf-8 -*-

from odoo import fields, models


class DemoBaseLookupType(models.Model):
    _name = "demo.base.lookup.type"
    _description = "Demo Base: Lookup Type"

    # 编码
    code = fields.Char(string="Code", required=True)
    # 名称
    name = fields.Char(string="Name", required=True, translate=True)
    # 描述
    description = fields.Text(string="Description", translate=True)
    # 快速编码值
    value_ids = fields.One2many(comodel_name="demo.base.lookup.value", inverse_name="type_id", string="Lookup Value")

    _sql_constraints = [
        ('unique_code', 'unique(code)', "Lookup code cannot be duplicated!"),
    ]


class DemoBaseLookupValue(models.Model):
    _name = "demo.base.lookup.value"
    _description = "Demo Base: Lookup Value"

    type_id = fields.Many2one(comodel_name="demo.base.lookup.type", string="Lookup", ondelete='cascade')
    # 编码
    code = fields.Char(string="Code", required=True)
    # 名称
    name = fields.Char(string="Name", required=True, translate=True)
    # 描述
    description = fields.Char(string="Description", translate=True)

    _sql_constraints = [
        ('unique_code_type_id', 'unique(type_id, code)', "The same lookup's value code cannot be duplicated!"),
        ('unique_name_type_id', 'unique(type_id, name)', "The same lookup's value name cannot be duplicated!"),
    ]
