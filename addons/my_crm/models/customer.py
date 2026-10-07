from odoo import models, fields


class Customer(models.Model):
    _name = "my.crm.customer"
    _description = "CRM Customer"

    name = fields.Char(
        string="Name",
        required=True
    )

    email = fields.Char(
        string="Email"
    )

    phone = fields.Char(
        string="Phone"
    )

    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )

    opportunity_ids = fields.One2many(
        "my.crm.opportunity",
        "customer_id",
        string="Opportunities"
    )

    def action_create_test_opportunity(self):
        self.env["my.crm.opportunity"].create({
            "name": "Test Opportunity",
            "customer_id": self.id,
        })

        return True