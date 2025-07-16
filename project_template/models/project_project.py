from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    is_from_template = fields.Boolean(string="Created from Template", default=False)

    def action_create_template(self):
        self.ensure_one()

        existing_template = self.env['project.template'].search([
            ('project_id', '=', self.id)
        ], limit=1)
        if existing_template:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'project.template',
                'res_id': existing_template.id,
                'view_mode': 'form',
                'target': 'current',
            }

        template = self.env['project.template'].create({
            'name': self.name,
            'project_id': self.id,
            'project_tag_ids': self.tag_ids.ids,
            'project_manager_id': self.user_id.id,
        })

        for task in self.task_ids:
            self.env['project.task.template'].create({
                'name': task.name,
                'project_template_id': template.id,
                'assignees_ids': [(6, 0, task.user_ids.ids)],
                'target_project_id': self.id,
                'tag_ids': [(6, 0, task.tag_ids.ids)],
                'partner_id': task.partner_id.id,
                'sale_line_id': task.sale_line_id.id,
                'deadline': task.date_deadline,
                'description': task.description,
                'parent_id': False,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.template',
            'res_id': template.id,
            'view_mode': 'form',
            'target': 'current',
        }