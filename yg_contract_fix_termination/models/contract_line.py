# Copyright 2024 Yves Goldberg (Ygol InternetWork)
# Part of module yg_contract_fix_termination. See LICENSE file for
# full copyright and licensing details.


from odoo import _, api, fields, models



class ContractLine(models.Model):
    _inherit = "contract.line"

    is_terminated = fields.Boolean(related="contract_id.is_terminated")
