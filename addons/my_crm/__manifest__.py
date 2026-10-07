{
    "name": "My CRM",
    "version": "1.0",
    "category": "CRM",
    "summary": "My first CRM module",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/customer_views.xml",
        "views/opportunity_views.xml",
        "views/stage_views.xml",
        "views/opportunity_won_wizard_views.xml",
    ],
    "installable": True,
    "application": True,
}