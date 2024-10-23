from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Document(models.Model):
    _inherit = 'documents.document'

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('pending_tags', 'Pendiente de Etiquetas'),
        ('done', 'Completado')
    ], default='draft', string='Estado', tracking=True)

    @api.model
    def create(self, vals):
        record = super(Document, self).create(vals)
        record.state = 'pending_tags'
        return record

    def action_validate_tags(self):
        for record in self:
            if not record.tag_ids:
                raise ValidationError('Debe asignar al menos una etiqueta antes de continuar.')
            record.state = 'done'

    def write(self, vals):
        res = super(Document, self).write(vals)
        if 'tag_ids' in vals and self.state == 'pending_tags':
            if self.tag_ids:
                self.state = 'done'
        return res

