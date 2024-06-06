# Copyright 2016 Tecnativa - Carlos Dauden
# Copyright 2018 ACSONE SA/NV.
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    # We keep this field for migration purpose
    old_contract_id = fields.Many2one("contract.contract")

    def write(self, vals):
        """
            Checked the invoice date and it should be not after the contract end date
            return: Boolean
        """
        updated_invoice_date = vals.get('invoice_date', False)
        for rec in self:
            contract_id = rec.invoice_line_ids.contract_line_id.contract_id
            if updated_invoice_date and datetime.strptime(updated_invoice_date, DF).date() > contract_id.date_end:
                raise UserError("You can change the invoice date only if it is before the contract end date.")
        return super(AccountMove, self).write(vals)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    contract_line_id = fields.Many2one(
        "contract.line", string="Contract Line", index=True
    )
