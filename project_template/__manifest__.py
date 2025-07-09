{
    'name': 'Project Template',
    'version': '1.0',
    'summary': 'Create project and task templates',
    'sequence':1,
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_template_views.xml',
        'views/project_template_menu.xml',
        'views/task_template_views.xml',
        'data/user_demo.xml',
    ],
    'application': True
}