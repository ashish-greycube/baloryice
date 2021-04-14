# -*- coding: utf-8 -*-
# Copyright (c) 2021, greycube.in and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.utils import cint


def sales_invoice_validate(doc, method=None):
    # alert if Customer geolocation check is mandatory.
    if not cint(
        frappe.db.get_value(
            "Customer", doc.customer, "is_freezer_location_verification_mandatory_cf"
        )
    ):
        pass
    # msg = "Freezer Location is not same as your location"