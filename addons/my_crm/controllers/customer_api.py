from odoo import http
from odoo.http import request


class CustomerAPI(http.Controller):

    @http.route(
        "/my_crm/customers",
        type="http",
        auth="user",
        methods=["GET"]
    )
    def get_customers(self):
        customers = request.env["my.crm.customer"].search([])

        result = []

        for customer in customers:
            result.append({
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
            })

        return request.make_json_response(result)


    @http.route(
        "/my_crm/customers",
        type="http",
        auth="user",
        methods=["POST"],
        csrf=False
    )
    def create_customer(self):
        data = request.httprequest.get_json(silent=True) or {}

        if not data.get("name"):
            return request.make_json_response(
                {"error": "name is required"},
                status=400
            )

        customer = request.env["my.crm.customer"].create({
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
        })

        return request.make_json_response(
            {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
            },
            status=201
        )

    @http.route(
        "/my_crm/customers/<int:customer_id>",
        type="http",
        auth="user",
        methods=["GET"]
    )
    def get_customer(self, customer_id):

        customer = request.env["my.crm.customer"].browse(customer_id)

        if not customer.exists():
            return request.make_json_response(
                {"error": "Customer not found"},
                status=404
            )

        return request.make_json_response({
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
        })


    @http.route(
        "/my_crm/customers/<int:customer_id>",
        type="http",
        auth="user",
        methods=["PUT"],
        csrf=False
    )
    def update_customer(self, customer_id):

        customer = request.env["my.crm.customer"].browse(customer_id)

        if not customer.exists():
            return request.make_json_response(
                {"error": "Customer not found"},
                status=404
            )

        data = request.httprequest.get_json(silent=True) or {}

        values = {}

        if "name" in data:
            values["name"] = data["name"]

        if "email" in data:
            values["email"] = data["email"]

        if "phone" in data:
            values["phone"] = data["phone"]

        if not values:
            return request.make_json_response(
                {"error": "No data to update"},
                status=400
            )

        customer.write(values)

        return request.make_json_response({
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
        })


    @http.route(
        "/my_crm/customers/<int:customer_id>",
        type="http",
        auth="user",
        methods=["DELETE"],
        csrf=False
    )
    def delete_customer(self, customer_id):

        customer = request.env["my.crm.customer"].browse(customer_id)

        if not customer.exists():
            return request.make_json_response(
                {"error": "Customer not found"},
                status=404
            )

        customer.unlink()

        return request.make_json_response({
            "message": "Customer deleted successfully"
        })