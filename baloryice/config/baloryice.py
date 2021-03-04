from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
    config = [
        {
            "label": _("Reports"),
            "items": [
                {
                    "type": "report",
                    "name": "Sales Partner Itemwise Profit",
                    "doctype": "Sales Invoice",
                    "is_query_report": True,
                },
            ],
        },
    ]
    return config
