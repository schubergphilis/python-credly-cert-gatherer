import requests

url = input("Url of group including json ")
#     "https://www.credly.com/organizations/amazon-web-services/collections/aws-certification-program-private-collection/badge_templates.json"
data = requests.get(url).json()


certs = []
for item in data["data"]:
    cert_id = item["id"]
    cert_name = item["name"]
    certs.append({"cert_id": cert_id, "cert_name": cert_name})

for cert in certs:
    print(f"{cert['cert_id']},{cert['cert_name']}")
