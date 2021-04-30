frappe.ui.form.on("Item", {
  refresh: function (frm) {
    frm.page.add_inner_button(__("Print Label"), () => {
      let url = "/api/method/baloryice.baloryice.get_item_label",
        args = {
          docname: frm.doc.name,
        };
      open_url_post(url, args, true);
    });
  },
});
