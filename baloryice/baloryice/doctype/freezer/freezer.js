// Copyright (c) 2021, greycube.in and contributors
// For license information, please see license.txt

frappe.ui.form.on("Freezer", {
  setup: function (frm) {},

  refresh: function (frm) {
    frm.fields_dict["freezer_barcode"].$input
      .prop("disabled", true)
      .toggle(false);

    frm.page.add_inner_button(__("Print Label"), () => {
      let url =
          "/api/method/baloryice.baloryice.doctype.freezer.freezer.get_label",
        args = {
          docname: frm.doc.name,
        };
      open_url_post(url, args, true);
    });
  },
});
