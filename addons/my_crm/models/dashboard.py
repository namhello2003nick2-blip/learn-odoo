from odoo import models, fields, api


class CRMDashboard(models.TransientModel):
    _name = "my.crm.dashboard"
    _description = "CRM Dashboard"

    total_customers = fields.Integer(
        string="Total Customers"
    )

    total_opportunities = fields.Integer(
        string="Total Opportunities"
    )

    open_opportunities = fields.Integer(
        string="Open Opportunities"
    )

    won_opportunities = fields.Integer(
        string="Won Opportunities"
    )

    lost_opportunities = fields.Integer(
        string="Lost Opportunities"
    )

    win_rate = fields.Float(
        string="Win Rate"
    )

    expected_revenue = fields.Float(
        string="Expected Revenue"
    )

    @api.model
    def get_dashboard_data(self):

        Customer = self.env["my.crm.customer"]
        Opportunity = self.env["my.crm.opportunity"]

        total_customers = Customer.search_count([])

        total_opportunities = Opportunity.search_count([])

        won_stage = self.env["my.crm.stage"].search(
            [("is_won", "=", True)],
            limit=1
        )

        lost_stage = self.env["my.crm.stage"].search(
            [("is_lost", "=", True)],
            limit=1
        )

        won_opportunities = 0
        lost_opportunities = 0

        if won_stage:
            won_opportunities = Opportunity.search_count([
                ("stage_id", "=", won_stage.id)
            ])

        if lost_stage:
            lost_opportunities = Opportunity.search_count([
                ("stage_id", "=", lost_stage.id)
            ])

        open_opportunities = (
            total_opportunities
            - won_opportunities
            - lost_opportunities
        )

        if total_opportunities:
            win_rate = (
                won_opportunities
                / total_opportunities
                * 100
            )
        else:
            win_rate = 0

        revenue_result = Opportunity.read_group(
            [],
            ["expected_revenue:sum"],
            []
        )

        expected_revenue = 0

        if revenue_result:
            expected_revenue = (
                revenue_result[0].get("expected_revenue", 0)
                or 0
            )

        return {
            "total_customers": total_customers,
            "total_opportunities": total_opportunities,
            "open_opportunities": open_opportunities,
            "won_opportunities": won_opportunities,
            "lost_opportunities": lost_opportunities,
            "win_rate": win_rate,
            "expected_revenue": expected_revenue,
        }


    @api.model
    def action_open_dashboard(self):

        data = self.get_dashboard_data()

        dashboard = self.create(data)

        return {
            "type": "ir.actions.act_window",
            "name": "CRM Dashboard",
            "res_model": "my.crm.dashboard",
            "view_mode": "form",
            "res_id": dashboard.id,
            "target": "current",
        }

    def action_open_all_opportunities(self):
        return {
            "type": "ir.actions.act_window",
            "name": "All Opportunities",
            "res_model": "my.crm.opportunity",
            "view_mode": "kanban,list,form",
        }

    def action_open_open_opportunities(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Open Opportunities",
            "res_model": "my.crm.opportunity",
            "view_mode": "kanban,list,form",
            "domain": [
                ("stage_id.is_won", "=", False),
                ("stage_id.is_lost", "=", False),
            ],
        }

    def action_open_won_opportunities(self):
        won_stage = self.env["my.crm.stage"].search(
            [("is_won", "=", True)],
            limit=1
        )

        domain = []

        if won_stage:
            domain = [
                ("stage_id", "=", won_stage.id)
            ]

        return {
            "type": "ir.actions.act_window",
            "name": "Won Opportunities",
            "res_model": "my.crm.opportunity",
            "view_mode": "kanban,list,form",
            "domain": domain,
        }

    def action_open_lost_opportunities(self):
        lost_stage = self.env["my.crm.stage"].search(
            [("is_lost", "=", True)],
            limit=1
        )

        domain = []

        if lost_stage:
            domain = [
                ("stage_id", "=", lost_stage.id)
            ]

        return {
            "type": "ir.actions.act_window",
            "name": "Lost Opportunities",
            "res_model": "my.crm.opportunity",
            "view_mode": "kanban,list,form",
            "domain": domain,
        }

    def action_open_customers(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Customers",
            "res_model": "my.crm.customer",
            "view_mode": "list,form",
        }