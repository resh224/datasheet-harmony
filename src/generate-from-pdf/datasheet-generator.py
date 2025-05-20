import json
from pyld import jsonld
from jsonschema import validate, ValidationError

# 1. Manually map DAC3484-Markup.pdf fields to JEDEC JEP30 structure (as per JEP30-E100G)
dac3484_jep30 = {
    "@id": "urn:ti:part:DAC3484",
    "manufacturer": "Texas Instruments",
    "manufacturerPartNumber": "DAC3484",
    "description": "Quad-Channel, 16-Bit, 1.25 GSPS Digital-to-Analog Converter",
    "partClassification": [
        {
            "class": "IC",
            "category": "Data Converter",
            "subcategory": "DAC"
        }
    ],
    "package": {
        "type": "WQFN",
        "pinCount": 88,
        "bodySize": {"length": 9.0, "width": 9.0, "unit": "mm"}
    },
    "electrical": {
        "supplyVoltage": {"min": 1.14, "max": 1.26, "unit": "V"},
        "supplyCurrent": {"typ": 1200, "unit": "mA"},
        "powerConsumption": {"typ": 1.27, "unit": "W"},
        "resolution": 16,
        "sampleRate": {"max": 1.25, "unit": "GSPS"},
        "operatingTemperature": {"min": -40, "max": 85, "unit": "C"}
    },
    "functions": [
        {"name": "DAC", "description": "Digital-to-Analog Converter"},
        {"name": "Interpolation", "description": "2x/4x/8x/16x interpolation filter"},
        {"name": "Complex Mixing", "description": "On-chip complex mixers"}
    ]
}

# 2. Generate JSON-LD context (based on JEP30 concepts and schema.org)
jep30_context = {
    "@context": {
        "manufacturer": "http://schema.org/manufacturer",
        "manufacturerPartNumber": "http://schema.org/Product/model",
        "description": "http://schema.org/description",
        "partClassification": "https://example.org/jedec/partClassification",
        "class": "http://schema.org/category",
        "category": "http://schema.org/category",
        "subcategory": "http://schema.org/category",
        "package": "https://example.org/jedec/package",
        "type": "@type",
        "pinCount": "https://example.org/jedec/pinCount",
        "bodySize": "https://example.org/jedec/bodySize",
        "length": "https://schema.org/width",
        "width": "https://schema.org/height",
        "unit": "http://qudt.org/schema/qudt/unit",
        "electrical": "https://example.org/jedec/electrical",
        "supplyVoltage": "https://example.org/jedec/supplyVoltage",
        "supplyCurrent": "https://example.org/jedec/supplyCurrent",
        "powerConsumption": "https://example.org/jedec/powerConsumption",
        "resolution": "https://example.org/jedec/resolution",
        "sampleRate": "https://example.org/jedec/sampleRate",
        "operatingTemperature": "https://example.org/jedec/operatingTemperature",
        "functions": "https://example.org/jedec/functions",
        "name": "http://schema.org/name"
    }
}

# 3. Combine context and part into JSON-LD datasheet
jsonld_datasheet = {
    **jep30_context,
    **dac3484_jep30
}

# 4. Validate JSON-LD using pyld (expand and compact)
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
    "title": "JEDEC JEP30 DAC3484 Electronic Datasheet",
    "type": "object",
    "properties": {
        "@id": {"type": "string"},
        "manufacturer": {"type": "string"},
        "manufacturerPartNumber": {"type": "string"},
        "description": {"type": "string"},
        "partClassification": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "class": {"type": "string"},
                    "category": {"type": "string"},
                    "subcategory": {"type": "string"}
                },
                "required": ["class", "category", "subcategory"]
            }
        },
        "package": {
            "type": "object",
            "properties": {
                "type": {"type": "string"},
                "pinCount": {"type": "integer"},
                "bodySize": {
                    "type": "object",
                    "properties": {
                        "length": {"type": "number"},
                        "width": {"type": "number"},
                        "unit": {"type": "string"}
                    },
                    "required": ["length", "width", "unit"]
                }
            },
            "required": ["type", "pinCount", "bodySize"]
        },
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
                        "unit": {"type": "string"}
                    },
                    "required": ["typ", "unit"]
                },
                "powerConsumption": {
                    "type": "object",
                    "properties": {
                        "typ": {"type": "number"},
                        "unit": {"type": "string"}
                    },
                    "required": ["typ", "unit"]
                },
                "resolution": {"type": "integer"},
                "sampleRate": {
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
            "required": ["supplyVoltage", "supplyCurrent", "powerConsumption", "resolution", "sampleRate", "operatingTemperature"]
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
    "required": [
        "@id", "manufacturer", "manufacturerPartNumber", "description",
        "partClassification", "package", "electrical", "functions"
    ]
}

# 6. Validate the JSON-LD datasheet against the generated JSON Schema
try:
    validate(instance=dac3484_jep30, schema=json_schema)
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
