from odoo import api, fields, models

class ProjectProject(models.Model):
    _inherit = 'project.project'

    is_from_template = fields.Boolean(string="Created from Template", default=False)

    @api.model_create_multi
    def create(self, vals_list):
        """
        When a new project is created, this method automatically:
        Creates a corresponding project template if not already existing for the project.
        Creates task templates from the project's tasks.
        """
        projects = super().create(vals_list)
        for project in projects:
            if project.is_from_template:
                continue

            existing_template = self.env['project.template'].search([
                ('project_id', '=', project.id)
            ], limit=1)

            if not existing_template:
                template = self.env['project.template'].create({
                    'name': project.name,
                    'project_id': project.id,
                    'project_tag_ids': project.tag_ids.ids,
                    'project_manager_id': project.user_id.id,
                })

                for task in self.env['project.task'].search([('project_id', '=', project.id)]):
                    self.env['project.task.template'].create({
                        'name': task.name,
                        'project_template_id': template.id,
                        'assignees_ids': task.user_ids.ids,
                        'target_project_id': project.id,
                    })
        return projects