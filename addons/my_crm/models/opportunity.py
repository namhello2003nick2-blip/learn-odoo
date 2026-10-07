from odoo import models, fields


class Opportunity(models.Model):
    _name = "my.crm.opportunity"
    _description = "CRM Opportunity"

    name = fields.Char(
        string="Opportunity",
        required=True
    )

    customer_id = fields.Many2one(
        "my.crm.customer",
        string="Customer",
        required=True
    )

    stage_id = fields.Many2one(
        "my.crm.stage",
        string="Stage",
        required=True
    )

    won_note = fields.Text(
        string="Won Note"
    )

    def action_mark_as_won(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Mark Opportunity as Won",
            "res_model": "my.crm.opportunity.won.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_opportunity_id": self.id,
            },
        }