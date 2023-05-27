import requests
import json
import datetime
import time

# Cisco vManage API endpoint and headers
url_templates = "https://<vmanage-ip>/dataservice/template/policy/security"
url_detach = "https://<vmanage-ip>/dataservice/template/policy/security/detach"
url_attach = "https://<vmanage-ip>/dataservice/template/policy/security/attach"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-viptela-session-token": "lkjkfd98y034pubtpeuagrW9fjkdjl",
}

# Device details
device_id = "<device-id>"

# Function to get the template ID based on template name
def get_template_id(template_name):
    response = requests.get(url_templates, headers=headers, verify=False)
    if response.status_code == 200:
        templates = response.json()
        for template in templates["data"]:
            if template["templateName"] == template_name:
                return template["templateId"]
    else:
        print("Error getting template IDs. Status code:", response.status_code)
        print("Response:", response.text)
    return None

# Detach and attach policy function
def detach_and_attach_policy(existing_policy_id, new_policy_id):
    # Request payload for detaching existing policy
    detach_payload = {
        "deviceTemplates": [
            {
                "templateId": existing_policy_id,
                "devices": [
                    {
                        "csv-status": "complete",
                        "csv-deviceId": device_id
                    }
                ]
            }
        ]
    }

    # Make the API call to detach existing policy
    response = requests.post(url_detach, headers=headers, data=json.dumps(detach_payload), verify=False)

    # Check the response status for detachment
    if response.status_code == 200:
        print("Existing security policy detached successfully.")
    else:
        print("Error detaching existing security policy. Status code:", response.status_code)
        print("Response:", response.text)
        return

    # Request payload for attaching new policy
    attach_payload = {
        "deviceTemplates": [
            {
                "templateId": new_policy_id,
                "devices": [
                    {
                        "csv-status": "complete",
                        "csv-deviceId": device_id
                    }
                ]
            }
        ]
    }

    # Make the API call to attach new policy
    response = requests.post(url_attach, headers=headers, data=json.dumps(attach_payload), verify=False)

    # Check the response status for attachment
    if response.status_code == 200:
        print("New security policy attached successfully.")
    else:
        print("Error attaching new security policy. Status code:", response.status_code)
        print("Response:", response.text)

# Calculate the next upcoming Friday at 6pm
today = datetime.date.today()
current_time = datetime.datetime.now().time()

# Check if today is Friday and the current time is before 6pm
if today.weekday() == 4 and current_time < datetime.time(18, 0):
    next_friday = today
else:
    days_ahead = (4 - today.weekday() + 7) % 7
    next_friday = today + datetime.timedelta(days=days_ahead)

target_time = datetime.datetime.combine(next_friday, datetime.time(18, 0))

# Wait until the target time
while datetime.datetime.now() < target_time:
    time.sleep(1)

# Get the IDs of the existing and new security policy templates
existing_policy_name = "<existing-policy-name>"
new_policy_name = "<new-policy-name>"

existing_policy_id = get_template_id(existing_policy_name)
new_policy_id = get_template_id(new_policy_name)

# Detach and attach the policies
if existing_policy_id and new_policy_id:
    detach_and_attach_policy(existing_policy_id, new_policy_id)
