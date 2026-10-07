from odoo import models, fields


class OpportunityWonWizard(models.TransientModel):
    _name = "my.crm.opportunity.won.wizard"
    _description = "Mark Opportunity as Won"

    opportunity_id = fields.Many2one(
        "my.crm.opportunity",
        string="Opportunity",
        required=True
    )

    note = fields.Text(
        string="Note"
    )

    def action_confirm(self):
        won_stage = self.env["my.crm.stage"].search(
            [("name", "=", "Won")],
            limit=1
        )

        if not won_stage:
            return False

        self.opportunity_id.write({
            "stage_id": won_stage.id,
            "won_note": self.note,
        })

        return {"type": "ir.actions.act_window_close"}