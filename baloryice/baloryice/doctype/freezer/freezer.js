// Copyright (c) 2021, greycube.in and contributors
// For license information, please see license.txt

frappe.ui.form.on("Freezer", {
  refresh: function (frm) {
    frm.fields_dict["freezer_barcode"].$input
      .prop("disabled", true)
      .toggle(false);
  },
});
