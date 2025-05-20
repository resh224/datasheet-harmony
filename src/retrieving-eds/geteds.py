import requests
import json

# Replace this with the actual URI for the semiconductor part's JSON EDS
eds_uri = "https://example.com/semiconductor/part1234/eds.json"

# Optionally, set the Accept header to prefer JSON-LD if the server supports content negotiation
headers = {
    "Accept": "application/ld+json, application/json"
}

response = requests.get(eds_uri, headers=headers)

if response.status_code == 200:
    # Parse the JSON content
    eds_data = response.json()
    # Optionally, pretty-print the JSON-LD or JSON EDS
    print(json.dumps(eds_data, indent=2))
else:
    print(f"Failed to retrieve EDS. HTTP status code: {response.status_code}")
