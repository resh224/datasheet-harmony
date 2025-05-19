import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

def jsonld_to_jep30_xml(jsonld_str):
    # Parse JSON-LD input
    data = json.loads(jsonld_str)
    
    # Create root element with namespaces
    root = ET.Element("PartModel", 
        xmlns="http://jedec.org/ns/JEP30#",
        ComplianceToPartModelSchemaVersion="1.0",
        PartModelContentRevision="1.0")
    
    # Manufacturer-Array
    manufacturer_array = ET.SubElement(root, "Manufacturer-Array")
    manufacturer = ET.SubElement(manufacturer_array, "Manufacturer",
                                 ManufacturerID=data["manufacturer"]["manufacturerId"])
    ET.SubElement(manufacturer, "Name").text = data["manufacturer"]["name"]
    
    # ManufacturerPartNumber-Array
    mpn_array = ET.SubElement(root, "ManufacturerPartNumber-Array")
    mpn = ET.SubElement(mpn_array, "ManufacturerPartNumber",
                        PartNumber=data["mpn"])
    ET.SubElement(mpn, "BasePartNumber").text = data["mpn"]
    
    # PartDetails-Array
    part_details = ET.SubElement(root, "PartDetails-Array")
    part_assoc = ET.SubElement(part_details, "PartDetails")
    
    # Part basic information
    part_info = ET.SubElement(part_assoc, "Part",
        xmlns="http://jedec.org/ns/JEP30#",
        PartType=data["partType"],
        Status=data["status"])
    
    ET.SubElement(part_info, "Name").text = data["name"]
    ET.SubElement(part_info, "Description").text = data["description"]
    
    # Package information
    package = ET.SubElement(part_info, "Package")
    ET.SubElement(package, "PackageCode").text = data["package"]
    
    # Electrical characteristics (example)
    electrical = ET.SubElement(part_info, "ElectricalCharacteristics")
    ET.SubElement(electrical, "Capacitance", 
                  Value="10",
                  Unit="uF",
                  Tolerance="±10%")
    ET.SubElement(electrical, "VoltageRating", 
                  Value="16",
                  Unit="V")
    
    # Convert to pretty XML
    rough_xml = ET.tostring(root, 'utf-8')
    parsed = minidom.parseString(rough_xml)
    return parsed.toprettyxml(indent="  ")

# Example usage
jsonld_input = """{
    "@context": {
        "pm": "https://example.org/jedec/partmodel#",
        "schema": "https://schema.org/",
        "Manufacturer": "pm:Manufacturer",
        "ManufacturerPartNumber": "pm:ManufacturerPartNumber",
        "Part": "pm:Part",
        "name": "schema:name",
        "description": "schema:description",
        "mpn": "schema:mpn",
        "manufacturer": "schema:manufacturer",
        "partType": "pm:partType",
        "package": "pm:package",
        "status": "pm:status"
    },
    "@type": "Part",
    "name": "SMT Ceramic Chip Capacitor",
    "description": "10uF, 16V, X7R, 0805, ±10% tolerance",
    "mpn": "C0805C106K4RACTU",
    "manufacturer": {
        "@type": "Manufacturer",
        "name": "ACME Components Inc.",
        "manufacturerId": "ACME-001"
    },
    "partType": "Capacitor",
    "package": "0805",
    "status": "Active"
}"""

print(jsonld_to_jep30_xml(jsonld_input))
