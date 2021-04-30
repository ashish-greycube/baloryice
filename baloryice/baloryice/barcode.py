from __future__ import unicode_literals
import frappe
from six import BytesIO
import barcode
from barcode.writer import ImageWriter
from frappe.utils import flt, cint


@frappe.whitelist(allow_guest=True)
def get_barcode(
    barcode_text="",
    code="code128",
    margin=6.5,
    height=15.0,
    write_text=True,
    background="white",
    foreground="black",
    font_size=12,
):
    """
    Returns barcode.png for barcode_text
    Usage: <site_url>/api/method/dotted_path_to.get_barcode"""

    buf = BytesIO()
    out = barcode.get(code, barcode_text, writer=ImageWriter()).write(
        buf,
        {
            # barcode options
            # https://python-barcode.readthedocs.io/en/stable/writers/index.html
            # The width of one barcode module in mm as float. Defaults to 0.2.
            "module_width": 0.2,
            # The height of the barcode modules in mm as float. Defaults to 15.0...26.46
            "module_height": flt(height),
            # Distance on the left and on the right from the border to the first (last) barcode module in mm as float. Defaults to 6.5.
            "quiet_zone": flt(margin),
            "font_size": font_size,
            # Do not print text below image
            "write_text": cint(write_text),
            "foreground": foreground,
            "background": background,
            # "text_distance": Distance between the barcode and the text under it in mm as float
        },
    )
    from werkzeug.wrappers import Response

    response = Response()
    response.mimetype = "image/png"
    response.data = buf.getvalue()
    return response