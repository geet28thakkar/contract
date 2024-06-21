from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _inherit = 'contract.contract'

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        self._check_company_id(vals)
        return super(Contract, self).create(vals)

    def write(self, vals):
        self._check_company_id(vals)
        return super(Contract, self).write(vals)

    def _check_company_id(self, vals):
        company_id = vals.get('company_id', self.env.company.id)

        for field_name, field in self._fields.items():
            if isinstance(field, fields.Many2one):
                related_model = self.env[field.comodel_name]
                related_record_id = vals.get(field_name, False)

                if related_record_id and 'company_id' in related_model._fields:
                    related_record = related_model.browse(related_record_id)
                    if related_record.company_id.id != company_id:
                        raise ValidationError(f"The company for {field.string} does not match the company of this record.")

    @api.constrains('company_id')
    def _check_related_companies(self):
        for record in self:
            company_id = record.company_id.id
            for field_name, field in self._fields.items():
                if isinstance(field, fields.Many2one):
                    related_model = self.env[field.comodel_name]
                    related_record = getattr(record, field_name)

                    if related_record and 'company_id' in related_model._fields and related_record.company_id.id != company_id:
                        raise ValidationError(
                            f"The company for {field.string} does not match the company of this record.")
