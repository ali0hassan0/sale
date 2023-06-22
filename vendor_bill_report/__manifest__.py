{
    'name': "Vendor bill Report",

    'summary': """
        This module add a menu in accounting under partner reports(vendor bill Report) and print products
        vendor bill details in excel sheet filtering on date range,contractor and products""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ERP VISION",
    'website': "http://www.ERPcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'sale', 'account', 'purchase','account_accountant','account_reports'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/wizard_vendor_bill.xml'
        ,'reports/report.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto-install': False,
    'installable': True,
    'sequence': -79
}
