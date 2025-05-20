import requests
import json
import jsonschema
from jsonschema import validate, ValidationError
import logging
from urllib.parse import urlparse
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EDSValidator:
    """Class to retrieve and validate JSON Electronic Datasheets (EDS) for semiconductor parts."""
    
    def __init__(self, schema_uri=None, eds_uri=None):
        """Initialize with optional schema and EDS URIs."""
        self.schema_uri = schema_uri
        self.eds_uri = eds_uri
        self.schema = None
        self.eds_data = None
        
    def retrieve_schema(self, schema_uri=None):
        """Retrieve JSON Schema from the provided URI."""
        uri = schema_uri or self.schema_uri
        if not uri:
            raise ValueError("Schema URI must be provided")
        
        logger.info(f"Retrieving schema from: {uri}")
        
        try:
            # Handle both HTTP/HTTPS and file URIs
            if uri.startswith(('http://', 'https://')):
                response = requests.get(uri, headers={"Accept": "application/schema+json, application/json"})
                response.raise_for_status()
                self.schema = response.json()
            elif uri.startswith('file://'):
                path = urlparse(uri).path
                with open(path, 'r') as f:
                    self.schema = json.load(f)
            else:
                # Assume local file path
                with open(uri, 'r') as f:
                    self.schema = json.load(f)
                    
            logger.info("Schema retrieved successfully")
            return self.schema
            
        except (requests.RequestException, json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to retrieve schema: {str(e)}")
            raise
    
    def retrieve_eds(self, eds_uri=None):
        """Retrieve JSON EDS from the provided URI."""
        uri = eds_uri or self.eds_uri
        if not uri:
            raise ValueError("EDS URI must be provided")
        
        logger.info(f"Retrieving EDS from: {uri}")
        
        try:
            # Handle both HTTP/HTTPS and file URIs
            if uri.startswith(('http://', 'https://')):
                # Set appropriate headers for JSON-LD or standard JSON
                headers = {
                    "Accept": "application/ld+json, application/json"
                }
                response = requests.get(uri, headers=headers)
                response.raise_for_status()
                self.eds_data = response.json()
            elif uri.startswith('file://'):
                path = urlparse(uri).path
                with open(path, 'r') as f:
                    self.eds_data = json.load(f)
            else:
                # Assume local file path
                with open(uri, 'r') as f:
                    self.eds_data = json.load(f)
                    
            logger.info("EDS retrieved successfully")
            return self.eds_data
            
        except (requests.RequestException, json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to retrieve EDS: {str(e)}")
            raise
    
    def validate_eds(self, eds_data=None, schema=None):
        """Validate the EDS data against the schema."""
        eds = eds_data or self.eds_data
        schema_to_use = schema or self.schema
        
        if not eds:
            raise ValueError("EDS data must be provided or retrieved first")
        if not schema_to_use:
            raise ValueError("Schema must be provided or retrieved first")
        
        logger.info("Validating EDS against schema...")
        
        try:
            validate(instance=eds, schema=schema_to_use)
            logger.info("EDS validation successful")
            return True
        except ValidationError as e:
            logger.error(f"EDS validation failed: {str(e)}")
            # Provide more detailed validation error information
            logger.error(f"Error path: {' -> '.join([str(p) for p in e.path])}")
            logger.error(f"Error schema path: {' -> '.join([str(p) for p in e.schema_path])}")
            return False
    
    def check_spdx_compliance(self, eds_data=None):
        """Check if the EDS complies with SPDX 3.0 standards."""
        eds = eds_data or self.eds_data
        
        if not eds:
            raise ValueError("EDS data must be provided or retrieved first")
        
        logger.info("Checking SPDX compliance...")
        
        # Basic SPDX compliance checks
        spdx_compliant = True
        
        # Check for SPDX context if it's JSON-LD
        if '@context' in eds and 'https://spdx.org/rdf/3.0.1/spdx-context.jsonld' not in str(eds['@context']):
            logger.warning("Missing SPDX 3.0.1 context in JSON-LD document")
            spdx_compliant = False
        
        # Check for required SPDX fields (simplified check)
        required_fields = ['spdxId', 'creationInfo']
        for field in required_fields:
            if field not in eds:
                logger.warning(f"Missing required SPDX field: {field}")
                spdx_compliant = False
        
        if spdx_compliant:
            logger.info("EDS appears to be SPDX compliant")
        else:
            logger.warning("EDS may not be fully SPDX compliant")
            
        return spdx_compliant
    
    def check_jedec_compliance(self, eds_data=None):
        """Check if the EDS complies with JEDEC JEP30 standards."""
        eds = eds_data or self.eds_data
        
        if not eds:
            raise ValueError("EDS data must be provided or retrieved first")
        
        logger.info("Checking JEDEC JEP30 compliance...")
        
        # Basic JEDEC compliance checks
        jedec_compliant = True
        
        # Check for PartModel structure as per JEP30
        if 'PartModel' not in eds:
            logger.warning("Missing PartModel structure required by JEDEC JEP30")
            jedec_compliant = False
        else:
            # Check for manufacturer information
            if 'Manufacturer' not in eds['PartModel']:
                logger.warning("Missing Manufacturer information required by JEDEC JEP30")
                jedec_compliant = False
        
        if jedec_compliant:
            logger.info("EDS appears to be JEDEC JEP30 compliant")
        else:
            logger.warning("EDS may not be fully JEDEC JEP30 compliant")
            
        return jedec_compliant
    
    def save_eds(self, filepath, eds_data=None):
        """Save the EDS data to a local file."""
        eds = eds_data or self.eds_data
        
        if not eds:
            raise ValueError("EDS data must be provided or retrieved first")
        
        try:
            with open(filepath, 'w') as f:
                json.dump(eds, f, indent=2)
            logger.info(f"EDS saved to {filepath}")
            return True
        except IOError as e:
            logger.error(f"Failed to save EDS: {str(e)}")
            return False

def main():
    """Main function to demonstrate the EDS validator."""
    # Example URIs - replace with actual URIs
    schema_uri = "https://spdx.org/schema/3.0.1/spdx-json-schema.json"
    eds_uri = "https://example.com/semiconductor/part1234/eds.json"
    
    # Create validator instance
    validator = EDSValidator(schema_uri, eds_uri)
    
    try:
        # Retrieve schema and EDS
        schema = validator.retrieve_schema()
        eds_data = validator.retrieve_eds()
        
        # Validate EDS against schema
        is_valid = validator.validate_eds()
        
        if is_valid:
            # Check compliance with standards
            spdx_compliant = validator.check_spdx_compliance()
            jedec_compliant = validator.check_jedec_compliance()
            
            # Save validated EDS locally
            validator.save_eds("validated_eds.json")
            
            print("\nValidation Summary:")
            print(f"Schema validation: {'✓ Passed' if is_valid else '✗ Failed'}")
            print(f"SPDX compliance: {'✓ Compliant' if spdx_compliant else '⚠ May not be fully compliant'}")
            print(f"JEDEC compliance: {'✓ Compliant' if jedec_compliant else '⚠ May not be fully compliant'}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
