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