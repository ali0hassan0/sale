from odoo import models


class VendorReportXlsx(models.AbstractModel):
    _name = 'report.vendor_bill_report.action_vendor_report_wizard'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, report):
        sheet = workbook.add_worksheet('Vendor Report')
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})
        row = 0
        col = 0
        sheet.set_column('A:A', 19)
        sheet.set_column('B:B', 16)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 10)
        sheet.set_column('E:E', 10)
        sheet.set_column('F:F', 10)
        sheet.set_column('G:G', 12)
        sheet.set_column('H:H', 10)

        results = data.get('result', '').split('\n')

        sheet.write(row, col, 'Bill No', bold)
        sheet.write(row, col + 1, 'Contractor', bold)
        sheet.write(row, col + 2, 'Product', bold)
        sheet.write(row, col + 3, 'Quantity', bold)
        sheet.write(row, col + 4, 'Unit Price', bold)
        sheet.write(row, col + 5, 'Subtotal', bold)
        sheet.write(row, col + 6, 'Amount Due', bold)
        row += 1

        subtotal_sum = 0.0
        previous_bill_no = False

        for result in results:
            values = result.split('\t')

            if len(values) >= 7:
                bill_no = values[0].strip()
                vendor_name = values[1].strip()
                product = values[2].strip()

                try:
                    quantity = float(values[3].strip())
                except ValueError:
                    quantity = 0.0

                try:
                    unit_price = float(values[4].strip())
                except ValueError:
                    unit_price = 0.0

                try:
                    residual = float(values[5].strip())
                except ValueError:
                    residual = 0.0
                if previous_bill_no and bill_no == previous_bill_no:
                    sheet.write(row, col + 2, product)
                    sheet.write(row, col + 3, quantity)
                    sheet.write(row, col + 4, unit_price)

                else:
                    sheet.write(row, col, bill_no)
                    sheet.write(row, col + 1, vendor_name)
                    sheet.write(row, col + 2, product)
                    sheet.write(row, col + 3, quantity)
                    sheet.write(row, col + 4, unit_price)
                    sheet.write(row, col + 6, residual)
                    previous_bill_no = bill_no

                total = (quantity * unit_price)
                sheet.write(row, col + 5, total)
                subtotal_sum += total

                row += 1

        sheet.write(row + 1, col + 5, 'Total:', format_1)
        sheet.write(row + 1, col + 6, subtotal_sum, format_1)
