from odoo import api, fields, models


class MedicineHospital(models.Model):
    _name = 'medicine.hospital'
    _description = 'Medicines available'
    _rec_name = 'medicine_name'

    medicine_name = fields.Char(string="Medicine Name")
    medicine_price = fields.Char(string="Medicine Price")
    doctor_details_ids = fields.One2many('doctor.appoint', 'medicine', string="Doctor Details")
    hide_doctor_fee = fields.Boolean(string="Hide Fee")
    record_reference = fields.Reference(selection=[('hospital.management', 'patients'),
                                                   ('doctor.appoint', 'Doctor')], string="Record")
    com = fields.Float(string="commission", compute="action_com")
    com2 = fields.Float(string="commission 2", compute="action_com2")

    @api.depends('com2')
    def action_com(self):
        for rec in self:
            if rec.com2 > 0:
                rec.com = 0
            return rec.com

    @api.depends('com')
    def action_com2(self):
        for rec in self:
            if rec.com > 0:
                rec.com2 = 0
            return rec.com2

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
            if not default.get('medicine_name'):
                default['medicine_name'] = ('%s (copy)' + self.medicine_name)
                res = super(MedicineHospital, self).copy(default)
        return res
