# import frappe
# import json


# @frappe.whitelist(allow_guest=True)
# def webhook():
#     if frappe.request.method == 'POST':
#         data = frappe.request.data or "No Data"
#         # Log or process the received message here
#         frappe.log_error(message=data, title="WhatsApp Webhook Data")

#         return {"status": "success"}
#     else:
#         return {"status": "Make post request"}



import frappe
import requests
import json



@frappe.whitelist(allow_guest=True)
def webhook():
    if frappe.request.method == "GET":
        # Get the query parameters
        mode = frappe.local.request.args.get("hub.mode")
        token = frappe.local.request.args.get("hub.verify_token")
        challenge = frappe.local.request.args.get("hub.challenge")
        
        # Log verification attempt
        frappe.log_error(
            message=f"Mode: {mode}, Token: {token}, Challenge: {challenge}",
            title="WhatsApp Verification Attempt"
        )
        
        # Verify the token
        if mode == "subscribe" and token == "TCBInfotech":
            frappe.response.http_status_code = 200
            return str(challenge)
        
        frappe.throw("Failed verification")
    
    elif frappe.request.method == "POST":
        try:
            # Get the webhook data
            data = json.loads(frappe.request.data)
            frappe.log_error(message=data, title="WhatsApp Webhook Data")
            
            # Return 200 OK
            frappe.response.http_status_code = 200
            return {"status": "success"}
            
        except Exception as e:
            frappe.log_error(f"Error processing webhook: {str(e)}", "Webhook Error")
            frappe.response.http_status_code = 200
            return {"status": "success"}
    
    else:
        return {"status": "Method not allowed"}


@frappe.whitelist()
def send_whatsapp_message(doc, method=None):
    """
    This function will be triggered on submit of Send Message doctype
    """
    try:
        # WhatsApp API configuration
        whatsapp_config = {
            "api_url": "https://graph.facebook.com/v21.0/533781416487678/messages",
            "access_token": "EAAHIBQatcf8BOZBBNsdZAGHPfDMoI8NLRB7RMMxRMThaT7Tw6nY6eFC2ZCNkDh0trvMEFVZBFPvZBTYknVPcuV7G4neMGRBOh4iznDLrqTAuGFbZBPoaMVlBVa4NXX9QYKj9psPdk16IDZB0ZA67wUZCO2PyzrnhvPweSoNYtJzixuTZC5MctevNt50Ku399ZBV3Rxxpyq0B1dpSKjGJibbXTMr2PpMYLxcMsGmkHIZD"
        }
        
        # Prepare the message payload
        payload = {
            "messaging_product": "whatsapp",
            "to": "918168152757",  # Get from your doctype
            "type": "template",
            "template": {
                "name": "hello_world",  # Your template name
                "language": {
                    "code": "en_US"
                }
            }
        }
        
        # If you want to send custom message instead of template
        # payload = {
        #     "messaging_product": "whatsapp",
        #     "to": "918168152757",
        #     "type": "text",
        #     "text": {
        #         "body": "Whats App Integration With Frappe. Hello World !!"
        #     }
        # }
        
        # Send request to WhatsApp API
        response = requests.post(
            whatsapp_config["api_url"],
            headers={
                "Authorization": f"Bearer {whatsapp_config['access_token']}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        
        # Log the response
        frappe.log_error(
            message=f"Response: {response.text}",
            title="WhatsApp Message Sent"
        )
        
        if response.status_code != 200:
            frappe.throw("Failed to send WhatsApp message")
            
    except Exception as e:
        frappe.log_error(
            message=f"Error sending WhatsApp message: {str(e)}",
            title="WhatsApp Send Error"
        )
        frappe.throw("Failed to send WhatsApp message")

