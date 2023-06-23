from odoo import models
import io
import base64


class PatientCardXlsx(models.AbstractModel):
    _name = 'report.hospital_management.report_patientreport'
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
            sheet.merge_range(row, col, row, col + 1, 'Id Card', format_1)
            row += 1
            if obj.image:
                patient_image = io.BytesIO(base64.b64decode(obj.image))
                sheet.insert_image(row, col, "image.png",
                                   {'image_data': patient_image, 'x_scale': 0.4, 'y_scale': 0.6})

                row += 7

            sheet.write(row, col, 'Name', bold)
            sheet.write(row, col + 1, obj.name)
            row += 1
            sheet.write(row, col, 'Reference', bold)
            sheet.write(row, col + 1, obj.ref)
            row += 1
            sheet.write(row, col, 'Gender', bold)
            sheet.write(row, col + 1, obj.gender)
            row += 1
            sheet.write(row, col, 'Priority', bold)
            sheet.write(row, col + 1, obj.priority)
            row += 1
            sheet.write(row, col, 'State', bold)
            sheet.write(row, col + 1, obj.state)

            row += 2

            # sheet.merge_range(18, 3, 19, 6, '',format_1)
            # sheet.merge_range(4, 2, 19, 2, '',format_1)
            # sheet.merge_range(4, 6, 19, 6, '',format_1)
            # sheet.merge_range(4,5,4,5,'', format_1)
