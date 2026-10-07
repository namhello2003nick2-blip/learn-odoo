from odoo import models, fields


class Stage(models.Model):
    _name = "my.crm.stage"
    _description = "CRM Stage"
    _order = "sequence, id"

    name = fields.Char(
        string="Stage Name",
        required=True
    )

    sequence = fields.Integer(
        string="Sequence",
        default=10
    )

    fold = fields.Boolean(
        string="Folded in Pipeline",
        default=False
    )

    opportunity_ids = fields.One2many(
        "my.crm.opportunity",
        "stage_id",
        string="Opportunities"
    )