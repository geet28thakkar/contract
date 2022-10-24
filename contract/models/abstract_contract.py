# Copyright 2004-2010 OpenERP SA
# Copyright 2014 Angel Moya <angel.moya@domatix.com>
# Copyright 2015-2020 Tecnativa - Pedro M. Baeza
# Copyright 2016-2018 Carlos Dauden <carlos.dauden@tecnativa.com>
# Copyright 2016-2017 LasLabs Inc.
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ContractAbstractContract(models.AbstractModel):
    _inherit = "contract.recurrency.basic.mixin"
    _name = "contract.abstract.contract"
    _description = "Abstract Recurring Contract"
    _check_company_auto = True

    # These fields will not be synced to the contract
    NO_SYNC = ["name", "partner_id", "company_id"]

    name = fields.Char(required=True)
    # Needed for avoiding errors on several inherited behaviors
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", index=True
    )
    pricelist_id = fields.Many2one(comodel_name="product.pricelist", string="Pricelist")
    contract_type = fields.Selection(
        selection=[("sale", "Customer"), ("purchase", "Supplier")],
        default="sale",
        index=True,
    )
    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
        domain="[('type', '=', contract_type)]",
        compute="_compute_journal_id",
        store=True,
        readonly=False,
        index=True,
        check_company=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company.id,
    )
    line_recurrence = fields.Boolean(
        string="Recurrence at line level?",
        help="Mark this check if you want to control recurrrence at line level instead"
        " of all together for the whole contract.",
    )
    generation_type = fields.Selection(
        selection=lambda self: self._selection_generation_type(),
        default=lambda self: self._default_generation_type(),
        help="Choose the document that will be automatically generated by cron.",
    )

    @api.model
    def _selection_generation_type(self):
        return [("invoice", "Invoice")]

    @api.model
    def _default_generation_type(self):
        return "invoice"

    @api.onchange("contract_type")
    def _onchange_contract_type(self):
        if self.contract_type == "purchase":
            self.contract_line_ids.filtered("automatic_price").update(
                {"automatic_price": False}
            )

    @api.depends("contract_type", "company_id")
    def _compute_journal_id(self):
        AccountJournal = self.env["account.journal"]
        for contract in self:
            domain = [
                ("type", "=", contract.contract_type),
                ("company_id", "=", contract.company_id.id),
            ]
            journal = AccountJournal.search(domain, limit=1)
            if journal:
                contract.journal_id = journal.id
            else:
                contract.journal_id = None
