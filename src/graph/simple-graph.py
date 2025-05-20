import json
from pyld import jsonld
import networkx as nx
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

# Define namespaces for standards
JEDEC = Namespace("https://jedec.org/ns/jep30#")
SPDX = Namespace("http://spdx.org/rdf/terms#")
IPC = Namespace("https://ipc.org/ns/2581#")
SCHEMA = Namespace("http://schema.org/")

# Create JSON-LD context for multi-standard interoperability
multistandard_context = {
    "@context": {
        "jedec": str(JEDEC),
        "spdx": str(SPDX),
        "ipc": str(IPC),
        "schema": str(SCHEMA),
        "GraphTraversal": {
            "@id": "ipc:GraphTraversal",
            "@type": "@id"
        }
    }
}

# Sample embedded controller data using JEP30, SPDX and IPC-2581
embedded_controller = {
    "@id": "urn:embedded-controller:ec123",
    "@type": ["jedec:EmbeddedController", "spdx:Package", "ipc:Assembly"],
    "schema:name": "XC2344 Embedded Controller",
    "schema:manufacturer": "ExampleSemiconductor",
    
    # JEP30 Electrical characteristics
    "jedec:electrical": {
        "jedec:supplyVoltage": {"min": 1.8, "max": 3.3, "unit": "V"},
        "jedec:operatingFrequency": {"max": 200, "unit": "MHz"}
    },
    
    # SPDX BOM components
    "spdx:hasFile": [
        {
            "@id": "urn:component:cpu-core",
            "@type": "spdx:File",
            "spdx:licenseConcluded": "Apache-2.0",
            "ipc:placement": {"x": 12.5, "y": 8.3, "layer": "Top"}
        },
        {
            "@id": "urn:component:flash-mem",
            "@type": "spdx:File",
            "spdx:licenseConcluded": "GPL-3.0",
            "ipc:placement": {"x": 5.7, "y": 3.2, "layer": "Bottom"}
        }
    ],
    
    # IPC-2581 Assembly details
    "ipc:stackup": [
        {
            "ipc:layer": "Top",
            "ipc:material": "FR-4",
            "ipc:thickness": 0.2
        },
        {
            "ipc:layer": "Signal1",
            "ipc:material": "Copper",
            "ipc:thickness": 0.035
        }
    ]
}

# Combine context and data
jsonld_datasheet = {**multistandard_context, **embedded_controller}

# Validate and expand JSON-LD
expanded = jsonld.expand(jsonld_datasheet)
compacted = jsonld.compact(expanded, multistandard_context["@context"])

# Create knowledge graph
g = Graph()
g.parse(data=json.dumps(expanded), format="json-ld")

# Define traversal paths
paths = [
    (JEDEC.EmbeddedController, SPDX.hasFile, None),
    (SPDX.File, IPC.placement, None),
    (JEDEC.EmbeddedController, IPC.stackup, None)
]

# Perform graph traversal
def traverse_graph(graph, paths):
    results = []
    for s, p, o in paths:
        for subj, pred, obj in graph.triples((s, p, o)):
            results.append({
                "subject": subj,
                "predicate": pred,
                "object": obj if o is None else o
            })
    return results

# Execute traversal
traversal_results = traverse_graph(g, paths)

# Print results
print("Graph Traversal Results:")
for result in traversal_results:
    print(f"{result['subject']} --{result['predicate']}--> {result['object']}")

# SPARQL query for cross-standard relationships
query = """
PREFIX jedec: <https://jedec.org/ns/jep30#>
PREFIX spdx: <http://spdx.org/rdf/terms#>
PREFIX ipc: <https://ipc.org/ns/2581#>

SELECT ?component ?license ?layer
WHERE {
    ?controller a jedec:EmbeddedController ;
                spdx:hasFile ?component ;
                ipc:stackup ?layer .
    ?component spdx:licenseConcluded ?license .
}
"""

print("\nSPARQL Query Results:")
for row in g.query(query):
    print(f"Component: {row[0]} | License: {row[1]} | Layer: {row[2]}")
