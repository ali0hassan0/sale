from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VendorBill(models.TransientModel):
    _name = 'vendor.bill'
    _description = "Vendor Bill Report"

    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", default=fields.Datetime.now)
    product_id = fields.Many2many('product.template', string="Services/Products")
    contractor_service = fields.Many2one('res.partner', string="Contractor")
    result = fields.Text(string="Result")

    def vendor_bill_filter(self):

        account_move_obj = self.env['account.move']
        domain = [
            ('state', '=', 'posted'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
            ('amount_residual', '!=', 0.0),
            ('invoice_line_ids.product_id.detailed_type', '=', 'service'),
        ]

        if self.contractor_service:
            domain.append(('partner_id', '=', self.contractor_service.id))

        if self.product_id:
            domain.append(('invoice_line_ids.product_id', 'in', self.product_id.ids))

        account_moves = account_move_obj.search(domain)

        if not account_moves:
            raise ValidationError('No data to print.')

        result_lines = []
        # move_totals = {}

        for move in account_moves:
            result_lines.append(f"\n{move.name}")
            # move_subtotal = 0

            for move_line in move.invoice_line_ids:
                if self.product_id and move_line.product_id.id not in self.product_id.ids:
                    continue

                if self.contractor_service and move_line.move_id.partner_id.id != self.contractor_service.id:
                    continue

                if move.amount_residual < 0.0:
                    continue

                product = move_line.product_id
                cost_value = product.standard_price
                result_line = (
                    f"{move.name}\t"
                    f"{move.partner_id.name}\t"
                    f"{move_line.product_id.name}\t"
                    f"{move_line.quantity}\t"
                    f"{move_line.price_unit}\t"
                    # f"{cost_value}\t"
                    # f"{move_line.price_subtotal}\t"
                    f"{move.amount_residual}\t"

                )
                result_lines.append(result_line)
                # move_subtotal += move_line.price_subtotal

            # move_totals[move.id] = move_subtotal

        # for move in account_moves:
        #     if move.id in move_totals:
        #         subtotal = move_totals[move.id]
        #         result_lines.append(f"Subtotal: {subtotal}")

        result_lines = [line + "\tUnit Cost" if line.startswith("\n") else line for line in result_lines]

        self.result = '\n'.join(result_lines)

        action = self.env.ref('vendor_bill_report.wizard_vendor_bill_action').read()[0]
        # action['context'] = {
        #     'default_product_id': self.product_id.ids[0] if self.product_id else False,
        # }

        return action

    def action_report_cancel(self):
        return

    def print_vendor_bill_report(self):
        self.vendor_bill_filter()
        data = {'result': self.result}
        return self.env.ref('vendor_bill_report.action_vendor_report_wizard').report_action(self, data=data)
