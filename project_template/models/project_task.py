from odoo import models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, vals):
        """
        On task creation, automatically add it to the corresponding project template
        as a task template (if the project has one and the task isn't duplicated).
        """
        task = super().create(vals)
        project = task.project_id
        template = self.env['project.template'].search([('project_id', '=', project.id)], limit=1)

        if template:
            existing_task_template = self.env['project.task.template'].search([
                ('name', '=', task.name),
                ('project_template_id', '=', template.id)
            ], limit=1)

            if not existing_task_template:
                self.env['project.task.template'].create({
                    'name': task.name,
                    'project_template_id': template.id,
                    'target_project_id': project.id,
                    'assignees_ids': task.user_ids.ids
                })
            else:
                pass
        return task