# Basic demonstration of PyLD usage for JSON-LD processing

from pyld import jsonld
import json

# Define a simple JSON-LD document and context
doc = {
    "@context": {
        "name": "http://schema.org/name",
        "homepage": {
            "@id": "http://schema.org/url",
            "@type": "@id"
        },
        "image": {
            "@id": "http://schema.org/image",
            "@type": "@id"
        }
    },
    "name": "Manu Sporny",
    "homepage": "http://manu.sporny.org/",
    "image": "http://manu.sporny.org/images/manu.png"
}

# 1. Compact (already compact, but demonstrates API)
compacted = jsonld.compact(doc, doc["@context"])
print("Compacted JSON-LD:\n", json.dumps(compacted, indent=2))

# 2. Expand (shows all IRIs)
expanded = jsonld.expand(doc)
print("\nExpanded JSON-LD:\n", json.dumps(expanded, indent=2))

# 3. Normalize (to N-Quads/RDF)
nquads = jsonld.normalize(doc, {'format': 'application/n-quads'})
print("\nNormalized (N-Quads):\n", nquads)
