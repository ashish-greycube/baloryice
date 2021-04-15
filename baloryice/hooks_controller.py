# -*- coding: utf-8 -*-
# Copyright (c) 2021, greycube.in and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import cint
from math import radians, sin, cos, asin, sqrt
import json

_AVG_EARTH_RADIUS_M = 6371.0088 * 1000


def sales_invoice_validate(doc, method=None):
    # alert if Customer geolocation check is mandatory.
    if cint(
        frappe.db.get_value(
            "Customer", doc.customer, "is_freezer_location_verification_mandatory_cf"
        )
    ):
        if not doc.user_location_cf or not doc.freezer_cf:
            frappe.throw(_("User location and Freezer location is required."))

        distance = get_haversine(doc.user_location_cf, doc.freezer_cf)
        if distance > 250:
            frappe.throw(
                _(
                    "Freezer Location is not same as your location. You are {}m away from the Freezer."
                ).format(distance)
            )


def get_haversine(user_coords, freezer):
    import decimal

    lat1, lng1 = [decimal.Decimal(d) for d in user_coords.split(",")]
    freezer_location = frappe.db.get_value("Freezer", freezer, "freezer_location")
    if not freezer_location:
        frappe.throw("Please set a location for freezer %s" % freezer)

    freezer_location = json.loads(freezer_location)
    lng2, lat2 = [
        decimal.Decimal(d)
        for d in freezer_location["features"][0]["geometry"]["coordinates"]
    ]
    print(lat1, lng1, lat2, lng2)

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = radians(lat2)
    lng2 = radians(lng2)

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2

    return round(2 * _AVG_EARTH_RADIUS_M * asin(sqrt(d)))