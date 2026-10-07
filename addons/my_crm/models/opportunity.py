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

    won_date = fields.Datetime(
        string="Won Date",
        readonly=True
    )

    expected_close_date = fields.Date(
        string="Expected Close Date"
    )

    expected_revenue = fields.Float(
        string="Expected Revenue"
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

    def write(self, vals):
        result = super().write(vals)

        if "stage_id" in vals:
            won_stage = self.env["my.crm.stage"].search(
                [("is_won", "=", True)],
                limit=1
            )

            if won_stage:
                for opportunity in self:
                    if opportunity.stage_id == won_stage:
                        if not opportunity.won_date:
                            opportunity.won_date = fields.Datetime.now()

        return result

    def _cron_auto_mark_expired(self):
        today = fields.Date.today()

        lost_stage = self.env["my.crm.stage"].search(
            [("is_lost", "=", True)],
            limit=1
        )

        if not lost_stage:
            return

        opportunities = self.search([
            ("expected_close_date", "<", today),
        ])

        for opportunity in opportunities:
            if opportunity.stage_id.is_won:
                continue

            if opportunity.stage_id.is_lost:
                continue

            opportunity.stage_id = lost_stage.id