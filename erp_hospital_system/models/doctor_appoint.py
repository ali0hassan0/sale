from odoo import api, fields, models


class DoctorAppoint(models.Model):
    _name = 'doctor.appoint'
    _description = 'doctor appointed to patient'
    _rec_name = 'doctor_name'

    doctor_name = fields.Char(string="Doctor Name", tracking=True)
    patient_parent = fields.Char(string="Parent Name")
    martial_status = fields.Selection([
        ('maried', 'Married'),
        ('single', 'Single')
    ], String="Martial Status")
    patient_partner_name = fields.Char(string="Partner Name")

    patient_name = fields.Many2one('hospital.management', string="Patient Name")
    doctor_age = fields.Integer(string="Doctor Age")
    patient_gender = fields.Selection(related='patient_name.gender')
    ref = fields.Char(string="Reference")
    date_for_checkup = fields.Date(string='Checkup Date')
    doctor_fee = fields.Float(string="Doctor Fee")
    medicine_price = fields.Char(related='medicine.medicine_price', string="HJdf")
    prescription = fields.Html(string="Prescription")
    medicine = fields.Many2one('medicine.hospital', string="Medicines")

    sequence = fields.Integer(string='Sequence', )

    def test_button(self):
        print('no data')

    @api.onchange('patient_name')
    def onchange_patient_name(self):
        for rec in self:
            rec.ref = rec.patient_name.ref

    def action_medicine(self):
        res = self.env['medicine.hospital']
        res['medicine_price'] = self.medicine_price
        return self.medicine_price
        print(self.medicine_price)
        return res

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('doctor.appoint')
        return super(DoctorAppoint, self).create(vals)
