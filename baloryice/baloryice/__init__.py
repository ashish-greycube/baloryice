# -*- coding: utf-8 -*-
# Copyright (c) 2021, greycube.in and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.utils.pdf import get_pdf
from frappe.model.document import Document

pdf_options = {
    # set margins
    "margin-left": "0.1mm",
    "margin-right": "2.5mm",  # from 4
    "margin-top": "0.1mm",  # 3.1
    "margin-bottom": "0.1mm",
    # "orientation": "Portrait",
    "orientation": "Landscape",
    "page-height": "5.7cm",
    "page-width": "4.3cm",
    # "outline": True,
    "no-outline": None,
}


@frappe.whitelist()
def get_item_label(docname):
    doc = frappe.db.get_values(
        "Item",
        docname,
        ["item_name", "item_code"],
        as_dict=True,
    )[0]
    html = frappe.render_template("templates/pages/item_label.html", dict(doc=doc))
    frappe.local.response.filename = f"Item_{doc.item_code}_label.pdf"
    frappe.local.response.filecontent = get_pdf(html, pdf_options)
    frappe.local.response.type = "download"
