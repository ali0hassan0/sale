{
    'name': 'Hospital Management',
    'description': 'Hospital Management',
    'author': 'Ali Hassan',
    'website': 'www.erplocalhost.com',
    'data': ['security/ir.model.access.csv','views/menu_items.xml','data/patient_tag.xml',
             'wizard/cancel_appointment_form.xml','data/configure.hospital.csv','data/sequence_data.xml',
             'views/hospital_management_form.xml',
             'views/doctor_appoint_form.xml',
             'views/medicine_hospital_form.xml','views/configure_hospital.xml',
             'views/sale_order_form.xml','views/technical_form.xml','views/hospital_res_config_setting.xml'
             ,'reports/report_xlsx.xml','static/src/xml/template.xml',
             'reports/product_template.xml'],
    'depends': ['base','event','sale','report_xlsx'],
    'application': True,
    'price':'12.0',
    'currency': 'USD',
    'images': 'static/description/icon.png',
    'category':'management',
    'maintainer':'Ali Hassan',
    'auto-install': False,
    'installable': True,
    'sequence': -88
}
