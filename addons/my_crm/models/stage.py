from odoo import models, fields, api
from odoo.exceptions import ValidationError

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

    is_won = fields.Boolean(
        string="Won Stage",
        default=False
    )

    is_lost = fields.Boolean(
        string="Lost Stage",
        default=False
    )

    opportunity_ids = fields.One2many(
        "my.crm.opportunity",
        "stage_id",
        string="Opportunities"
    )

    @api.constrains("is_won", "is_lost")
    def _check_special_stage(self):
        for stage in self:

            if stage.is_won and stage.is_lost:
                raise ValidationError(
                    "Một Stage không thể vừa là Won vừa là Lost."
                )

            if stage.is_won:
                other_won = self.search([
                    ("is_won", "=", True),
                    ("id", "!=", stage.id),
                ], limit=1)

                if other_won:
                    raise ValidationError(
                        "Chỉ được có một Won Stage."
                    )

            if stage.is_lost:
                other_lost = self.search([
                    ("is_lost", "=", True),
                    ("id", "!=", stage.id),
                ], limit=1)

                if other_lost:
                    raise ValidationError(
                        "Chỉ được có một Lost Stage."
                    )