# File Description

* **context.jsonld -** JSON-LD context provides semantic meaning to each field, linking them to industry-standard ontologies.
* **ipc-2581-pcb-assembly-instructions.json** - describes board assembly using a JSON version of the IPC-2581 spec

* **spdx.json** - contains the BOM information.

* **usd-manufacturing-instructions.json** - contains the "manufacturing recipe"
* **merged-graph.jsonld** - An example of merging the files into a single document that could be used to drive. manufacturing line.

# **Process Description**

* **Each file is converted to JSON** using this context, enabling integration and interoperability across manufacturing, compliance, and digital twin platforms.
* **Interoperability:** Each `@id` node represents a different aspect (PCB, firmware, digital twin) but can be linked in your systems by the component name or BOM reference.

* **Extensibility:** You can add more nodes (e.g., test results, logistics) as your digital thread grows.
* **Semantic Search:** The context enables semantic queries (e.g., find all manufacturing steps for "ACME1234" or trace firmware licenses).

* This approach supports traceability, automation, and Industry 4.0 workflows for advanced semiconductor manufacturing.
