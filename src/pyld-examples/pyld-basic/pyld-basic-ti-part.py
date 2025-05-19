"""
JSON-LD Processing Demo for Texas Instruments DAC3484 using PyLD
"""

from pyld import jsonld
import json

# Define JSON-LD Context for electronic components
context = {
    "@context": {
        "schema": "http://schema.org/",
        "jedec": "http://jedec.org/ns/JEP30#",
        "id": "@id",
        "type": "@type",
        "name": "schema:name",
        "manufacturer": "schema:manufacturer",
        "partNumber": "jedec:partNumber",
        "description": "schema:description",
        "package": {
            "@id": "jedec:package",
            "@type": "@id"
        },
        "supplyVoltage": {
            "@id": "jedec:supplyVoltage",
            "@type": "schema:QuantitativeValue"
        }
    }
}

# Sample DAC3484 data in expanded JSON-LD format
dac_data = {
    "@id": "urn:ti:DAC3484IZAYR",
    "@type": "schema:Product",
    "schema:name": "DAC3484 Quad-Channel 16-Bit DAC",
    "schema:manufacturer": {
        "@id": "urn:ti",
        "schema:name": "Texas Instruments"
    },
    "jedec:partNumber": "DAC3484IZAYR",
    "schema:description": "1.25 GSPS Digital-to-Analog Converter",
    "jedec:package": {
        "@id": "urn:package:NFBGA-196",
        "schema:name": "196-ball NFBGA package"
    },
    "jedec:supplyVoltage": {
        "schema:minValue": 3.135,
        "schema:maxValue": 3.465,
        "schema:unitText": "V"
    }
}

def process_dac_data():
    try:
        # 1. Compact the JSON-LD using our context
        compacted = jsonld.compact(dac_data, context["@context"])
        print("Compacted JSON-LD:\n")
        print(json.dumps(compacted, indent=2))

        # 2. Expand to show full JSON-LD structure
        expanded = jsonld.expand(compacted)
        print("\nExpanded JSON-LD:\n")
        print(json.dumps(expanded, indent=2))

        # 3. Normalize to RDF N-Quads
        normalized = jsonld.normalize(dac_data, {'format': 'application/n-quads'})
        print("\nNormalized RDF (N-Quads):\n")
        print(normalized)

    except Exception as e:
        print(f"Error processing JSON-LD: {str(e)}")

if __name__ == "__main__":
    process_dac_data()
