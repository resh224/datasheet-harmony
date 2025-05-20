- **Defines a Multi-Standard JSON-LD Context:**
  The program creates a JSON-LD context that integrates vocabulary from JEDEC JEP30 (electrical data), SPDX (BOM and licensing), and IPC-2581 (PCB assembly).
- **Models an Embedded Controller Dataset:**
  It constructs a JSON-LD document for an embedded controller, including electrical characteristics (JEP30), BOM components with licenses (SPDX), and PCB stackup/placement details (IPC-2581).
- **Expands and Compacts JSON-LD:**
  Uses the `pyld` library to expand and compact the JSON-LD document, ensuring the relationships and context are correctly interpreted semantically.
- **Builds a Knowledge Graph:**
  Loads the expanded JSON-LD into an RDF graph using `rdflib`, enabling semantic queries and graph traversal across the combined standards.
- **Performs Graph Traversal:**
  Traverses the RDF graph to identify and print relationships between the embedded controller, its BOM components, their licenses, and PCB assembly layers.
- **Executes a SPARQL Query:**
  Runs a SPARQL query to extract cross-standard relationships, such as linking components to their licenses and physical PCB layers.
- **Demonstrates Interoperability:**
  Shows how data from JEDEC JEP30, SPDX, and IPC-2581 can be connected, queried, and traversed as a unified, standards-based knowledge graph for an electronic part.
