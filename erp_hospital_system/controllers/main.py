from odoo import http


class HospitalWebpage(http.Controller):
    @http.route('/hospital', auth='public', website=True)
    def hospital_website(self):
        patient = http.request.env['hospital.management'].search(self)
        return http.request.render(
            'hospital_management.hospital_webpage', {'patients': patient}
        )
