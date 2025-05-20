import json
from pyld import jsonld
from jsonschema import validate, ValidationError

# 1. Simulate retrieval of a JEDEC JEP30-compliant USB retimer part datasheet from JEDEC repository
# (In practice, you would fetch and parse XML/JSON from JEDEC; here we construct an example.)

jep30_part = {
    "@id": "urn:jecec:part:USBRetimer1234",
    "partNumber": "USBRetimer1234",
    "manufacturer": "ExampleSemi",
    "description": "USB 3.2/4 Retimer with Redriver",
    "classification": "IC",
    "electrical": {
        "supplyVoltage": {"min": 3.0, "max": 3.6, "unit": "V"},
        "supplyCurrent": {"typ": 120, "max": 150, "unit": "mA"},
        "powerConsumption": {"typ": 0.4, "max": 0.54, "unit": "W"},
        "dataRate": {"max": 20, "unit": "Gbps"},
        "operatingTemperature": {"min": -40, "max": 85, "unit": "C"}
    },
    "package": {
        "type": "QFN",
        "pins": 56,
        "dimensions": {"length": 7, "width": 7, "unit": "mm"}
    },
    "functions": [
        {"name": "Retimer", "description": "USB signal retiming"},
        {"name": "Redriver", "description": "USB signal redriving"}
    ]
}

# 2. Generate a JSON-LD context for the part (based on JEP30 concepts and common vocabularies)
jep30_context = {
    "@context": {
        "partNumber": "http://schema.org/Product/model",
        "manufacturer": "http://schema.org/manufacturer",
        "description": "http://schema.org/description",
        "classification": "http://schema.org/category",
        "electrical": "https://example.org/jedec/electrical",
        "supplyVoltage": "https://example.org/jedec/supplyVoltage",
        "supplyCurrent": "https://example.org/jedec/supplyCurrent",
        "powerConsumption": "https://example.org/jedec/powerConsumption",
        "dataRate": "https://example.org/jedec/dataRate",
        "operatingTemperature": "https://example.org/jedec/operatingTemperature",
        "package": "https://example.org/jedec/package",
        "type": "@type",
        "pins": "https://example.org/jedec/pins",
        "dimensions": "https://example.org/jedec/dimensions",
        "length": "https://schema.org/width",
        "width": "https://schema.org/height",
        "unit": "http://qudt.org/schema/qudt/unit",
        "functions": "https://example.org/jedec/functions",
        "name": "http://schema.org/name"
    }
}

# 3. Combine context and part into JSON-LD datasheet
jsonld_datasheet = {
    **jep30_context,
    **jep30_part
}

# 4. Validate JSON-LD using pyld (expand and compact as a form of structural validation)
try:
    expanded = jsonld.expand(jsonld_datasheet)
    compacted = jsonld.compact(expanded, jep30_context["@context"])
    print("JSON-LD validation (pyld) succeeded.\n")
except Exception as e:
    print("JSON-LD validation (pyld) failed:", e)
    compacted = None

# 5. Generate a JSON Schema from the JSON-LD structure (simplified for demonstration)
json_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "JEDEC JEP30 USB Retimer Part",
    "type": "object",
    "properties": {
        "@id": {"type": "string"},
        "partNumber": {"type": "string"},
        "manufacturer": {"type": "string"},
        "description": {"type": "string"},
        "classification": {"type": "string"},
        "electrical": {
            "type": "object",
            "properties": {
                "supplyVoltage": {
                    "type": "object",
                    "properties": {
                        "min": {"type": "number"},
                        "max": {"type": "number"},
                        "unit": {"type": "string"}
                    },
                    "required": ["min", "max", "unit"]
                },
                "supplyCurrent": {
                    "type": "object",
                    "properties": {
                        "typ": {"type": "number"},
                        "max": {"type": "number"},
                        "unit": {"type": "string"}
                    },
                    "required": ["typ", "max", "unit"]
                },
                "powerConsumption": {
                    "type": "object",
                    "properties": {
                        "typ": {"type": "number"},
                        "max": {"type": "number"},
                        "unit": {"type": "string"}
                    },
                    "required": ["typ", "max", "unit"]
                },
                "dataRate": {
                    "type": "object",
                    "properties": {
                        "max": {"type": "number"},
                        "unit": {"type": "string"}
                    },
                    "required": ["max", "unit"]
                },
                "operatingTemperature": {
                    "type": "object",
                    "properties": {
                        "min": {"type": "number"},
                        "max": {"type": "number"},
                        "unit": {"type": "string"}
                    },
                    "required": ["min", "max", "unit"]
                }
            },
            "required": ["supplyVoltage", "supplyCurrent", "powerConsumption", "dataRate", "operatingTemperature"]
        },
        "package": {
            "type": "object",
            "properties": {
                "type": {"type": "string"},
                "pins": {"type": "integer"},
                "dimensions": {
                    "type": "object",
                    "properties": {
                        "length": {"type": "number"},
                        "width": {"type": "number"},
                        "unit": {"type": "string"}
                    },
                    "required": ["length", "width", "unit"]
                }
            },
            "required": ["type", "pins", "dimensions"]
        },
        "functions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["name", "description"]
            }
        }
    },
    "required": ["@id", "partNumber", "manufacturer", "description", "classification", "electrical", "package", "functions"]
}

# 6. Validate the JSON-LD datasheet against the generated JSON Schema
try:
    validate(instance=jep30_part, schema=json_schema)
    print("JSON Schema validation succeeded.\n")
except ValidationError as e:
    print("JSON Schema validation failed:", e)

# 7. Print all artifacts
print("\n--- JSON-LD Context ---")
print(json.dumps(jep30_context, indent=2))

print("\n--- JSON-LD Datasheet ---")
print(json.dumps(jsonld_datasheet, indent=2))

print("\n--- JSON-LD Expanded (pyld) ---")
print(json.dumps(expanded, indent=2))

print("\n--- JSON Schema ---")
print(json.dumps(json_schema, indent=2))

print("\n--- JSON-LD Compacted (pyld) ---")
print(json.dumps(compacted, indent=2))
