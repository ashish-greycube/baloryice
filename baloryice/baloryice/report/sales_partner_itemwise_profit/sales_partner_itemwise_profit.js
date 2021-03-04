// Copyright (c) 2016, greycube.in and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Partner Itemwise Profit"] = {
  filters: [
    {
      fieldname: "from_date",
      label: __("From Date"),
      fieldtype: "Date",
      reqd: 1,
      default: frappe.defaults.get_user_default("year_start_date"),
    },
    {
      fieldname: "to_date",
      label: __("To Date"),
      fieldtype: "Date",
      reqd: 1,
      default: frappe.defaults.get_user_default("year_end_date"),
    },
    {
      fieldname: "sales_partner",
      label: __("Sales Partner"),
      fieldtype: "Link",
      options: "Sales Partner",
      reqd: 1,
    },
  ],

  onload: function (report) {
    //
  },
};
