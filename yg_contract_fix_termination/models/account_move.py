# Copyright 2024 Yves Goldberg (Ygol InternetWork)
# Part of module yg_contract_fix_termination. See LICENSE file for
# full copyright and licensing details.

from odoo import fields, models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def write(self, vals):
        """
            Checked the invoice date and it should be not after the contract end date
            return: Boolean
        """
        updated_invoice_date = vals.get('invoice_date', False)
        for rec in self:
            contract_id = rec.invoice_line_ids.contract_line_id.contract_id
            if updated_invoice_date and contract_id.date_end and datetime.strptime(updated_invoice_date, DF).date() > contract_id.date_end:
                raise UserError("You can change the invoice date only if it is before the contract end date.")
        return super(AccountMove, self).write(vals)
