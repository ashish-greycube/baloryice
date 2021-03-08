# Copyright (c) 2013, greycube.in and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import erpnext
import pandas
from six import string_types


def execute(filters=None):
    columns, data = get_data(filters)
    return columns, data


def get_data(filters=None):
    filters["group_by"] = "Invoice"

    from erpnext.accounts.report.gross_profit.gross_profit import execute

    invoices = frappe.db.sql(
        """
    select 
        si.name sales_invoice, si.sales_partner, si.company
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
    companies = set([d.company for d in invoices])
    sales_partners = {d["sales_invoice"]: d["sales_partner"] for d in invoices}

    gp_columns, gp_data = [], []

    for d in companies:
        filters["company"] = d
        _columns, _data = execute(filters)
        if _data:
            gp_data = gp_data + _data
        if _columns:
            gp_columns = _columns

    fields = [
        frappe.scrub(d.split(":")[0])
        if isinstance(d, string_types)
        else d.get("fieldname")
        for d in gp_columns
    ] + ["sales_partner"]

    for d in gp_data:
        d.append(sales_partners.get(d[0]))

    invoice_columns = [
        "parent",
        "customer",
        "customer_group",
        "posting_date",
        "item_code",
        "item_name",
        "item_group",
        "brand",
        "description",
        "warehouse",
        "qty",
        "base_rate",
        "buying_rate",
        "base_amount",
        "buying_amount",
        "gross_profit",
        "gross_profit_percent",
        "project",
    ]

    item_code = fields[invoice_columns.index("item_code")]
    item_name = fields[invoice_columns.index("item_name")]
    qty = fields[invoice_columns.index("qty")]
    selling_amount = fields[invoice_columns.index("base_amount")]
    buying_amount = fields[invoice_columns.index("buying_amount")]

    result = []

    if gp_data:
        df = pandas.DataFrame(gp_data, columns=fields)
        pt = pandas.pivot_table(
            df,
            index=["sales_partner", item_code, item_name],
            values=[qty, selling_amount, buying_amount],
            fill_value=0,
            aggfunc=sum,
            dropna=True,
        )
        df2 = pt.reset_index()
        result = df2.to_dict("r")

    for d in result:
        d["profit"] = d.get(selling_amount, 0) - d.get(buying_amount, 0)
        d["sales_unit"] = 0 if not d.get(qty) else d.get(selling_amount, 0) / d.get(qty)
        d["cost_unit"] = 0 if not d.get(qty) else d.get(buying_amount, 0) / d.get(qty)
        if d.get(buying_amount):
            d["profit_percent"] = d.get("profit") * 100 / d.get(buying_amount)

    columns = [
        item_code + ":Link/Item:280",
        qty + ":Float:90",
        "Sales Unit:Int:90",
        "Cost Unit:Int:90",
        selling_amount + ":Currency:130",
        buying_amount + ":Currency:130",
        "Profit:Currency:130",
        "Profit Percent:Float:130",
    ]

    return columns, result
