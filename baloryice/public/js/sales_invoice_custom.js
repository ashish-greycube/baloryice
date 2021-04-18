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

  validate: function (frm) {
    // return Promise.resolve();

    return new Promise((resolve, reject) => {
      let coords;

      frappe.db.get_value(
        "Customer",
        { name: frm.doc.customer },
        "is_freezer_location_verification_mandatory_cf",
        (r) => {
          if (cint(r.is_freezer_location_verification_mandatory_cf)) {
            if (!navigator.geolocation) {
              frappe.throw(__("Geolocation is not enabled."));
            } else {
              navigator.geolocation.getCurrentPosition(
                (loc) => {
                  coords = [loc.coords.latitude, loc.coords.longitude].join(
                    ","
                  );
                  frm.set_value("user_location_cf", coords);
                  resolve();
                },
                (err) => {
                  frappe.throw(err.message);
                  reject();
                  // frm.set_value("user_location_cf","12.884377599999999,80.2193408");
                  // resolve();
                }
              );
            }
          } else {
            resolve();
          }
        }
      );
    });
  },
});
