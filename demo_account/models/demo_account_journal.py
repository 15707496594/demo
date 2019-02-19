# -*- coding: utf-8 -*-

from odoo import fields, models


class DemoAccountJournal(models.Model):
    _name = "demo.account.journal"
    _description = "Demo Account: Journal"

    # 代码
    code = fields.Char(string="Code", required=True)
    # 名称
    name = fields.Char(string="Name", required=True, translate=True)
    # 类型
    type = fields.Selection(selection=[('sale', 'Sale'),
                                       ('sale_refund', 'Sale Refund'),
                                       ('purchase', 'Purchase'),
                                       ('purchase_refund', 'Purchase Refund'),
                                       ('cash', 'Cash'),
                                       ('bank', 'Bank'),
                                       ('general', 'General'),
                                       ('situation', 'Situation')], string="Type", required=True,
                            help="'Sales' ledger for customer invoices;\n"
                                 "'Purchases' ledger for supplier invoices;\n"
                                 "'Cash' or 'Bank' ledger for payment by customers or suppliers;\n"
                                 "'General' for various other businesses;\n"
                                 "'Situation' earlier balances used to generate new fiscal year.\n")
