from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectTaskTemplate(models.Model):
    _name = 'project.task.template'
    _description = 'Task Template'

    name = fields.Char(required=True)
    project_template_id = fields.Many2one('project.template', string='Project Template')
    target_project_id = fields.Many2one('project.project', string='Target Project')
    assignees_ids = fields.Many2many(
        'res.users',
        'project_task_template_user_rel',
        'template_id',
        'user_id',
        string='Assignees'
    )
    tag_ids = fields.Many2many('project.tags', string='Tags')
    partner_id = fields.Many2one('res.partner', string='Customer')
    sale_line_id = fields.Many2one('sale.order.line', string='Sale Order Item')
    deadline = fields.Date(string="Deadline")
    description = fields.Html(string="Description")
    subtask_ids = fields.One2many('project.task.template', 'parent_id', string='Subtasks')
    parent_id = fields.Many2one('project.task.template', string='Parent Task')

    def action_create_task(self):
        self.ensure_one()

        if not self.target_project_id:
            raise ValidationError("Please select a project where the task should be created.")

        task = self.env['project.task'].create({
            'name': self.name,
            'project_id': self.target_project_id.id,
            'user_ids': self.assignees_ids.ids,
            'tag_ids': self.tag_ids.ids,
            'partner_id': self.partner_id.id,
            'sale_line_id': self.sale_line_id.id,
            'date_deadline': self.deadline,
            'description': self.description,
            'stage_id': default_stage.id if default_stage else False,
        })

        for subtask_template in self.subtask_ids:
            self.env['project.task'].create({
                'name': subtask_template.name,
                'project_id': self.target_project_id.id,
                'user_ids': subtask_template.assignees_ids.ids,
                'tag_ids': subtask_template.tag_ids.ids,
                'partner_id': subtask_template.partner_id.id,
                'sale_line_id': subtask_template.sale_line_id.id,
                'date_deadline': subtask_template.deadline,
                'description': subtask_template.description,
                'stage_id': default_stage.id if default_stage else False,
                'parent_id': task.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'res_id': task.id,
            'view_mode': 'form',
            'target': 'current',
        }