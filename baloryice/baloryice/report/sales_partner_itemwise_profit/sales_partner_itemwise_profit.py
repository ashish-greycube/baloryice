# Copyright (c) 2013, greycube.in and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import erpnext
import pandas
from six import string_types


def execute(filters=None):
    columns, data = get_data(filters)
    return columns, data


def get_data(filters=None):
    filters["group_by"] = "Invoice"

    from erpnext.accounts.report.gross_profit.gross_profit import execute

    gp_columns, gp_data = execute(filters)
    fields = [
        frappe.scrub(d.split(":")[0])
        if isinstance(d, string_types)
        else d.get("fieldname")
        for d in gp_columns
    ] + ["sales_partner"]

    sales_partners = frappe.db.sql(
        """
    select 
        si.name sales_invoice, sales_partner
    from 
        `tabSales Invoice` si
    where 
        si.docstatus = 1
        and si.posting_date between %(from_date)s and %(to_date)s
        and si.sales_partner = %(sales_partner)s
    """,
        filters,
        as_dict=True,
    )
    sales_partners = {d["sales_invoice"]: d["sales_partner"] for d in sales_partners}
    for d in gp_data:
        d.append(sales_partners.get(d[0]))

    df = pandas.DataFrame(gp_data, columns=fields)
    pt = pandas.pivot_table(
        df,
        index=["sales_partner", "item_code", "item_name"],
        values=[
            "qty",
            "selling_amount",
            "buying_amount",
        ],
        fill_value=0,
        aggfunc=sum,
        dropna=True,
    )
    df2 = pt.reset_index()
    result = df2.to_dict("r")

    for d in result:
        d["profit"] = d.get("selling_amount", 0) - d.get("buying_amount", 0)
        d["sales_unit"] = (
            0 if not d.get("qty") else d.get("selling_amount", 0) / d.get("qty")
        )
        d["cost_unit"] = (
            0 if not d.get("qty") else d.get("buying_amount", 0) / d.get("qty")
        )
        if d.get("buying_amount"):
            d["profit_percent"] = d.get("profit") * 100 / d.get("buying_amount")

    columns = [
        "Item Code:Link/Item:280",
        "Qty:Float:90",
        "Sales Unit:Int:90",
        "Cost Unit:Int:90",
        "Selling Amount:Currency:130",
        "Buying Amount:Currency:130",
        "Profit:Currency:130",
        "Profit Percent:Float:130",
    ]

    return columns, result
