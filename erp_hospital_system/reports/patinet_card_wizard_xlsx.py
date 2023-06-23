from odoo import models
import io
import base64


class PatientCardWizardXlsx(models.AbstractModel):
    _name = 'report.hospital_management.action_report_hospital_wizard'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patient):
        sheet = workbook.add_worksheet('Patient Cards')
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})
        row = 3
        col = 3
        sheet.set_column('D:D', 13)
        for obj in patient:
            row += 1
            sheet.write(row, col, 'Patient Name', bold)
            sheet.write(row, col + 1, obj.cancel_date)
            row += 1
            if obj.cancel_appointment:
                appointment = self.env[obj.cancel_appointment._name].search([('id', '=', obj.cancel_appointment.id)],
                                                                            limit=1)
                if appointment:
                    sheet.write(row, col, 'Appointment', bold)
                    sheet.write(row, col + 1, appointment.name)
                    row += 1
        sheet.write(row, col, 'Reason', bold)
        sheet.write(row, col + 1, obj.reason)

