from odoo import models, fields, api


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

    customer_email = fields.Char(
        string="Customer Email",
        readonly=True
    )

    @api.onchange("customer_id")
    def _onchange_customer_id(self):
        if self.customer_id:
            self.customer_email = self.customer_id.email