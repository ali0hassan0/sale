from odoo import api, fields, models


class ConfigureHospital(models.Model):
    _name = 'configure.hospital'
    _description = 'Configure Hospital'
    _rec_name = 'tag_name'

    tag_name = fields.Char(string="Tag Name", required=True)
    active = fields.Boolean(string="Status", default=True)
    color = fields.Integer(string="Color")
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
            if not default.get('tag_name'):
                default['tag_name'] = ("(copy)","", self.tag_name)
            res = super(ConfigureHospital, self).copy(default)
        return res

    _sql_constraints = [
        ('unique_tag_name', 'unique (tag_name,active)', 'The Tag must be unique!'),
        ('check_sequence', 'check (sequence > 0)', 'The Must be Greater Than Zero')
    ]
