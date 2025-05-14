import requests
import json
import os

url = "https://chatiqnet.rcqatol.com/25-5-0/openaibot/ai/propertysummary"

headers = {
    "Content-Type": "application/json",
    # "Cookie": "__cf_bm=3.bcfVIKZkwvPbrTmj3KGAQm2fqfryjo19ecerVOgKE-1747202326-1.0.1.1-ekARfgVDhWCk7e8RnWskZxf0OlL2HIdWgfB46qw4P9wDhpmDlh._NSfaDcA2VeCRDaQmKJxaUdKaNMuTfsLt3rnHZUd1EILbhi7Di2FlXrE; BIGipServerpRentCafeAPIQA.com-tanzu=1396569610.20480.0000"
}
# 510835
# 506589
object_id = "510835"
payload = {
    "objecttype": "3",
    "objectid": object_id,
    "QueryText": "propertyinfo"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    response_json = response.json()

    # Specify the path where you want to save the JSON file
    output_dir = r"C:\Users\dm35820\assignment_2\office_mcp"  

    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    filename = f"property_response_{object_id}.json"
    output_path = os.path.join(output_dir, filename)
    # Write the JSON response to the file
    with open(output_path, "w") as f:
        json.dump(response_json, f, indent=4)

    print(f"Response saved to: {output_path}")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text) 
