// Copyright (c) 2021, greycube.in and contributors
// For license information, please see license.txt

frappe.ui.form.on("Freezer", {
  setup: function (frm) { },

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

  set_freezer_location: function name(frm) {
    const zoom = 15;
    let fld = frm.get_field("freezer_location"),
      _map = fld.map;

    let lat_long = /\/\@(.*),(.*),/.exec(frm.doc.freezer_google_location_url);

    if (lat_long && lat_long.length == 3) {
      var geojsonFeature = {
        type: "Feature",
        properties: {
          name: "Freezer Location",
          popupContent: "This is the freezer's location",
        },
        geometry: {
          type: "Point",
          coordinates: lat_long.slice(1).reverse(),
        },
      };
      let layer = L.geoJSON(geojsonFeature);
      layer.addTo(_map);
      fld.editableLayers.addLayer(layer);
      fld.set_value(JSON.stringify(fld.editableLayers.toGeoJSON()));
    } else {
      frappe.throw(
        __(
          `The url does not contain valid longitide, latitude. (e.g. /@24.645284,46.7002566,17z/) 
          Please paste a google map link url in the Client Location Url in order to set marker.`
        )
      );
    }
  },
});
