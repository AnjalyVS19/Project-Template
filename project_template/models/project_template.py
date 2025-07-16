from odoo import models, fields
from odoo.exceptions import AccessError


class ProjectTemplate(models.Model):
    _name = 'project.template'
    _description = 'Project Template'

    name = fields.Char(required=True, string="Project Name")
    project_id = fields.Many2one('project.project', string="Linked Project")
    task_template_ids = fields.One2many('project.task.template', 'project_template_id', string='Tasks')
    project_tag_ids = fields.Many2many('project.tags', string='Tags')
    project_manager_id = fields.Many2one('res.users', string='Project Manager', default=lambda self: self.env.ref('project_template.project_user_madison', raise_if_not_found=False))

    def action_create_project(self):
        """
        Allows only the assigned project manager to create a real project from this template.
        Copies the template tasks to the new project.
        """
        if self.env.user != self.project_manager_id:
            raise AccessError("Only the Project Manager can create the project from this template.")

        for template in self:
            project = self.env['project.project'].create({
                'name': template.name,
                'user_id': template.project_manager_id.id,
                'tag_ids': template.project_tag_ids.ids,
                'is_from_template': True,
            })

            for task_template in template.task_template_ids:
                self.env['project.task'].create({
                    'name': task_template.name,
                    'project_id': project.id,
                    'user_ids': task_template.assignees_ids.ids
                })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'res_id': project.id,
            'view_mode': 'form',
            'target': 'current',
        }