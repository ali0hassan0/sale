from odoo import api, models, fields
import datetime
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import date


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    @api.model
    def default_get(self, fields):
        raja = super(CancelAppointmentWizard, self).default_get(fields)
        raja['cancel_date'] = datetime.date.today()
        return raja

    reason = fields.Text(string="Reason", required=False)
    cancel_appointment = fields.Many2one('hospital.management', string="Cancel Appointment")
    cancel_date = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        cancel_days = self.env['ir.config_parameter'].get_param('hospital_management.cancel_days')
        allowed_date = self.cancel_appointment.admit_date - relativedelta.relativedelta(day=int(cancel_days))
        if allowed_date.date() < date.today():
            raise ValidationError("Not allowed to delete this record")
        self.cancel_appointment.state = 'cancel'
        return {
            'type': 'ir.action.client',
            'tag': 'reload'}

    def action_back(self):
        return

    def print_xlsx_report(self):
        data = {'form_data': self.read()[0]}
        print(data)
        return self.env.ref('hospital_management.action_report_hospital_wizard').report_action(self, data=data)
