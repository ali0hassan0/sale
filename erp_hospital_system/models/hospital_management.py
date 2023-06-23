from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalManagement(models.Model):
    _name = 'hospital.management'
    # _inherit = 'event.event'
    _description = 'Hospital Management System'
    _order = 'id desc'

    name = fields.Char(string="Patient Name", tracking=True, required=False)
    age = fields.Integer(string="Patient Age", compute='_compute_age',
                         inverse="inverse_compute_age", search='_search_age')
    date_begin = fields.Datetime(required=False)
    date_end = fields.Datetime(required=False)
    # date_tz = fields.Selection(required=False)
    admit_date = fields.Datetime(string="Admit Date", default=fields.Datetime.now)
    discharge_date = fields.Date(string="Discharge Date")
    # built-in f            unction for current date default = fields.Date.context_today

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender")
    active = fields.Boolean(string="Active", active=False)
    image = fields.Image(string="Image")
    cancel_patient_tag = fields.Char(string="CANCELLED", readonly=True)
    work_hour = fields.Float(string="Working Hours", required=True)
    salary = fields.Float(string="salary")
    doctor_appoint = fields.Many2one('doctor.appoint', sring="Doctor Appoint")
    date_of_birth = fields.Date(string="Date of Birth")
    ref = fields.Char(string="Reference", readonly=True)
    duration = fields.Float(string="duration")
    # commission = fields.Float(string="commission", compute="onchange_commission2")
    # commission2 = fields.Float(string="Commission2", compute="onchange_commission")

    priority = fields.Selection([('0', 'Normal'),
                                 ('1', 'Low'),
                                 ('2', 'High'),
                                 ('3', 'Very High')]
                                , string="Status")
    state = fields.Selection([('draft', 'Draft'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')]
                             , string="Status", required=True, default='draft')
    user_id = fields.Many2one('res.users', string="Doctor")
    tag_ids = fields.Many2many('configure.hospital', string="Tags")
    is_birthday = fields.Boolean(string='birthday', compute="_compute_is_birthday")
    phone_call = fields.Integer(string="Phone Number")
    e_mail = fields.Char(string="E-mail")
    website = fields.Char(string="Website")
    progress = fields.Integer(string="Progress", compute="_compute_progress")

    @api.constrains('date_of_birth')
    def check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError("Inavlid Date of Birht")
            return

    @api.depends('age')
    def inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

        return

    def _search_age(self, operator, value):
        today = date.today()
        date_of_birth = today - relativedelta.relativedelta(years=value)
        start_date = date_of_birth.replace(day=1, month=1)
        end_date = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_date), ('date_of_birth', '<=', end_date)]

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = (today.year - rec.date_of_birth.year)
            else:
                rec.age = 1

    def salary_compute(self):
        for rec in self:
            rec.salary = rec.work_hour * 200
            return rec.salary

    @api.depends('state')
    def cancel_form(self, state='draft'):
        if state: "draft,'done','in_consultation"
        state = ''

    def action_in_consultation(self):
        for rec in self:
            rec.state = "in_consultation"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        # action = self.env.ref('hospital_management.cancel_appointment_action').read()[0]
        for rec in self:
            rec.state = 'cancel'

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalManagement, self).create(vals)

    # def name_get(self):
    #     patient_list = []
    #     for record in self:
    #         name = record.ref + ' : ' + record.name
    #         patient_list.append((record.id, name))
    #     return patient_list

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):

        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = 30
            elif rec.state == 'in_consultation':
                progress = 60
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

    def action_view_doctor(self):
        return {
            'name': 'Doctor',
            'res_model': 'doctor.appoint',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': {},
            'context': [],
            'type': 'ir.actions.act_window'
        }

    def action_send_msg(self):
        message = 'Hi patient %s' % self.name
        if not self.phone_call:
            ValidationError('No Phone number is provide')

        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.phone_call, message)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }
