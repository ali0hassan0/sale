from odoo import api, models, fields


class TechnicalHospital(models.Model):
    _name = 'technical.hospital'
    _description = 'Technical Hospital'

    only_text = fields.Text(string="Text")
    code = fields.Text(string="Code")
    technical_expenses = fields.Integer(string="Expenditures", default=None)
