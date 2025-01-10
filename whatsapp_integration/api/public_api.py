import frappe
import json


@frappe.whitelist(allow_guest=True)
def webhook():
    if frappe.request.method == 'POST':
        data = frappe.request.data or "No Data"
        # Log or process the received message here
        frappe.log_error(message=data, title="WhatsApp Webhook Data")

        return {"status": "success"}
    else:
        return {"status": "Make post request"}


