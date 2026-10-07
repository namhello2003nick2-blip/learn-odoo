from odoo import models, fields, api
from odoo.exceptions import ValidationError

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

    opportunity_count = fields.Integer(
        string="Opportunity Count",
        compute="_compute_opportunity_count"
    )

    @api.depends("opportunity_ids")
    def _compute_opportunity_count(self):
        for customer in self:
            customer.opportunity_count = len(customer.opportunity_ids)

    @api.onchange("email")
    def _onchange_email(self):
        if self.email:
            self.email = self.email.strip().lower()

    @api.constrains("email")
    def _check_email(self):
        for customer in self:
            if customer.email and "@" not in customer.email:
                raise ValidationError(
                    "Email không hợp lệ."
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name"):
                vals["name"] = vals["name"].strip()

        return super().create(vals_list)

    def write(self, vals):
        if vals.get("name"):
            vals["name"] = vals["name"].strip()

        return super().write(vals)

    def unlink(self):
        for customer in self:
            if customer.opportunity_ids:
                raise ValidationError(
                    "Không thể xóa Customer đang có Opportunity."
                )

        return super().unlink()

    def action_create_test_opportunity(self):
        stage = self.env["my.crm.stage"].search(
            [],
            order="sequence, id",
            limit=1,
        )

        if not stage:
            raise ValidationError("Chưa có Stage nào.")

        self.env["my.crm.opportunity"].create({
            "name": "Test Opportunity",
            "customer_id": self.id,
            "stage_id": stage.id,
        })

        return True