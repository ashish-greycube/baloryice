// Copyright (c) 2016, greycube.in and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports['Customers Without Any Sales Transactions'] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            reqd: 1,
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -3),
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.get_today(),
        },
    ],

    onload: function (report) {
        //
    },
};
