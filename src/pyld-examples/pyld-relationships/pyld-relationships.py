import xml.etree.ElementTree as ET
import json

def xml_to_jsonld(xml_str):
    root = ET.fromstring(xml_str)
    
    # Define JSON-LD context
    context = {
        "@context": {
            "schema": "http://schema.org/",
            "jedec": "http://jedec.org/ns/JEP30#",
            "ipc": "http://ipc.org/ns/IPC-2581#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "id": "@id",
            "type": "@type",
            "ElectricalParameters": "jedec:ElectricalParameters",
            "symbol": "jedec:symbol",
            "value": {"@id": "jedec:value", "@type": "xsd:float"},
            "unit": "jedec:unit",
            "pcbAssembly": "ipc:pcbAssembly"
        }
    }

    # Extract data from XML
    part = {
        "@id": "urn:ti:dac3484",
        "@type": "schema:Product",
        "schema:name": root.find('.//jedec:Name', namespaces={'jedec': 'http://jedec.org/ns/JEP30#'}).text,
        "schema:manufacturer": {
            "@id": "urn:manufacturer:ti",
            "schema:name": root.find('.//jedec:Manufacturer/jedec:Name', namespaces={'jedec': 'http://jedec.org/ns/JEP30#'}).text
        },
        "jedec:partNumber": root.find('.//jedec:ManufacturerPartNumber', namespaces={'jedec': 'http://jedec.org/ns/JEP30#'}).get('PartNumber'),
        "ElectricalParameters": [],
        "pcbAssembly": {
            "@id": "urn:ipc:assembly123",
            "@type": "ipc:PCBAssembly",
            "ipc:file": "http://example.com/pcb/dac3484.xml",
            "ipc:standard": "IPC-2581B"
        }
    }

    # Add electrical parameters
    for param in root.findall('.//jedec:ElectricalParameters/jedec:Parameter', namespaces={'jedec': 'http://jedec.org/ns/JEP30#'}):
        part["ElectricalParameters"].append({
            "symbol": param.find('jedec:symbol', namespaces={'jedec': 'http://jedec.org/ns/JEP30#'}).text,
            "description": param.find('jedec:description', namespaces={'jedec': 'http://jedec.org/ns/JEP30#'}).text,
            "value": float(param.find('jedec:value', namespaces={'jedec': 'http://jedec.org/ns/JEP30#'}).text),
            "unit": param.find('jedec:unit', namespaces={'jedec': 'http://jedec.org/ns/JEP30#'}).text
        })

    # Build JSON-LD graph
    return {
        **context,
        "@graph": [
            part,
            {
                "@id": "urn:ipc:assembly123",
                "@type": "ipc:PCBAssembly",
                "ipc:layers": 8,
                "ipc:material": "FR-4",
                "ipc:thickness": {"@value": 1.6, "@type": "xsd:mm"},
                "ipc:referenceDesignator": "U1",
                "schema:manufacturer": {"@id": "urn:manufacturer:ti"}
            }
        ]
    }

# Example XML input (simplified)
xml_data = '''<?xml version="1.0"?>
<PartModel xmlns="http://jedec.org/ns/JEP30#">
  <Manufacturer>
    <Name>TEXAS INSTRUMENTS</Name>
  </Manufacturer>
  <ManufacturerPartNumber PartNumber="DAC3484IZAYR"/>
  <PartDetails>
    <Part>
      <Name>DAC3484 Quad-Channel DAC</Name>
      <ElectricalParameters>
        <Parameter>
          <symbol>IOUT_FS</symbol>
          <description>Full-scale output current</description>
          <value>20</value>
          <unit>mA</unit>
        </Parameter>
      </ElectricalParameters>
    </Part>
  </PartDetails>
</PartModel>'''

# Convert and print
result = xml_to_jsonld(xml_data)
print(json.dumps(result, indent=2))
