import xml.etree.ElementTree as ET
import json

def xml_to_jsonld(xml_string):
    # Define namespaces
    ns = {'jep30': 'http://jedec.org/ns/JEP30#'}
    
    # Parse XML
    root = ET.fromstring(xml_string)
    
    # Extract Manufacturer
    manufacturer = root.find('.//jep30:Manufacturer', ns)
    manufacturer_data = {
        "@type": "Manufacturer",
        "manufacturerId": manufacturer.get('ManufacturerID'),
        "name": manufacturer.find('jep30:Name', ns).text
    }
    
    # Extract ManufacturerPartNumber
    mpn = root.find('.//jep30:ManufacturerPartNumber', ns)
    mpn_data = {
        "partNumber": mpn.get('PartNumber'),
        "basePartNumber": mpn.find('jep30:BasePartNumber', ns).text
    }
    
    # Extract Part Details
    part = root.find('.//jep30:Part', ns)
    electrical = part.find('jep30:ElectricalCharacteristics', ns)
    
    part_data = {
        "@type": "Part",
        "partType": part.get('PartType'),
        "status": part.get('Status'),
        "name": part.find('jep30:Name', ns).text,
        "description": part.find('jep30:Description', ns).text,
        "package": {
            "packageCode": part.find('.//jep30:PackageCode', ns).text
        },
        "electricalCharacteristics": {
            "capacitance": {
                "value": electrical.find('jep30:Capacitance', ns).get('Value'),
                "unit": electrical.find('jep30:Capacitance', ns).get('Unit'),
                "tolerance": electrical.find('jep30:Capacitance', ns).get('Tolerance')
            },
            "voltageRating": {
                "value": electrical.find('jep30:VoltageRating', ns).get('Value'),
                "unit": electrical.find('jep30:VoltageRating', ns).get('Unit')
            }
        }
    }
    
    # Build JSON-LD structure
    jsonld = {
        "@context": {
            "pm": "http://jedec.org/ns/JEP30#",
            "schema": "http://schema.org/",
            "Manufacturer": "pm:Manufacturer",
            "manufacturerId": "pm:manufacturerId",
            "partNumber": "pm:partNumber",
            "basePartNumber": "pm:basePartNumber",
            "Part": "pm:Part",
            "partType": "pm:partType",
            "status": "pm:status",
            "name": "schema:name",
            "description": "schema:description",
            "package": "pm:package",
            "electricalCharacteristics": "pm:electricalCharacteristics",
            "capacitance": "pm:capacitance",
            "voltageRating": "pm:voltageRating",
            "value": "pm:value",
            "unit": "pm:unit",
            "tolerance": "pm:tolerance"
        },
        "@graph": [
            {
                "@id": "urn:part:C0805C106K4RACTU",
                "@type": "Part",
                "manufacturer": manufacturer_data,
                "mpn": mpn_data,
                **part_data
            }
        ]
    }
    
    return jsonld

# Example usage
xml_data = '''<?xml version="1.0" ?>
<PartModel xmlns="http://jedec.org/ns/JEP30#" ComplianceToPartModelSchemaVersion="1.0" PartModelContentRevision="1.0">
  <Manufacturer-Array>
    <Manufacturer ManufacturerID="ACME-001">
      <Name>ACME Components Inc.</Name>
    </Manufacturer>
  </Manufacturer-Array>
  <ManufacturerPartNumber-Array>
    <ManufacturerPartNumber PartNumber="C0805C106K4RACTU">
      <BasePartNumber>C0805C106K4RACTU</BasePartNumber>
    </ManufacturerPartNumber>
  </ManufacturerPartNumber-Array>
  <PartDetails-Array>
    <PartDetails>
      <Part xmlns="http://jedec.org/ns/JEP30#" PartType="Capacitor" Status="Active">
        <Name>SMT Ceramic Chip Capacitor</Name>
        <Description>10uF, 16V, X7R, 0805, ±10% tolerance</Description>
        <Package>
          <PackageCode>0805</PackageCode>
        </Package>
        <ElectricalCharacteristics>
          <Capacitance Value="10" Unit="uF" Tolerance="±10%"/>
          <VoltageRating Value="16" Unit="V"/>
        </ElectricalCharacteristics>
      </Part>
    </PartDetails>
  </PartDetails-Array>
</PartModel>'''

result = xml_to_jsonld(xml_data)
print(json.dumps(result, indent=2))
