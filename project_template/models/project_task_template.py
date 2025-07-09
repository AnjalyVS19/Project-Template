from odoo import models, fields
from odoo.exceptions import ValidationError


class ProjectTaskTemplate(models.Model):
    """Model to store reusable task templates linked to a project template."""

    _name = 'project.task.template'
    _description = 'Task Template'

    name = fields.Char(required=True)
    project_template_id = fields.Many2one('project.template', string='Project Template')
    target_project_id = fields.Many2one('project.project', string='Target Project')
    assignees_ids = fields.Many2many('res.users',
                                     'project_task_template_user_rel',
                                     'template_id',
                                     'user_id',
                                     string='Assignees')

    def action_create_task(self):
        """
        Button action to create a task in the selected project using the template.
        Only Madison (login 'user') is allowed to trigger it.
        """
        self.ensure_one()
        if self.env.user.login != 'user':
            raise ValidationError("Only Madison can create tasks from template.")

        if not self.target_project_id:
            raise ValidationError("Please select a project where the task should be created.")

        task = self.env['project.task'].create({
            'name': self.name,
            'project_id': self.target_project_id.id,
            'user_ids': self.assignees_ids.ids,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'res_id': task.id,
            'view_mode': 'form',
            'target': 'current',
        }