frappe.ui.form.on("Sales Invoice", {
  setup: function (frm) {
    frm.set_query("freezer_cf", function () {
      return {
        filters: {
          customer_name: frm.doc.customer,
        },
      };
    });
  },
});
