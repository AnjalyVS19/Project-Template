from odoo import models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def action_create_template(self):
        self.ensure_one()

        def create_template_from_task(task, parent_template_id=None):
            template = self.env['project.task.template'].create({
                'name': task.name,
                'target_project_id': task.project_id.id,
                'assignees_ids': [(6, 0, task.user_ids.ids)],
                'tag_ids': [(6, 0, task.tag_ids.ids)],
                'partner_id': task.partner_id.id,
                'sale_line_id': task.sale_line_id.id,
                'deadline': task.date_deadline,
                'description': task.description,
                'parent_id': parent_template_id,
            })

            for subtask in task.child_ids:
                create_template_from_task(subtask, template.id)

            return template

        template = create_template_from_task(self)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.task.template',
            'res_id': template.id,
            'view_mode': 'form',
            'target': 'current',
        }